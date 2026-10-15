"""Conversation assembly (handbook §5.2, §6.2; design §4.2-4.4).

Each NeutralConversation is the *final call* for one condition: the full event list the model
sees on turn 5 (or on turn 1 for static cells). Model-specific chat formatting is Task 2's
renderer; this module is model-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from pu.build.cells import CellSpec
from pu.config import C4Clock
from pu.schemas import (
    Branch,
    Channel,
    Event,
    EventType,
    Frame,
    HistoryTurn,
    Item,
    Policy,
    Remedy,
    policies_for,
)
from pu.texts.library import TextLibrary

TS_FMT = "%Y-%m-%d %H:%M"


@dataclass
class HistoryRecord:
    """One generated 4-turn history (R-hist or P-hist) for one probe item and model."""

    model_id: str
    probe_item_id: str
    hist: str
    turns: list[HistoryTurn]

    def __post_init__(self) -> None:
        self.turns = sorted(self.turns, key=lambda t: t.turn)
        if [t.turn for t in self.turns] != [1, 2, 3, 4]:
            raise ValueError(f"history {self.probe_item_id}/{self.hist} is not 4 complete turns")


@dataclass(frozen=True)
class RecogDraw:
    polarity: str  # "allowed" | "prohibited"
    yes_option: str  # "A" | "B"


def other(p: Policy) -> Policy:
    return Policy.P if p == Policy.R else Policy.R


# ------------------------------------------------------------------ C4 clock


def c4_timestamps(clock: C4Clock, frame: Frame) -> tuple[str, list[str]]:
    """Return (T, [t1..t5]) for a 5-turn conversation.

    SWITCH: t1..t4 < T < t5 = T + g. NOOP: T < t1..t4 < t5 = T + g (history compressed after T).
    T and t5 are identical in both frames, so the rule text and the current time match.
    """
    base = clock.base_dt()
    sp = timedelta(minutes=clock.switch_spacing_min)
    g = timedelta(minutes=clock.gap_min)
    t_rule = base + 4 * sp  # T, one spacing after SWITCH turn 4
    t5 = t_rule + g
    if frame == Frame.SWITCH:
        hist = [base + k * sp for k in range(4)]
    elif frame == Frame.NOOP:
        off = timedelta(minutes=clock.noop_offset_min)
        nsp = timedelta(minutes=clock.noop_spacing_min)
        hist = [t_rule + off + k * nsp for k in range(4)]
    else:
        raise ValueError("c4_timestamps is for SWITCH/NOOP frames")
    ts = hist + [t5]
    assert all(a < b for a, b in zip(ts, ts[1:], strict=False)), "timestamps must increase"
    if frame == Frame.SWITCH:
        assert ts[3] < t_rule < ts[4]
    else:
        assert t_rule < ts[0]
    return t_rule.strftime(TS_FMT), [t.strftime(TS_FMT) for t in ts]


def c4_static_timestamps(clock: C4Clock) -> tuple[str, list[str]]:
    """Manipulation check: one turn, after T by g.

    The rule reads 'Before T: other policy. From T on: delivered policy.'
    """
    base = clock.base_dt()
    t_rule = base + 4 * timedelta(minutes=clock.switch_spacing_min)
    t1 = t_rule + timedelta(minutes=clock.gap_min)
    return t_rule.strftime(TS_FMT), [t1.strftime(TS_FMT)]


# --------------------------------------------------------------- frames


def _tool_events(texts: TextLibrary, content: dict) -> list[Event]:
    return [
        Event(type=EventType.TOOL_CALL, name=texts.tool_name, args={}),
        Event(type=EventType.TOOL_RESULT, name=texts.tool_name, content=content),
    ]


def _static_frame(ch: Channel, p: Policy, texts: TextLibrary, clock: C4Clock) -> list[Event]:
    if ch == Channel.C1:
        return [Event(type=EventType.SYSTEM, text=texts.system_with_policy(p, ch))]
    if ch == Channel.C2:
        return [
            Event(type=EventType.SYSTEM, text=texts.system_neutral(ch)),
            Event(type=EventType.SYSTEM_MID, text=texts.policy_text(p)),
        ]
    if ch == Channel.C3:
        return [Event(type=EventType.SYSTEM, text=texts.system_c3())] + _tool_events(
            texts, {"policy": texts.policy_text(p)}
        )
    t_rule, ts = c4_static_timestamps(clock)
    return [Event(type=EventType.SYSTEM, text=texts.system_c4(t_rule, other(p), p, ts))]


def _dynamic_start(spec: CellSpec, texts: TextLibrary, clock: C4Clock) -> list[Event]:
    old, new = policies_for(spec.direction)  # type: ignore[arg-type]
    start = old if spec.frame == Frame.SWITCH else new
    ch = spec.channel
    if ch == Channel.C1:
        # Silent replacement: the final call shows only the current policy in both frames.
        return [Event(type=EventType.SYSTEM, text=texts.system_with_policy(new, ch))]
    if ch == Channel.C2:
        return [Event(type=EventType.SYSTEM, text=texts.system_with_policy(start, ch))]
    if ch == Channel.C3:
        return [Event(type=EventType.SYSTEM, text=texts.system_c3())] + _tool_events(
            texts, {"policy": texts.policy_text(start)}
        )
    t_rule, ts = c4_timestamps(clock, spec.frame)
    return [Event(type=EventType.SYSTEM, text=texts.system_c4(t_rule, old, new, ts))]


def _update_events(spec: CellSpec, texts: TextLibrary) -> list[Event]:
    _, new = policies_for(spec.direction)  # type: ignore[arg-type]
    if spec.channel == Channel.C2:
        return [
            Event(type=EventType.SYSTEM_MID, text=f"{texts.update_note} {texts.policy_text(new)}")
        ]
    if spec.channel == Channel.C3:
        return _tool_events(texts, {"policy": texts.policy_text(new), "note": texts.update_note})
    return []  # C1: no event; C4: the clock crossing T is the change


def r3_system(spec: CellSpec, texts: TextLibrary, clock: C4Clock) -> str:
    """System prompt after the operator applies the remedy (handbook §5.2, design §4.4)."""
    _, new = policies_for(spec.direction)  # type: ignore[arg-type]
    notice = texts.r3_notice(new)
    ch = spec.channel
    if ch in (Channel.C1, Channel.C2):
        return f"{texts.system_with_policy(new, ch)}\n\n{notice}"
    if ch == Channel.C3:
        return (
            f"{texts.role}\n\n{texts.c3_instruction}\n{texts.policy_text(new)}\n"
            f"{texts.shared_lines(ch)}\n\n{notice}"
        )
    _, ts = c4_timestamps(clock, spec.frame)
    return (
        f"{texts.role}\n\n{texts.policy_text(new)}\n{texts.shared_lines(ch)}\n\n{notice}\n\n"
        f"{texts.c4_log(ts)}"
    )


# --------------------------------------------------------------- assembly


def build_events(
    spec: CellSpec,
    item: Item,
    texts: TextLibrary,
    clock: C4Clock,
    history: HistoryRecord | None = None,
    history_items: list[Item] | None = None,
    recog: RecogDraw | None = None,
) -> list[Event]:
    if spec.frame == Frame.STATIC:
        assert spec.policy is not None
        events = _static_frame(spec.channel, spec.policy, texts, clock)
    else:
        if history is None or history_items is None or len(history_items) != 4:
            raise ValueError(f"{spec.name} needs a 4-turn history and 4 history items")
        events = _dynamic_start(spec, texts, clock)
        for i in range(4):
            events.append(
                Event(type=EventType.USER, text=texts.student(i + 1, history_items[i].text))
            )
            events.append(
                Event(type=EventType.ASSISTANT, text=history.turns[i].text, source=history.hist)
            )
        events += _update_events(spec, texts)
        if spec.remedy == Remedy.R3:
            events[0] = Event(type=EventType.SYSTEM, text=r3_system(spec, texts, clock))

    if spec.branch == Branch.RECOG:
        if recog is None:
            raise ValueError("recognition cell needs a RecogDraw")
        events.append(
            Event(type=EventType.USER, text=texts.recognition(recog.polarity, recog.yes_option))
        )
    else:
        if item.paraphrase_id is None:
            raise ValueError(f"probe item {item.item_id} has no paraphrase_id")
        events.append(Event(type=EventType.USER, text=texts.probe(item.paraphrase_id, item.text)))
    return events


def history_turn_events(
    texts: TextLibrary,
    policy: Policy,
    history_items: list[Item],
    previous_texts: list[str],
) -> list[Event]:
    """Prompt for generating history turn len(previous_texts)+1 under a plain R or P prompt."""
    turn = len(previous_texts) + 1
    events = [Event(type=EventType.SYSTEM, text=texts.system_with_policy(policy, Channel.C1))]
    for i, prev in enumerate(previous_texts):
        events.append(Event(type=EventType.USER, text=texts.student(i + 1, history_items[i].text)))
        events.append(Event(type=EventType.ASSISTANT, text=prev))
    events.append(
        Event(type=EventType.USER, text=texts.student(turn, history_items[turn - 1].text))
    )
    return events
