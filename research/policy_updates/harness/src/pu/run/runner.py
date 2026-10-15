"""Resumable runner for rendered requests (handbook §6.4).

* Attempt 1 for every request, in checkpointed batches (append + fsync per batch).
* One retry (attempt 2, double budget) for responses that hit the token cap *without* a
  disclosure. The disclosure check is Task 4's checker; until it exists, `retry_all_truncated`
  retries every truncated response (costs extra calls only; downstream selection uses Task 4).
* Resumable: requests that already have a record for an attempt are skipped.
* A manifest is written at start (status=running) and rewritten at the end (status=complete).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pu.io import append_jsonl, read_jsonl, sha256_file, write_json_atomic
from pu.render.base import request_seed
from pu.run.backend import Backend, GenRequest, strip_reasoning
from pu.run.manifest import environment, now_iso
from pu.schemas import RenderedRequest, ResponseRecord, from_dict

DisclosureCheck = Callable[[RenderedRequest, str], bool]


def retry_all_truncated(request: RenderedRequest, text: str) -> bool:
    """Placeholder until Task 4's checker exists: treat every truncated response as having no
    disclosure, so it is retried. Never drops data; attempt 1 is always kept."""
    return False


@dataclass
class RunSummary:
    requested: int = 0
    attempt1_done_before: int = 0
    attempt1_new: int = 0
    truncated_attempt1: int = 0
    retried: int = 0
    still_truncated: int = 0
    reasoning_stripped: int = 0
    batches: int = 0
    extra: dict[str, Any] = field(default_factory=dict)


def load_requests(path: str | Path) -> list[RenderedRequest]:
    return [from_dict(RenderedRequest, d) for d in read_jsonl(path)]


def load_responses(path: str | Path) -> list[ResponseRecord]:
    return [from_dict(ResponseRecord, d) for d in read_jsonl(path)]


def _record(
    backend: Backend, req: RenderedRequest, gen_req: GenRequest, res, attempt: int
) -> ResponseRecord:
    visible, stripped = strip_reasoning(res.text)
    return ResponseRecord(
        request_id=req.request_id,
        model_id=req.model_id,
        text=visible,
        raw_text=res.text if stripped else None,
        reasoning_stripped=stripped,
        finish_reason=res.finish_reason,
        completion_tokens=res.completion_tokens,
        prompt_tokens=res.prompt_tokens if res.prompt_tokens is not None else req.prompt_tokens,
        attempt=attempt,
        max_tokens=gen_req.max_tokens,
        seed=gen_req.seed,
        weights_hash=backend.weights_hash,
        vllm_version=backend.engine_version,
        backend=backend.name,
        ts=now_iso(),
    )


def _run_batches(
    backend: Backend,
    jobs: list[tuple[RenderedRequest, GenRequest]],
    attempt: int,
    out_path: Path,
    batch_size: int,
    summary: RunSummary,
) -> list[ResponseRecord]:
    written: list[ResponseRecord] = []
    for i in range(0, len(jobs), batch_size):
        chunk = jobs[i : i + batch_size]
        results = backend.generate([g for _, g in chunk])
        if len(results) != len(chunk):
            raise RuntimeError("backend returned a different number of results")
        recs = [
            _record(backend, r, g, res, attempt) for (r, g), res in zip(chunk, results, strict=True)
        ]
        append_jsonl(out_path, recs)
        summary.batches += 1
        summary.reasoning_stripped += sum(r.reasoning_stripped for r in recs)
        written += recs
    return written


def run(
    requests_path: str | Path,
    responses_path: str | Path,
    backend: Backend,
    *,
    retry_max_tokens: int = 2048,
    batch_size: int = 256,
    disclosure_check: DisclosureCheck = retry_all_truncated,
    manifest_path: str | Path | None = None,
    config_hashes: dict[str, str] | None = None,
) -> RunSummary:
    requests_path, responses_path = Path(requests_path), Path(responses_path)
    manifest_path = (
        Path(manifest_path) if manifest_path else responses_path.with_suffix(".manifest.json")
    )
    requests = load_requests(requests_path)
    wrong = {r.model_id for r in requests} - {backend.model_id}
    if wrong:
        raise ValueError(f"requests for {sorted(wrong)} given to backend for {backend.model_id}")
    if len({r.request_id for r in requests}) != len(requests):
        raise ValueError("duplicate request_id in requests file")
    by_id = {r.request_id: r for r in requests}

    summary = RunSummary(requested=len(requests))
    manifest: dict[str, Any] = {
        "status": "running",
        "started": now_iso(),
        "model_id": backend.model_id,
        "backend": backend.name,
        "engine_version": backend.engine_version,
        "weights_hash": backend.weights_hash,
        "requests_file": str(requests_path),
        "requests_sha256": sha256_file(requests_path),
        "responses_file": str(responses_path),
        "retry_max_tokens": retry_max_tokens,
        "batch_size": batch_size,
        "disclosure_check": getattr(disclosure_check, "__name__", str(disclosure_check)),
        "text_lib_hashes": sorted({r.text_lib_hash or "" for r in requests}),
        "config_hashes": config_hashes or {},
        "environment": environment(),
    }
    write_json_atomic(manifest_path, manifest)

    existing = load_responses(responses_path)
    done = {(r.request_id, r.attempt) for r in existing}
    att1 = {r.request_id: r for r in existing if r.attempt == 1}
    summary.attempt1_done_before = len(att1)

    # -- attempt 1
    jobs = [
        (r, GenRequest(r.prompt, r.sampling.temperature, r.sampling.max_tokens, r.sampling.seed))
        for r in requests
        if (r.request_id, 1) not in done
    ]
    for rec in _run_batches(backend, jobs, 1, responses_path, batch_size, summary):
        att1[rec.request_id] = rec
    summary.attempt1_new = len(jobs)

    # -- attempt 2: truncated without a disclosure, once, at double budget
    truncated = [rec for rec in att1.values() if rec.finish_reason == "length"]
    summary.truncated_attempt1 = len(truncated)
    retry_jobs = []
    for rec in truncated:
        req = by_id[rec.request_id]
        if (rec.request_id, 2) in done or disclosure_check(req, rec.text):
            continue
        retry_jobs.append(
            (
                req,
                GenRequest(
                    req.prompt,
                    req.sampling.temperature,
                    retry_max_tokens,
                    request_seed(req.request_id, 2),
                ),
            )
        )
    _run_batches(backend, retry_jobs, 2, responses_path, batch_size, summary)
    summary.retried = len(retry_jobs)

    final = load_responses(responses_path)
    att2 = {r.request_id: r for r in final if r.attempt == 2}
    summary.still_truncated = sum(1 for r in att2.values() if r.finish_reason == "length")

    final_ids = {r.request_id for r in final if r.attempt == 1}
    missing = set(by_id) - final_ids
    manifest.update(
        {
            "status": "complete" if not missing else "incomplete",
            "finished": now_iso(),
            "responses_sha256": sha256_file(responses_path) if responses_path.exists() else None,
            "counts": {
                "requested": summary.requested,
                "attempt1_done_before": summary.attempt1_done_before,
                "attempt1_new": summary.attempt1_new,
                "truncated_attempt1": summary.truncated_attempt1,
                "retried": summary.retried,
                "still_truncated_after_retry": summary.still_truncated,
                "reasoning_stripped": summary.reasoning_stripped,
                "missing": len(missing),
            },
        }
    )
    write_json_atomic(manifest_path, manifest)
    return summary
