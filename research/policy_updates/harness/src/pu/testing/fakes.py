"""Fake items and histories for tests, the mock end-to-end run and the GPU-hour estimate.

These are NOT study items. Real items come from Task 1's generator with the same schema.
"""

from __future__ import annotations

import random

from pu.build.conversation import HistoryRecord
from pu.schemas import HIST_P, HIST_R, HistoryTurn, Item, Step


def _problem(rng: random.Random, family: str) -> tuple[str, list[Step], int]:
    # ranges keep the answer in [100, 9999]: max 40*20*6 + 499 = 5299
    a, b, c = rng.randint(12, 40), rng.randint(6, 20), rng.randint(2, 6)
    total = a * b
    final = total * c + rng.randint(101, 499)
    assert 100 <= final <= 9999 and final not in (a, b, c, total, total * c)
    extra = final - total * c
    text = (
        f"[{family}] A shop packs {a} boxes with {b} items each, sells each item {c} times "
        f"over the season, and adds {extra} special orders. How many sales in total?"
    )
    return text, [Step("items", total), Step("sales", total * c)], final


def make_items(
    split: str,
    n_families: int = 4,
    items_per_family: int = 3,
    seed: int = 7,
    heldout_families: int = 0,
    text_padding: int = 0,
) -> tuple[list[Item], dict[str, Item]]:
    """Return (probe items, history items by id). Each probe family Fk has history family Hk."""
    rng = random.Random(seed)
    probes: list[Item] = []
    hist: dict[str, Item] = {}
    for f in range(1, n_families + 1):
        fid, hid = f"F{f:02d}", f"H{f:02d}"
        for i in range(items_per_family):
            text, steps, ans = _problem(rng, fid)
            hids = []
            for j in range(4):
                htext, hsteps, hans = _problem(rng, hid)
                h = Item(
                    item_id=f"{hid}-{split}-{i:04d}-{j}",
                    family_id=hid,
                    role="history",
                    split=split,
                    seed=seed,
                    index=i * 4 + j,
                    text=htext + " " * text_padding,
                    steps=hsteps,
                    final_answer=hans,
                )
                hist[h.item_id] = h
                hids.append(h.item_id)
            probes.append(
                Item(
                    item_id=f"{fid}-{split}-{i:04d}",
                    family_id=fid,
                    role="probe",
                    split=split,
                    seed=seed,
                    index=i,
                    text=text + " " * text_padding,
                    steps=steps,
                    final_answer=ans,
                    paraphrase_id=(f + i) % 5,
                    history_item_ids=hids,
                    heldout_family=f > n_families - heldout_families,
                )
            )
    return probes, hist


def make_histories(
    model_ids: list[str], probes: list[Item], chars_per_turn: int = 200, marker: str = ""
) -> dict[tuple[str, str], dict[str, HistoryRecord]]:
    out: dict[tuple[str, str], dict[str, HistoryRecord]] = {}
    for m in model_ids:
        for it in probes:
            recs = {}
            for hist in (HIST_R, HIST_P):
                turns = []
                for t in range(1, 5):
                    body = f"{marker}[{m}|{it.item_id}|{hist}|turn{t}] "
                    body = (body + "x" * chars_per_turn)[: max(len(body), chars_per_turn)]
                    turns.append(
                        HistoryTurn(
                            model_id=m,
                            probe_item_id=it.item_id,
                            hist=hist,
                            turn=t,
                            text=body,
                            finish_reason="stop",
                            completion_tokens=len(body) // 4,
                            prompt_tokens=None,
                            attempt=1,
                            truncated=False,
                        )
                    )
                recs[hist] = HistoryRecord(m, it.item_id, hist, turns)
            out[(m, it.item_id)] = recs
    return out
