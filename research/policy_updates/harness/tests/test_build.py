import json
import uuid

import pytest

from pu.build.ids import load_or_create_salt, new_salt, opaque_id
from pu.build.requests import MissingHistories, UnknownSupport, build_split
from pu.config import ModelSpec
from pu.io import read_jsonl, sha256_file
from pu.schemas import Split
from pu.testing.fakes import make_histories


def test_opaque_ids():
    s1, s2 = new_salt(), new_salt()
    a = opaque_id(s1, "confirm", "m1", "cell1-loosen-C3", "F01-confirm-0000", 0)
    assert a == opaque_id(s1, "confirm", "m1", "cell1-loosen-C3", "F01-confirm-0000", 0)
    assert a != opaque_id(s2, "confirm", "m1", "cell1-loosen-C3", "F01-confirm-0000", 0)
    assert a != opaque_id(s1, "confirm", "m1", "cell2-loosen-C3", "F01-confirm-0000", 0)
    uuid.UUID(a)
    assert "cell" not in a and "loosen" not in a


def test_salt_persisted(tmp_path):
    s = load_or_create_salt(tmp_path)
    assert load_or_create_salt(tmp_path) == s
    assert oct((tmp_path / "salt.txt").stat().st_mode)[-3:] == "600"


@pytest.fixture
def built(tmp_path, small_items, small_histories, models, texts, cfg):
    probes, hitems = small_items
    salt = new_salt()
    res = build_split(
        Split.CONFIRM,
        probes,
        hitems,
        small_histories,
        models,
        texts,
        cfg,
        salt,
        tmp_path / "out",
        tmp_path / "keys",
    )
    return res, tmp_path, salt


def test_build_outputs(built, small_items):
    res, tmp, _ = built
    probes, _ = small_items
    convs_a = list(read_jsonl(tmp / "out/confirm/mA.conversations.jsonl"))
    convs_b = list(read_jsonl(tmp / "out/confirm/mB.conversations.jsonl"))
    keys = list(read_jsonl(tmp / "keys/confirm.condition_key.jsonl"))
    metas = list(read_jsonl(tmp / "out/confirm/recog_meta.jsonl"))
    assert len(keys) == len(convs_a) + len(convs_b) == res.n_conversations
    ids = [c["conv_id"] for c in convs_a + convs_b]
    assert len(set(ids)) == len(ids)
    assert [c["conv_id"] for c in convs_a] == sorted(c["conv_id"] for c in convs_a)
    # mB lacks C2 -> its C2 descriptive cells are skipped and logged
    assert res.per_model["mA"] > res.per_model["mB"]
    assert res.skipped and all(k.startswith("mB:C2") for k in res.skipped)
    # every recognition request has meta; meta has no condition labels
    n_recog = sum(1 for k in keys if k["branch"] == "recog")
    assert n_recog == len(metas) and set(metas[0]) == {"request_id", "polarity", "yes_option"}
    # conversations carry no condition labels
    blob = json.dumps(convs_a)
    for label in ("SWITCH", "NOOP", "OLD-SELF", "NEW-SELF", "R3", "loosen", "tighten", "cell1"):
        assert label not in blob
    manifest = json.loads((tmp / "out/confirm/build_manifest.json").read_text())
    assert manifest["n_conversations"] == res.n_conversations
    assert manifest["text_lib"]["version"] == "v0-draft"


def test_build_is_deterministic(built, small_items, small_histories, models, texts, cfg):
    res, tmp, salt = built
    probes, hitems = small_items
    before = sha256_file(tmp / "out/confirm/mA.conversations.jsonl")
    build_split(
        Split.CONFIRM,
        probes,
        hitems,
        small_histories,
        models,
        texts,
        cfg,
        salt,
        tmp / "out",
        tmp / "keys",
    )
    assert sha256_file(tmp / "out/confirm/mA.conversations.jsonl") == before


def test_missing_histories_raise(tmp_path, small_items, models, texts, cfg):
    probes, hitems = small_items
    partial = make_histories(["mA", "mB"], probes[:-1])
    with pytest.raises(MissingHistories):
        build_split(
            Split.CONFIRM,
            probes,
            hitems,
            partial,
            models,
            texts,
            cfg,
            new_salt(),
            tmp_path / "o",
            tmp_path / "k",
        )
    assert not (tmp_path / "o/confirm/mA.conversations.jsonl").exists()


def test_unknown_support_raises(tmp_path, small_items, small_histories, texts, cfg):
    probes, hitems = small_items
    unknown = [
        ModelSpec(id="mA", hf_repo="x", support={"C1": None, "C2": None, "C3": True, "C4": True})
    ]
    with pytest.raises(UnknownSupport):
        build_split(
            Split.CONFIRM,
            probes,
            hitems,
            small_histories,
            unknown,
            texts,
            cfg,
            new_salt(),
            tmp_path / "o",
            tmp_path / "k",
        )
    res = build_split(
        Split.CONFIRM,
        probes,
        hitems,
        small_histories,
        unknown,
        texts,
        cfg,
        new_salt(),
        tmp_path / "o",
        tmp_path / "k",
        allow_unknown_support=True,
    )
    assert res.n_conversations > 0


def test_screen_and_manip_need_no_histories(tmp_path, small_items, models, texts, cfg):
    probes, _ = small_items
    for split, per_item in ((Split.SCREEN, 2), (Split.MANIP, 8)):
        res = build_split(
            split, probes, {}, {}, models, texts, cfg, new_salt(), tmp_path / "o", tmp_path / "k"
        )
        assert res.per_model["mA"] == per_item * len(probes)
        if split == Split.MANIP:
            assert res.per_model["mB"] == 6 * len(probes)  # no C2
