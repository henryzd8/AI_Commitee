"""Shared data formats (handbook §3). Frozen on day 1; changes need all five owners.

Every record is a plain dataclass serialised to one JSON object per JSONL line.
Enums serialise to their string values.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar

SCHEMA_VERSION = "1.0"


class Direction(str, Enum):
    LOOSEN = "loosen"  # R -> P
    TIGHTEN = "tighten"  # P -> R


class Frame(str, Enum):
    SWITCH = "SWITCH"
    NOOP = "NOOP"
    STATIC = "STATIC"  # no history, one policy (screen / manipulation check)


class History(str, Enum):
    OLD_SELF = "OLD-SELF"
    NEW_SELF = "NEW-SELF"
    NONE = "NONE"


class Remedy(str, Enum):
    R0 = "R0"
    R3 = "R3"


class Channel(str, Enum):
    C1 = "C1"  # silent system-prompt replacement
    C2 = "C2"  # mid-conversation system message
    C3 = "C3"  # course_policy tool result
    C4 = "C4"  # dated rule + timestamp log


class Branch(str, Enum):
    PROBE = "probe"
    RECOG = "recog"
    SCREEN = "screen"
    MANIP = "manip"


class Policy(str, Enum):
    R = "R"  # must not give the final answer
    P = "P"  # must give the full solution when asked


class Split(str, Enum):
    SCREEN = "screen"
    EXPLORE = "explore"
    MANIP = "manip"
    CALIB = "calib"
    CONFIRM = "confirm"


class EventType(str, Enum):
    SYSTEM = "system"
    SYSTEM_MID = "system_mid"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    USER = "user"
    ASSISTANT = "assistant"


HIST_R = "R-hist"
HIST_P = "P-hist"


def policies_for(direction: Direction) -> tuple[Policy, Policy]:
    """Return (old, new) policy for a direction."""
    return (Policy.R, Policy.P) if direction == Direction.LOOSEN else (Policy.P, Policy.R)


def history_source(direction: Direction, history: History) -> str:
    """Which generated history fills a slot.

    Loosen: OLD-SELF = R-hist, NEW-SELF = P-hist. Tighten: OLD-SELF = P-hist, NEW-SELF = R-hist.
    """
    if history == History.NONE:
        raise ValueError("cell has no history")
    old, new = policies_for(direction)
    pol = old if history == History.OLD_SELF else new
    return HIST_R if pol == Policy.R else HIST_P


def violation(direction: Direction, given: bool) -> bool:
    """Y = 1 if the response violates the *current* policy.

    Tighten (current R): Y = GIVEN. Loosen (current P): Y = not GIVEN.
    """
    return given if direction == Direction.TIGHTEN else not given


# ---------------------------------------------------------------- records


@dataclass
class Step:
    name: str
    value: int


@dataclass
class Item:
    item_id: str
    family_id: str
    role: str  # "probe" | "history"
    split: str
    seed: int
    index: int
    text: str
    steps: list[Step]
    final_answer: int
    paraphrase_id: int | None = None
    history_item_ids: list[str] = field(default_factory=list)
    heldout_family: bool = False


@dataclass
class Event:
    type: EventType
    text: str | None = None
    name: str | None = None
    args: dict[str, Any] | None = None
    content: dict[str, Any] | None = None
    source: str | None = None  # assistant turns: "R-hist" | "P-hist"


@dataclass
class NeutralConversation:
    conv_id: str
    model_id: str
    events: list[Event]


@dataclass
class Sampling:
    temperature: float
    max_tokens: int
    seed: int


@dataclass
class RenderedRequest:
    request_id: str
    model_id: str
    prompt: str
    sampling: Sampling
    prompt_tokens: int | None = None
    text_lib_hash: str | None = None
    render_hash: str | None = None


@dataclass
class ResponseRecord:
    request_id: str
    model_id: str
    text: str  # visible text (reasoning blocks stripped)
    finish_reason: str | None
    completion_tokens: int | None
    attempt: int
    prompt_tokens: int | None = None
    max_tokens: int | None = None
    seed: int | None = None
    weights_hash: str | None = None
    vllm_version: str | None = None
    backend: str | None = None
    ts: str | None = None
    raw_text: str | None = None
    reasoning_stripped: bool = False


@dataclass
class LabelRecord:
    request_id: str
    checker_version: str
    given: bool
    help: bool
    refuse: bool
    confirm_seeking: bool
    bare_answer: bool
    truncated: bool
    recog_answer: str | None = None


@dataclass
class ConditionKey:
    """Blinded: written only to keys/, read only by the blinded analyst (Task 5)."""

    request_id: str
    model_id: str
    split: str
    branch: Branch
    frame: Frame
    history: History
    remedy: Remedy
    channel: Channel
    item_id: str
    sample_idx: int = 0
    direction: Direction | None = None
    policy: Policy | None = None  # delivered policy for STATIC cells
    cell: str | None = None  # human-readable cell name


@dataclass
class RecogMeta:
    """Not blinded: needed by the Task 4 parser to undo randomisation."""

    request_id: str
    polarity: str  # "allowed" | "prohibited"
    yes_option: str  # "A" | "B"


@dataclass
class HistoryTurn:
    model_id: str
    probe_item_id: str
    hist: str  # "R-hist" | "P-hist"
    turn: int  # 1..4
    text: str  # visible text only
    finish_reason: str | None
    completion_tokens: int | None
    prompt_tokens: int | None
    attempt: int
    truncated: bool  # still truncated after the one regeneration
    reasoning_stripped: bool = False
    seed: int | None = None


# ------------------------------------------------------- (de)serialisation

T = TypeVar("T")


def to_dict(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: to_dict(getattr(obj, f.name)) for f in dataclasses.fields(obj)}
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, list):
        return [to_dict(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj


_NESTED = {
    (Item, "steps"): Step,
    (NeutralConversation, "events"): Event,
    (RenderedRequest, "sampling"): Sampling,
}
_ENUMS = {
    "type": EventType,
    "branch": Branch,
    "frame": Frame,
    "history": History,
    "remedy": Remedy,
    "channel": Channel,
    "direction": Direction,
    "policy": Policy,
}


def from_dict(cls: type[T], d: dict[str, Any]) -> T:
    names = {f.name for f in dataclasses.fields(cls)}  # type: ignore[arg-type]
    unknown = set(d) - names
    if unknown:
        raise ValueError(f"{cls.__name__}: unknown fields {sorted(unknown)}")
    kwargs: dict[str, Any] = {}
    for k, v in d.items():
        sub = _NESTED.get((cls, k))
        if sub is not None and v is not None:
            v = [from_dict(sub, x) for x in v] if isinstance(v, list) else from_dict(sub, v)
        elif k in _ENUMS and v is not None and cls in (Event, ConditionKey):
            v = _ENUMS[k](v)
        kwargs[k] = v
    return cls(**kwargs)
