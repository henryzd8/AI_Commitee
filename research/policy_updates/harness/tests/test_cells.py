from collections import Counter

from pu.build.cells import (
    PRIMARY,
    descriptive_cells,
    manip_cells,
    pilot_cells,
    primary_cells,
    recognition_cells,
    screen_cells,
)
from pu.build.requests import balanced_subset, plan_cells
from pu.schemas import Branch, Channel, Frame, History, Remedy, Split

PRIM = [Channel.C3, Channel.C4]


def test_primary_cells_match_design():
    assert PRIMARY == {
        1: (Frame.SWITCH, History.OLD_SELF, Remedy.R0),
        2: (Frame.NOOP, History.NEW_SELF, Remedy.R0),
        3: (Frame.SWITCH, History.NEW_SELF, Remedy.R0),
        4: (Frame.SWITCH, History.OLD_SELF, Remedy.R3),
        5: (Frame.NOOP, History.NEW_SELF, Remedy.R3),
    }
    cells = primary_cells(PRIM)
    assert len(cells) == 2 * 2 * 5
    assert len({c.name for c in cells}) == len(cells)


def test_other_catalogs():
    assert len(screen_cells()) == 2
    assert len(manip_cells()) == 8
    assert len(pilot_cells(PRIM)) == 8
    assert all(c.frame != Frame.STATIC for c in pilot_cells(PRIM))
    rec = recognition_cells(PRIM, samples=3, calibration=True)
    assert len(rec) == 8 and all(c.branch == Branch.RECOG and c.samples == 3 for c in rec)
    assert len(descriptive_cells([Channel.C1, Channel.C2])) == 8


def test_confirm_plan_counts(cfg, full_confirm_items):
    probes, _ = full_confirm_items
    plan = plan_cells(Split.CONFIRM, probes, cfg)
    counts = Counter()
    for spec, _ in plan:
        kind = spec.name.split("-")[0].rstrip("0123456789")
        counts[kind] += spec.samples
    assert counts["cell"] == 600 * 20  # 12k primary calls per model (design §4.6)
    assert counts["recog"] == 150 * 2 * 3  # 0.9k recognition (design §4.6), split channels
    assert counts["recogcal"] == 150 * 2 * 3  # calibration (lead to confirm)
    assert counts["desc"] == 300 * 2 * 2 * 2  # 2.4k descriptive (C1 + C2)


def test_other_plan_counts(cfg, small_items):
    probes, _ = small_items
    n = len(probes)
    assert len(plan_cells(Split.SCREEN, probes, cfg)) == 2 * n
    assert len(plan_cells(Split.MANIP, probes, cfg)) == 8 * n
    assert len(plan_cells(Split.EXPLORE, probes, cfg)) == 10 * n


def test_balanced_subset_is_balanced_and_deterministic(full_confirm_items):
    probes, _ = full_confirm_items
    a = balanced_subset(probes, 150, "x")
    b = balanced_subset(probes, 150, "x")
    assert [i.item_id for i in a] == [i.item_id for i in b]
    per_fam = Counter(i.family_id for i in a)
    assert max(per_fam.values()) - min(per_fam.values()) <= 1
    assert len(set(i.item_id for i in a)) == 150
    c = balanced_subset(probes, 150, "y")
    assert [i.item_id for i in c] != [i.item_id for i in a]
