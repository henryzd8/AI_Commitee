import pytest

from pu.schemas import (
    HIST_P,
    HIST_R,
    Branch,
    Channel,
    ConditionKey,
    Direction,
    Event,
    EventType,
    Frame,
    History,
    Item,
    NeutralConversation,
    Policy,
    Remedy,
    RenderedRequest,
    ResponseRecord,
    Sampling,
    Step,
    from_dict,
    history_source,
    policies_for,
    to_dict,
    violation,
)


def test_policies_for():
    assert policies_for(Direction.LOOSEN) == (Policy.R, Policy.P)
    assert policies_for(Direction.TIGHTEN) == (Policy.P, Policy.R)


@pytest.mark.parametrize(
    "direction,history,expected",
    [
        (Direction.LOOSEN, History.OLD_SELF, HIST_R),
        (Direction.LOOSEN, History.NEW_SELF, HIST_P),
        (Direction.TIGHTEN, History.OLD_SELF, HIST_P),
        (Direction.TIGHTEN, History.NEW_SELF, HIST_R),
    ],
)
def test_history_source_matches_design_table(direction, history, expected):
    assert history_source(direction, history) == expected


def test_history_source_none_raises():
    with pytest.raises(ValueError):
        history_source(Direction.LOOSEN, History.NONE)


def test_violation_mapping():
    assert violation(Direction.TIGHTEN, given=True) is True
    assert violation(Direction.TIGHTEN, given=False) is False
    assert violation(Direction.LOOSEN, given=False) is True
    assert violation(Direction.LOOSEN, given=True) is False


def _roundtrip(obj):
    d = to_dict(obj)
    return from_dict(type(obj), d)


def test_roundtrips():
    item = Item(
        "F01-x-0",
        "F01",
        "probe",
        "explore",
        1,
        0,
        "text",
        [Step("a", 3)],
        120,
        paraphrase_id=2,
        history_item_ids=["h1"],
    )
    assert _roundtrip(item) == item
    conv = NeutralConversation(
        "id",
        "m",
        [
            Event(EventType.SYSTEM, text="s"),
            Event(EventType.TOOL_RESULT, name="t", content={"p": 1}),
        ],
    )
    assert _roundtrip(conv) == conv
    req = RenderedRequest("id", "m", "prompt", Sampling(0.7, 1024, 5), prompt_tokens=3)
    assert _roundtrip(req) == req
    key = ConditionKey(
        "id",
        "m",
        "confirm",
        Branch.PROBE,
        Frame.SWITCH,
        History.OLD_SELF,
        Remedy.R0,
        Channel.C3,
        "F01-x-0",
        0,
        Direction.LOOSEN,
        None,
        "cell1",
    )
    assert _roundtrip(key) == key
    resp = ResponseRecord("id", "m", "t", "stop", 3, 1)
    assert _roundtrip(resp) == resp


def test_unknown_field_rejected():
    with pytest.raises(ValueError):
        from_dict(Sampling, {"temperature": 0.7, "max_tokens": 1, "seed": 1, "extra": 1})
