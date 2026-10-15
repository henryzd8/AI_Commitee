import pytest

from pu.build.histories import generate_histories, load_histories, load_turns
from pu.render.base import PlainRenderer
from pu.run.backend import GenResult, MockBackend, MockCrash, default_responder
from pu.schemas import Policy


def test_generates_four_sequential_turns(tmp_path, small_items, texts, cfg):
    probes, hitems = small_items
    prompts = []

    def responder(req):
        prompts.append(req.prompt)
        n = req.prompt.count("<|user|>")
        return GenResult(text=f"reply-to-turn-{n}", finish_reason="stop", completion_tokens=5)

    out = tmp_path / "h.jsonl"
    s = generate_histories(
        MockBackend("mA", responder), PlainRenderer(), texts, probes, hitems, out, cfg.sampling
    )
    assert s.turns_generated == len(probes) * 2 * 4
    hist = load_histories(out)
    assert len(hist) == len(probes)
    rec = hist[("mA", probes[0].item_id)]["R-hist"]
    assert [t.text for t in rec.turns] == [f"reply-to-turn-{k}" for k in range(1, 5)]
    # turn-4 prompts contain the model's own turns 1-3
    t4 = [p for p in prompts if p.count("<|user|>") == 4]
    assert t4 and all("reply-to-turn-3" in p for p in t4)
    # first prompt is item 1's R-hist turn 1: plain R system prompt, no channel frame
    assert texts.policy_body(Policy.R) in prompts[0] and "course_policy" not in prompts[0]
    assert texts.policy_body(Policy.P) in prompts[1]


def test_truncation_regenerated_once(tmp_path, small_items, texts, cfg):
    probes, hitems = small_items
    probes = probes[:1]

    def responder(req):
        if req.max_tokens < 2048:
            return GenResult("cut off", "length", req.max_tokens)
        return GenResult("<think>hmm</think>full answer", "stop", 40)

    out = tmp_path / "h.jsonl"
    s = generate_histories(
        MockBackend("mA", responder), PlainRenderer(), texts, probes, hitems, out, cfg.sampling
    )
    turns = load_turns(out)
    assert s.regenerated == 8 and s.still_truncated == 0
    assert all(t.attempt == 2 and t.text == "full answer" and t.reasoning_stripped for t in turns)

    def always_cut(req):
        return GenResult("cut", "length", req.max_tokens)

    out2 = tmp_path / "h2.jsonl"
    s2 = generate_histories(
        MockBackend("mA", always_cut), PlainRenderer(), texts, probes, hitems, out2, cfg.sampling
    )
    assert s2.still_truncated == 8
    assert all(t.truncated and t.attempt == 2 for t in load_turns(out2))
    assert len(load_histories(out2)) == 1  # kept and flagged, not filtered


def test_resume_after_crash(tmp_path, small_items, texts, cfg):
    probes, hitems = small_items
    out = tmp_path / "h.jsonl"
    total = len(probes) * 2 * 4
    with pytest.raises(MockCrash):
        generate_histories(
            MockBackend("mA", default_responder, crash_after_requests=total // 2),
            PlainRenderer(),
            texts,
            probes,
            hitems,
            out,
            cfg.sampling,
            batch_size=4,
        )
    partial = len(load_turns(out))
    assert 0 < partial < total
    s = generate_histories(
        MockBackend("mA"), PlainRenderer(), texts, probes, hitems, out, cfg.sampling, batch_size=4
    )
    assert s.turns_generated == total - partial
    turns = load_turns(out)
    assert len(turns) == total
    assert len({(t.probe_item_id, t.hist, t.turn) for t in turns}) == total
