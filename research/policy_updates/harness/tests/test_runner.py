import json

import pytest

from pu.io import read_jsonl, write_jsonl_atomic
from pu.render.base import request_seed
from pu.run.backend import GenResult, MockBackend, MockCrash, strip_reasoning
from pu.run.runner import load_responses, run
from pu.schemas import RenderedRequest, Sampling


def make_requests(path, n=10, model="mA", truncate_every=0):
    reqs = []
    for i in range(n):
        rid = f"00000000-0000-4000-8000-{i:012d}"
        marker = "[[TRUNCATE]]" if truncate_every and i % truncate_every == 0 else ""
        reqs.append(
            RenderedRequest(
                rid,
                model,
                f"prompt {i} {marker}",
                Sampling(0.7, 1024, request_seed(rid, 1)),
                prompt_tokens=5,
            )
        )
    write_jsonl_atomic(path, reqs)
    return reqs


def test_runs_all_and_writes_manifest(tmp_path):
    make_requests(tmp_path / "req.jsonl", 10)
    s = run(tmp_path / "req.jsonl", tmp_path / "resp.jsonl", MockBackend("mA"), batch_size=3)
    resp = load_responses(tmp_path / "resp.jsonl")
    assert s.attempt1_new == 10 and len(resp) == 10 and s.batches == 4
    assert all(r.attempt == 1 and r.max_tokens == 1024 and r.backend == "mock" for r in resp)
    m = json.loads((tmp_path / "resp.manifest.json").read_text())
    assert m["status"] == "complete" and m["counts"]["requested"] == 10
    assert m["requests_sha256"] and m["environment"]["python"]


def test_resume_after_crash_no_duplicates(tmp_path):
    make_requests(tmp_path / "req.jsonl", 10)
    with pytest.raises(MockCrash):
        run(
            tmp_path / "req.jsonl",
            tmp_path / "resp.jsonl",
            MockBackend("mA", crash_after_requests=6),
            batch_size=3,
        )
    assert len(load_responses(tmp_path / "resp.jsonl")) == 6
    m = json.loads((tmp_path / "resp.manifest.json").read_text())
    assert m["status"] == "running"  # crash leaves the manifest marked unfinished
    s = run(tmp_path / "req.jsonl", tmp_path / "resp.jsonl", MockBackend("mA"), batch_size=3)
    resp = load_responses(tmp_path / "resp.jsonl")
    assert s.attempt1_done_before == 6 and s.attempt1_new == 4
    assert len(resp) == 10 and len({r.request_id for r in resp}) == 10
    # re-running a finished file does nothing
    s2 = run(tmp_path / "req.jsonl", tmp_path / "resp.jsonl", MockBackend("mA"))
    assert s2.attempt1_new == 0 and s2.retried == 0


def test_half_written_last_line_is_tolerated(tmp_path):
    make_requests(tmp_path / "req.jsonl", 4)
    run(tmp_path / "req.jsonl", tmp_path / "resp.jsonl", MockBackend("mA"), batch_size=2)
    lines = (tmp_path / "resp.jsonl").read_text().splitlines()
    (tmp_path / "resp.jsonl").write_text("\n".join(lines[:3]) + "\n" + lines[3][:20])
    run(tmp_path / "req.jsonl", tmp_path / "resp.jsonl", MockBackend("mA"))
    ids = [r["request_id"] for r in read_jsonl(tmp_path / "resp.jsonl")]
    assert len(set(ids)) == 4


def test_truncation_retry_once_at_double_budget(tmp_path):
    reqs = make_requests(tmp_path / "req.jsonl", 9, truncate_every=3)
    s = run(tmp_path / "req.jsonl", tmp_path / "resp.jsonl", MockBackend("mA"))
    resp = load_responses(tmp_path / "resp.jsonl")
    a2 = [r for r in resp if r.attempt == 2]
    assert s.truncated_attempt1 == 3 and s.retried == 3 and len(a2) == 3
    assert all(r.max_tokens == 2048 and r.finish_reason == "stop" for r in a2)
    by_id = {r.request_id: r for r in reqs}
    assert all(
        r.seed == request_seed(r.request_id, 2) != by_id[r.request_id].sampling.seed for r in a2
    )
    assert s.still_truncated == 0


def test_no_retry_when_disclosure_present(tmp_path):
    make_requests(tmp_path / "req.jsonl", 6, truncate_every=2)
    s = run(
        tmp_path / "req.jsonl",
        tmp_path / "resp.jsonl",
        MockBackend("mA"),
        disclosure_check=lambda req, text: True,
    )
    assert s.truncated_attempt1 == 3 and s.retried == 0


def test_still_truncated_counted(tmp_path):
    make_requests(tmp_path / "req.jsonl", 3)

    def cut(req):
        return GenResult("x", "length", req.max_tokens)

    s = run(tmp_path / "req.jsonl", tmp_path / "resp.jsonl", MockBackend("mA", cut))
    assert s.retried == 3 and s.still_truncated == 3


def test_model_mismatch_rejected(tmp_path):
    make_requests(tmp_path / "req.jsonl", 2, model="mA")
    with pytest.raises(ValueError):
        run(tmp_path / "req.jsonl", tmp_path / "resp.jsonl", MockBackend("mB"))


@pytest.mark.parametrize(
    "raw,visible,stripped",
    [
        ("plain answer", "plain answer", False),
        ("<think>secret</think>\nAnswer", "Answer", True),
        ("<think>never closed", "", True),
        ("leftover</think> Answer", "Answer", True),
    ],
)
def test_strip_reasoning(raw, visible, stripped):
    assert strip_reasoning(raw) == (visible, stripped)
