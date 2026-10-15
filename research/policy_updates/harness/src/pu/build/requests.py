"""Plan and build all conversations for a split (handbook §6.1-6.2).

Outputs (per split):
  <out>/<split>/<model>.conversations.jsonl   neutral conversations, sorted by opaque id
  <out>/<split>/recog_meta.jsonl               polarity / option order (not blinded)
  <out>/<split>/build_manifest.json            counts, hashes, skipped channels
  <keys>/<split>.condition_key.jsonl           BLINDED: request_id -> condition
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pu.build.cells import (
    DIRECTIONS,
    CellSpec,
    descriptive_cells,
    explore_static_cells,
    manip_cells,
    pilot_cells,
    primary_cells,
    recognition_cells,
    screen_cells,
)
from pu.build.conversation import HistoryRecord, RecogDraw, build_events
from pu.build.ids import opaque_id
from pu.config import ModelSpec, RunConfig
from pu.io import derive_seed, sha256_text, write_json_atomic, write_jsonl_atomic
from pu.run.manifest import now_iso
from pu.schemas import (
    SCHEMA_VERSION,
    ConditionKey,
    Item,
    NeutralConversation,
    RecogMeta,
    Split,
    history_source,
)
from pu.texts.library import TextLibrary


class MissingHistories(RuntimeError):
    pass


class UnknownSupport(RuntimeError):
    pass


def balanced_subset(items: list[Item], n: int, label: str) -> list[Item]:
    """Deterministic subset of n items, balanced across families (round-robin over families in a
    hashed order, items within a family in hashed order). Uses ids only, never outcomes."""
    if n >= len(items):
        return sorted(items, key=lambda it: sha256_text(f"{label}|{it.item_id}"))
    by_fam: dict[str, list[Item]] = defaultdict(list)
    for it in items:
        by_fam[it.family_id].append(it)
    fams = sorted(by_fam, key=lambda f: sha256_text(f"{label}|fam|{f}"))
    queues = {
        f: sorted(by_fam[f], key=lambda it: sha256_text(f"{label}|{it.item_id}")) for f in fams
    }
    out: list[Item] = []
    while len(out) < n:
        progressed = False
        for f in fams:
            if queues[f] and len(out) < n:
                out.append(queues[f].pop(0))
                progressed = True
        if not progressed:
            break
    return out


def plan_cells(split: Split, items: list[Item], cfg: RunConfig) -> list[tuple[CellSpec, Item]]:
    plan: list[tuple[CellSpec, Item]] = []
    if split == Split.SCREEN:
        plan = [(c, it) for it in items for c in screen_cells()]
    elif split == Split.MANIP:
        plan = [(c, it) for it in items for c in manip_cells()]
    elif split in (Split.EXPLORE, Split.CALIB):
        cells = pilot_cells(cfg.primary_channels) + explore_static_cells()
        plan = [(c, it) for it in items for c in cells]
    elif split == Split.CONFIRM:
        plan = [(c, it) for it in items for c in primary_cells(cfg.primary_channels)]
        rc = cfg.recognition
        rcells = recognition_cells(cfg.primary_channels, rc.samples, rc.calibration)
        for d in DIRECTIONS:
            subset = balanced_subset(items, rc.items_per_direction, f"recog-{d.value}")
            for k, it in enumerate(subset):
                if rc.channel_assignment == "split":
                    chans = [cfg.primary_channels[k % len(cfg.primary_channels)]]
                else:
                    chans = list(cfg.primary_channels)
                plan += [(c, it) for c in rcells if c.direction == d and c.channel in chans]
        dc = cfg.descriptive
        dcells = descriptive_cells(dc.channels)
        for d in DIRECTIONS:
            subset = balanced_subset(items, dc.items_per_direction, f"desc-{d.value}")
            plan += [(c, it) for it in subset for c in dcells if c.direction == d]
    else:
        raise ValueError(split)
    return plan


@dataclass
class BuildResult:
    n_conversations: int = 0
    per_model: dict[str, int] = field(default_factory=dict)
    per_cell: dict[str, int] = field(default_factory=dict)
    skipped: dict[str, int] = field(default_factory=dict)
    outputs: dict[str, str] = field(default_factory=dict)


def recog_draw(request_id: str) -> RecogDraw:
    polarity = "allowed" if derive_seed("recog-polarity", request_id) % 2 == 0 else "prohibited"
    yes_option = "A" if derive_seed("recog-order", request_id) % 2 == 0 else "B"
    return RecogDraw(polarity, yes_option)


def build_split(
    split: Split,
    items: list[Item],
    history_items: dict[str, Item],
    histories: dict[tuple[str, str], dict[str, HistoryRecord]],
    models: list[ModelSpec],
    texts: TextLibrary,
    cfg: RunConfig,
    salt: str,
    out_dir: str | Path,
    keys_dir: str | Path,
    allow_unknown_support: bool = False,
) -> BuildResult:
    out_dir, keys_dir = Path(out_dir) / split.value, Path(keys_dir)
    plan = plan_cells(split, items, cfg)
    result = BuildResult()
    keys: list[ConditionKey] = []
    metas: list[RecogMeta] = []
    missing: set[tuple[str, str]] = set()
    unknown: set[tuple[str, str]] = set()
    per_cell: Counter[str] = Counter()
    by_model: dict[str, list[NeutralConversation]] = {}

    for m in models:
        convs: list[NeutralConversation] = []
        for spec, item in plan:
            ok = m.supports(spec.channel)
            if ok is False:
                result.skipped[f"{m.id}:{spec.channel.value}"] = (
                    result.skipped.get(f"{m.id}:{spec.channel.value}", 0) + spec.samples
                )
                continue
            if ok is None and not allow_unknown_support:
                unknown.add((m.id, spec.channel.value))
                continue
            hist = hitems = None
            if spec.needs_history:
                rec = histories.get((m.id, item.item_id), {})
                src = history_source(spec.direction, spec.history)  # type: ignore[arg-type]
                if src not in rec:
                    missing.add((m.id, item.item_id))
                    continue
                hist = rec[src]
                hitems = [history_items[h] for h in item.history_item_ids]
            for s in range(spec.samples):
                rid = opaque_id(salt, split.value, m.id, spec.name, item.item_id, s)
                draw = recog_draw(rid) if spec.branch.value == "recog" else None
                events = build_events(spec, item, texts, cfg.c4_clock, hist, hitems, draw)
                convs.append(NeutralConversation(conv_id=rid, model_id=m.id, events=events))
                keys.append(
                    ConditionKey(
                        request_id=rid,
                        model_id=m.id,
                        split=split.value,
                        branch=spec.branch,
                        frame=spec.frame,
                        history=spec.history,
                        remedy=spec.remedy,
                        channel=spec.channel,
                        item_id=item.item_id,
                        sample_idx=s,
                        direction=spec.direction,
                        policy=spec.policy,
                        cell=spec.name,
                    )
                )
                if draw:
                    metas.append(RecogMeta(rid, draw.polarity, draw.yes_option))
                per_cell[spec.name] += 1
        convs.sort(key=lambda c: c.conv_id)
        by_model[m.id] = convs
        result.per_model[m.id] = len(convs)
        result.n_conversations += len(convs)

    if unknown:
        raise UnknownSupport(
            f"channel support unknown for {sorted(unknown)}; Task 2 must fill models.yaml "
            "support, or pass allow_unknown_support=True (tests only)"
        )
    if missing:
        sample = sorted(missing)[:5]
        raise MissingHistories(
            f"{len(missing)} (model, item) pairs lack complete histories, e.g. {sample}"
        )

    for model_id, convs in by_model.items():
        path = out_dir / f"{model_id}.conversations.jsonl"
        write_jsonl_atomic(path, convs)
        result.outputs[model_id] = str(path)
    keys.sort(key=lambda k: k.request_id)
    write_jsonl_atomic(keys_dir / f"{split.value}.condition_key.jsonl", keys)
    metas.sort(key=lambda r: r.request_id)
    write_jsonl_atomic(out_dir / "recog_meta.jsonl", metas)
    result.per_cell = dict(sorted(per_cell.items()))
    manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "built": now_iso(),
        "split": split.value,
        "text_lib": {"path": str(texts.path), "version": texts.version, "sha256": texts.hash},
        "models": [m.id for m in models],
        "n_conversations": result.n_conversations,
        "per_model": result.per_model,
        "per_cell": result.per_cell,
        "skipped_unsupported": result.skipped,
        "primary_channels": [c.value for c in cfg.primary_channels],
        "c4_clock": vars(cfg.c4_clock),
        "note": "Condition keys are in keys/ (blinded analyst only).",
    }
    write_json_atomic(out_dir / "build_manifest.json", manifest)
    return result
