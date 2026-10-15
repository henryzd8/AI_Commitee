import json
import os
import re
from pathlib import Path

import pytest

from pu.build.cells import PRIMARY, CellSpec, manip_cells, recognition_cells, screen_cells
from pu.build.conversation import (
    RecogDraw,
    build_events,
    c4_timestamps,
    history_turn_events,
)
from pu.schemas import (
    HIST_P,
    HIST_R,
    Branch,
    Channel,
    Direction,
    EventType,
    Frame,
    Policy,
    history_source,
    policies_for,
    to_dict,
)

GOLDEN = Path(__file__).parent / "golden" / "conversations.json"


def cell(n, d, ch):
    frame, hist, rem = PRIMARY[n]
    return CellSpec(
        f"cell{n}-{d.value}-{ch.value}", Branch.PROBE, frame, hist, rem, ch, direction=d
    )


@pytest.fixture
def setup(small_items, small_histories, texts, cfg):
    probes, hitems = small_items
    item = probes[0]
    hist = small_histories[("mA", item.item_id)]
    hlist = [hitems[h] for h in item.history_item_ids]

    def make(spec, recog=None):
        h = hist[history_source(spec.direction, spec.history)] if spec.needs_history else None
        return build_events(spec, item, texts, cfg.c4_clock, h, hlist if h else None, recog)

    return make, item, texts, cfg


def types(events):
    return [e.type for e in events]


def body(texts, p):
    return texts.policy_body(p)


def test_no_unfilled_slots_anywhere(setup):
    make, *_ = setup
    for d in Direction:
        for ch in Channel:
            for n in PRIMARY:
                for e in make(cell(n, d, ch)):
                    blob = json.dumps(to_dict(e))
                    assert not re.search(r"\{[a-zA-Z_]+\}", blob), blob


def test_history_slot_and_order(setup):
    make, item, texts, _ = setup
    for d in Direction:
        for n in PRIMARY:
            spec = cell(n, d, Channel.C2)
            ev = make(spec)
            assistants = [e for e in ev if e.type == EventType.ASSISTANT]
            assert len(assistants) == 4
            assert all(e.source == history_source(d, spec.history) for e in assistants)
            assert f"|{history_source(d, spec.history)}|turn1]" in assistants[0].text
            users = [e for e in ev if e.type == EventType.USER]
            assert len(users) == 5
            assert users[-1].text == texts.probe(item.paraphrase_id, item.text)


def test_c1_switch_and_noop_differ_only_in_history(setup):
    make, *_ = setup
    for d in Direction:
        s = make(cell(1, d, Channel.C1))
        n = make(cell(2, d, Channel.C1))
        assert s[0] == n[0]  # same system prompt: only the new policy is visible
        assert [e for e in s if e.type != EventType.ASSISTANT] == [
            e for e in n if e.type != EventType.ASSISTANT
        ]
        assert [e.source for e in s if e.source] != [e.source for e in n if e.source]


def test_c2_frames(setup):
    make, _, texts, _ = setup
    for d in Direction:
        old, new = policies_for(d)
        s = make(cell(1, d, Channel.C2))
        n = make(cell(2, d, Channel.C2))
        assert body(texts, old) in s[0].text and body(texts, new) not in s[0].text
        assert body(texts, new) in n[0].text
        for ev in (s, n):
            mids = [e for e in ev if e.type == EventType.SYSTEM_MID]
            assert len(mids) == 1
            assert mids[0].text.startswith(texts.update_note) and body(texts, new) in mids[0].text
            idx = ev.index(mids[0])
            assert ev[idx - 1].type == EventType.ASSISTANT and ev[idx + 1].type == EventType.USER


def test_c3_tool_results(setup):
    make, _, texts, _ = setup
    for d in Direction:
        old, new = policies_for(d)
        for n, start in ((1, old), (2, new)):
            ev = make(cell(n, d, Channel.C3))
            assert texts.c3_instruction in ev[0].text
            assert (
                body(texts, Policy.R) not in ev[0].text and body(texts, Policy.P) not in ev[0].text
            )
            results = [e for e in ev if e.type == EventType.TOOL_RESULT]
            calls = [e for e in ev if e.type == EventType.TOOL_CALL]
            assert len(results) == 2 and len(calls) == 2
            assert results[0].content == {"policy": texts.policy_text(start)}
            assert results[1].content == {
                "policy": texts.policy_text(new),
                "note": texts.update_note,
            }
            assert types(ev)[:3] == [EventType.SYSTEM, EventType.TOOL_CALL, EventType.TOOL_RESULT]
            assert types(ev)[-3:] == [EventType.TOOL_CALL, EventType.TOOL_RESULT, EventType.USER]


