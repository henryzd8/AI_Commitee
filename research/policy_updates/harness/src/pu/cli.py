"""Command line: `pu <command>`. Run `pu <command> -h` for options."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

from pu.config import CONFIG_DIR, ModelSpec, RunConfig, load_models
from pu.io import read_jsonl
from pu.schemas import Item, Split, from_dict
from pu.texts.library import TextLibrary


def _items(path: str) -> list[Item]:
    return [from_dict(Item, d) for d in read_jsonl(path)]


def _models(ids: str, models_path: str | None) -> list[ModelSpec]:
    specs = load_models(models_path)
    return [specs[i] for i in ids.split(",")]


def _renderer_factory(dotted: str):
    """'package.module:callable' -> callable(model_spec, texts) -> Renderer."""
    mod, _, attr = dotted.partition(":")
    return getattr(importlib.import_module(mod), attr)


def _backend(args, spec: ModelSpec):
    if args.backend == "mock":
        from pu.run.backend import MockBackend

        return MockBackend(model_id=spec.id)
    from pu.run.backend import VLLMBackend

    return VLLMBackend(
        model_id=spec.id,
        model_path=args.model_path or spec.hf_repo,
        revision=None if args.model_path else spec.revision,
        weights_hash=spec.weights_sha256,
        tensor_parallel_size=spec.tensor_parallel_size,
        dtype=spec.dtype,
        quantization=spec.quantization,
        max_model_len=spec.max_model_len,
        gpu_memory_utilization=spec.gpu_memory_utilization,
    )


def cmd_build(args) -> int:
    from pu.build.histories import load_histories
    from pu.build.ids import load_or_create_salt
    from pu.build.requests import build_split

    cfg = RunConfig.load(args.run_config)
    texts = TextLibrary(args.texts)
    probes = _items(args.items)
    hitems = {it.item_id: it for it in _items(args.history_items)} if args.history_items else {}
    hist = load_histories(args.histories) if args.histories else {}
    res = build_split(
        Split(args.split),
        probes,
        hitems,
        hist,
        _models(args.models, args.models_config),
        texts,
        cfg,
        load_or_create_salt(args.keys),
        args.out,
        args.keys,
        allow_unknown_support=args.allow_unknown_support,
    )
    print(
        json.dumps(
            {"n": res.n_conversations, "per_model": res.per_model, "skipped": res.skipped}, indent=2
        )
    )
    return 0


def cmd_render(args) -> int:
    from pu.render.base import render_file

    cfg = RunConfig.load(args.run_config)
    texts = TextLibrary(args.texts)
    spec = load_models(args.models_config)[args.model]
    renderer = _renderer_factory(args.renderer)(spec, texts)
    n = render_file(args.conversations, args.out, renderer, cfg.sampling, texts.hash)
    print(f"rendered {n} requests -> {args.out}")
    return 0


def cmd_run(args) -> int:
    from pu.run.manifest import config_hashes
    from pu.run.runner import run

    cfg = RunConfig.load(args.run_config)
    spec = load_models(args.models_config)[args.model]
    backend = _backend(args, spec)
    hashes = config_hashes(
        [
            args.run_config or CONFIG_DIR / "run.yaml",
            args.models_config or CONFIG_DIR / "models.yaml",
        ]
    )
    s = run(
        args.requests,
        args.responses,
        backend,
        retry_max_tokens=cfg.sampling.retry_max_tokens,
        batch_size=cfg.batch_size,
        config_hashes=hashes,
    )
    print(json.dumps(vars(s), indent=2, default=str))
    return 0


def cmd_histories(args) -> int:
    from pu.build.histories import generate_histories

    cfg = RunConfig.load(args.run_config)
    texts = TextLibrary(args.texts)
    spec = load_models(args.models_config)[args.model]
    renderer = _renderer_factory(args.renderer)(spec, texts)
    s = generate_histories(
        _backend(args, spec),
        renderer,
        texts,
        _items(args.items),
        {it.item_id: it for it in _items(args.history_items)},
        args.out,
        cfg.sampling,
        cfg.batch_size,
    )
    print(json.dumps(vars(s), indent=2))
    return 0


def cmd_estimate(args) -> int:
    from pu.env.estimate import estimate, format_table

    cfg = RunConfig.load(args.run_config)
    specs = load_models(args.models_config)
    ids = (
        args.models.split(",")
        if args.models
        else [k for k, v in specs.items() if v.role == "candidate"]
    )
    print(format_table(estimate([specs[i] for i in ids], cfg, TextLibrary(args.texts))))
    print(
        "\nThroughput figures are ASSUMPTIONS (configs/run.yaml: estimate). "
        "Replace after the smoke test."
    )
    return 0


def cmd_download_weights(args) -> int:
    from pu.env.weights import download_model, hash_model_dir, record_in_models_yaml

    spec = load_models(args.models_config)[args.model]
    sha, path = download_model(spec.hf_repo, spec.revision, Path(args.dest) / spec.id)
    combined, files = hash_model_dir(path)
    record_in_models_yaml(spec.id, sha, combined, args.models_config)
    print(
        json.dumps(
            {
                "model": spec.id,
                "revision": sha,
                "weights_sha256": combined,
                "files": len(files),
                "path": str(path),
            },
            indent=2,
        )
    )
    return 0


def cmd_hash_weights(args) -> int:
    from pu.env.weights import hash_model_dir

    combined, files = hash_model_dir(args.dir)
    print(json.dumps({"weights_sha256": combined, "files": files}, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="pu", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, texts=True):
        sp.add_argument("--run-config", default=None)
        sp.add_argument("--models-config", default=None)
        if texts:
            sp.add_argument("--texts", default=None, help="text library YAML (default v0)")

    b = sub.add_parser("build", help="build neutral conversations + blinded keys for a split")
    common(b)
    b.add_argument("--split", required=True, choices=[s.value for s in Split])
    b.add_argument("--items", required=True)
    b.add_argument("--history-items")
    b.add_argument("--histories", help="history turns JSONL from `pu histories`")
    b.add_argument("--models", required=True, help="comma-separated model ids")
    b.add_argument("--out", default="data/conversations")
    b.add_argument("--keys", default="keys")
    b.add_argument("--allow-unknown-support", action="store_true", help="tests only")
    b.set_defaults(fn=cmd_build)

    r = sub.add_parser("render", help="render conversations for one model (Task 2 renderer)")
    common(r)
    r.add_argument("--model", required=True)
    r.add_argument("--conversations", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--renderer", required=True, help="module:factory(model_spec, texts)")
    r.set_defaults(fn=cmd_render)

    for name, fn, helptext in (
        ("run", cmd_run, "run rendered requests for one model"),
        ("histories", cmd_histories, "generate R-hist/P-hist for probe items"),
    ):
        sp = sub.add_parser(name, help=helptext)
        common(sp)
        sp.add_argument("--model", required=True)
        sp.add_argument("--backend", choices=["mock", "vllm"], default="mock")
        sp.add_argument("--model-path", help="local weights dir (else hf_repo@revision)")
        if name == "run":
            sp.add_argument("--requests", required=True)
            sp.add_argument("--responses", required=True)
        else:
            sp.add_argument("--items", required=True)
            sp.add_argument("--history-items", required=True)
            sp.add_argument("--out", required=True)
            sp.add_argument("--renderer", required=True)
        sp.set_defaults(fn=fn)

    e = sub.add_parser("estimate", help="token-count-based GPU-hour estimate")
    common(e)
    e.add_argument("--models", help="comma-separated ids (default: all candidates)")
    e.set_defaults(fn=cmd_estimate)

    d = sub.add_parser("download-weights", help="download pinned weights and record hashes")
    common(d, texts=False)
    d.add_argument("--model", required=True)
    d.add_argument("--dest", default="/data/models")
    d.set_defaults(fn=cmd_download_weights)

    h = sub.add_parser("hash-weights", help="hash a local model directory")
    h.add_argument("--dir", required=True)
    h.set_defaults(fn=cmd_hash_weights)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
