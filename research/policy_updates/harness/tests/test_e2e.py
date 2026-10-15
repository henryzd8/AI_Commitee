"""End-to-end on the mock backend: items -> histories -> build -> render -> run -> responses."""

import json

import pytest

from pu.build.histories import generate_histories, load_histories
from pu.build.ids import load_or_create_salt
from pu.build.requests import build_split
from pu.cli import main
from pu.io import read_jsonl, write_jsonl_atomic
from pu.render.base import PlainRenderer, render_file
from pu.run.backend import MockBackend, MockCrash
from pu.run.runner import load_responses, run
from pu.schemas import Split


def test_pipeline_with_crash_and_resume(tmp_path, small_items, models, texts, cfg):
    probes, hitems = small_items
    hist_path = tmp_path / "hist.jsonl"
    for m in models:
        generate_histories(
            MockBackend(m.id), PlainRenderer(), texts, probes, hitems, hist_path, cfg.sampling
        )
    histories = load_histories(hist_path)
    salt = load_or_create_salt(tmp_path / "keys")
    res = build_split(
        Split.CONFIRM,
        probes,
        hitems,
        histories,
        models,
        texts,
        cfg,
        salt,
        tmp_path / "conv",
        tmp_path / "keys",
    )
    for m in models:
        convs = tmp_path / f"conv/confirm/{m.id}.conversations.jsonl"
        reqs = tmp_path / f"req/{m.id}.jsonl"
        n = render_file(convs, reqs, PlainRenderer(), cfg.sampling, texts.hash)
        assert n == res.per_model[m.id]
        resp = tmp_path / f"resp/{m.id}.jsonl"
        with pytest.raises(MockCrash):
            run(reqs, resp, MockBackend(m.id, crash_after_requests=n // 2), batch_size=7)
        run(reqs, resp, MockBackend(m.id), batch_size=7)
        got = load_responses(resp)
        assert {r.request_id for r in got} == {d["request_id"] for d in read_jsonl(reqs)}
        assert len(got) == n  # no duplicates, nothing truncated in the default mock
    keys = list(read_jsonl(tmp_path / "keys/confirm.condition_key.jsonl"))
    assert len(keys) == res.n_conversations


def test_cli_build_render_run(tmp_path, small_items, small_histories, monkeypatch):
    probes, hitems = small_items
    write_jsonl_atomic(tmp_path / "items.jsonl", probes)
    write_jsonl_atomic(tmp_path / "hitems.jsonl", list(hitems.values()))
    turns = [t for recs in small_histories.values() for r in recs.values() for t in r.turns]
    write_jsonl_atomic(tmp_path / "hist.jsonl", turns)
    models_yaml = tmp_path / "models.yaml"
    models_yaml.write_text(
        "models:\n- {id: mA, hf_repo: fake/a, support: {C1: true, C2: true, C3: true, C4: true}}\n"
    )
    assert (
        main(
            [
                "build",
                "--split",
                "confirm",
                "--items",
                str(tmp_path / "items.jsonl"),
                "--history-items",
                str(tmp_path / "hitems.jsonl"),
                "--histories",
                str(tmp_path / "hist.jsonl"),
                "--models",
                "mA",
                "--models-config",
                str(models_yaml),
                "--out",
                str(tmp_path / "conv"),
                "--keys",
                str(tmp_path / "keys"),
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "render",
                "--model",
                "mA",
                "--models-config",
                str(models_yaml),
                "--conversations",
                str(tmp_path / "conv/confirm/mA.conversations.jsonl"),
                "--out",
                str(tmp_path / "req.jsonl"),
                "--renderer",
                "pu.render.base:plain_factory",
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "run",
                "--model",
                "mA",
                "--models-config",
                str(models_yaml),
                "--backend",
                "mock",
                "--requests",
                str(tmp_path / "req.jsonl"),
                "--responses",
                str(tmp_path / "resp.jsonl"),
            ]
        )
        == 0
    )
    m = json.loads((tmp_path / "resp.manifest.json").read_text())
    assert m["status"] == "complete" and m["config_hashes"]