def test_c4_rule_identical_and_clock(setup, cfg):
    make, *_ = setup
    for d in Direction:
        s = make(cell(1, d, Channel.C4))[0].text
        n = make(cell(2, d, Channel.C4))[0].text
        rule = lambda t: t.split("\n")[2]  # noqa: E731
        assert rule(s) == rule(n) and rule(s).startswith("Course policy schedule: Before ")
        assert s.splitlines()[-1] == n.splitlines()[-1]  # same current time
        assert s != n  # history timestamps differ
    T, sw = c4_timestamps(cfg.c4_clock, Frame.SWITCH)
    _, no = c4_timestamps(cfg.c4_clock, Frame.NOOP)
    assert sw[3] < T < sw[4] and T < no[0] < no[3] < no[4] and sw[4] == no[4]


def test_r3_per_channel(setup):
    make, _, texts, _ = setup
    for d in Direction:
        old, new = policies_for(d)
        notice = texts.r3_notice(new)
        for ch in Channel:
            r0 = make(cell(1, d, ch))
            r3 = make(cell(4, d, ch))
            assert r3[0].text.endswith(notice) or (ch == Channel.C4 and notice in r3[0].text)
            assert r3[1:] == r0[1:]  # only the system prompt changes
            assert body(texts, old) not in r3[0].text  # old policy no longer stated
            assert body(texts, new) in r3[0].text
        c3 = make(cell(4, d, Channel.C3))[0].text
        assert texts.c3_instruction in c3
        c4 = make(cell(4, d, Channel.C4))[0].text
        assert "Course policy schedule" not in c4 and "Conversation log" in c4
    # NOOP + R3 applies the same procedure
    n5 = make(cell(5, Direction.TIGHTEN, Channel.C3))
    assert texts.r3_notice(Policy.R) in n5[0].text


def test_static_frames(setup, texts):
    make, item, texts, cfg = setup
    for spec in screen_cells() + manip_cells():
        ev = make(spec)
        assert ev[-1].text == texts.probe(item.paraphrase_id, item.text)
        assert not any(e.type == EventType.ASSISTANT for e in ev)
        p = spec.policy
        if spec.channel == Channel.C2:
            assert body(texts, p) not in ev[0].text and ev[1].type == EventType.SYSTEM_MID
            assert ev[1].text == texts.policy_text(p)
        if spec.channel == Channel.C4:
            other = Policy.P if p == Policy.R else Policy.R
            assert f": {body(texts, other)} From " in ev[0].text  # before T: other
            assert ev[0].text.split("From ")[1].split(" on: ")[1].startswith(body(texts, p))
        if spec.channel == Channel.C3:
            assert ev[2].content == {"policy": texts.policy_text(p)}


def test_recognition_question(setup):
    make, _, texts, _ = setup
    spec = recognition_cells([Channel.C3], 3, False)[0]
    ev = make(spec, RecogDraw("prohibited", "B"))
    assert "prohibited" in ev[-1].text and "A) No B) Yes" in ev[-1].text
    ev = make(spec, RecogDraw("allowed", "A"))
    assert "allowed" in ev[-1].text and "A) Yes B) No" in ev[-1].text
    with pytest.raises(ValueError):
        make(spec, None)


def test_history_generation_prompt(small_items, texts):
    probes, hitems = small_items
    hl = [hitems[h] for h in probes[0].history_item_ids]
    ev = history_turn_events(texts, Policy.R, hl, ["a1", "a2"])
    assert types(ev) == [
        EventType.SYSTEM,
        EventType.USER,
        EventType.ASSISTANT,
        EventType.USER,
        EventType.ASSISTANT,
        EventType.USER,
    ]
    assert body(texts, Policy.R) in ev[0].text
    assert ev[-1].text == texts.student(3, hl[2].text)
    assert ev[1].text.startswith("I'm stuck") and ev[3].text.startswith("Can you just give")


def test_golden_snapshots(setup):
    """Snapshot of every primary cell and static frame for one fixed item.
    Regenerate deliberately with UPDATE_GOLDEN=1 after reviewing the diff."""
    make, *_ = setup
    snap = {}
    for d in Direction:
        for ch in Channel:
            for n in PRIMARY:
                snap[f"cell{n}-{d.value}-{ch.value}"] = [to_dict(e) for e in make(cell(n, d, ch))]
    for spec in manip_cells():
        snap[spec.name] = [to_dict(e) for e in make(spec)]
    if os.environ.get("UPDATE_GOLDEN") or not GOLDEN.exists():
        GOLDEN.parent.mkdir(exist_ok=True)
        GOLDEN.write_text(json.dumps(snap, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    assert json.loads(GOLDEN.read_text()) == json.loads(json.dumps(snap))
    assert HIST_R and HIST_P
