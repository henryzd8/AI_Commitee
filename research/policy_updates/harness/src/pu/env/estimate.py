"""Token-count-based GPU-hour estimate for the gate/pilot week and the confirmatory run.

Call counts come from the real cell planner (so they stay consistent with what the builder
produces). Prompt tokens are measured by rendering conversations built from fake items and
fake histories of the assumed length. Throughput figures are ASSUMPTIONS in configs/run.yaml
and must be replaced by measured numbers after the first real-model smoke test.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from pu.build.conversation import build_events, history_turn_events
from pu.build.requests import plan_cells, recog_draw
from pu.config import ModelSpec, RunConfig
from pu.render.base import PlainRenderer, Renderer
from pu.schemas import HIST_P, HIST_R, NeutralConversation, Policy, Split, history_source
from pu.testing.fakes import make_histories, make_items
from pu.texts.library import TextLibrary


@dataclass
class Line:
    model_id: str
    phase: str
    calls: int
    prompt_tokens: int
    completion_tokens: int
    gpu_hours: float


def _call_type(branch: str) -> str:
    return {"recog": "recog", "screen": "probe", "manip": "probe", "probe": "probe"}[branch]


def estimate(
    models: list[ModelSpec], cfg: RunConfig, texts: TextLibrary, renderer: Renderer | None = None
) -> list[Line]:
    est: dict[str, Any] = cfg.raw.get("estimate", {})
    splits: dict[str, Any] = cfg.raw.get("splits", {})
    comp = est.get("completion_tokens", {})
    hist_chars = int(comp.get("history_turn", 300)) * 4
    cache_hit = float(est.get("prefix_cache_hit", 0.3))
    trunc = float(est.get("truncation_rate", 0.05))
    thr = est.get("throughput", {})
    renderer = renderer or PlainRenderer()

    n_fam = int(splits.get("families", 40))
    sizes = {  # split -> (families, total probe items)
        Split.SCREEN: (n_fam, n_fam * int(splits.get("screen_items_per_family", 40))),
        Split.MANIP: (int(splits.get("shared_families", 32)), int(splits.get("manip_items", 100))),
        Split.EXPLORE: (
            int(splits.get("shared_families", 32)),
            int(splits.get("explore_items", 100)),
        ),
        Split.CONFIRM: (n_fam, int(splits.get("confirm_items", 600))),
    }
    phases = {
        Split.SCREEN: "W2 screen",
        Split.MANIP: "W3 manip",
        Split.EXPLORE: "W3 explore+pilot",
        Split.CONFIRM: "W6 confirmatory",
    }
    lines: list[Line] = []
    for m in models:
        t = thr.get(m.size_class) or thr.get("default")
        if not t:
            raise KeyError(f"no throughput assumption for size class {m.size_class}")
        for split, (nf, n_items) in sizes.items():
            items, hitems = make_items(
                split.value, n_families=nf, items_per_family=-(-n_items // nf)
            )
            items = items[:n_items]
            hist = make_histories([m.id], items, chars_per_turn=hist_chars)
            agg: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])  # calls, prompt, completion
            for spec, item in plan_cells(split, items, cfg):
                if m.supports(spec.channel) is False:
                    continue
                hrec = hitm = None
                if spec.needs_history:
                    hrec = hist[(m.id, item.item_id)][history_source(spec.direction, spec.history)]
                    hitm = [hitems[h] for h in item.history_item_ids]
                draw = recog_draw("est") if spec.branch.value == "recog" else None
                conv = NeutralConversation(
                    "est", m.id, build_events(spec, item, texts, cfg.c4_clock, hrec, hitm, draw)
                )
                _, ntok = renderer.render(conv)
                ct = _call_type(spec.branch.value)
                a = agg[ct]
                a[0] += spec.samples
                a[1] += (ntok or 0) * spec.samples
                a[2] += int(comp.get(ct, 350)) * spec.samples
            if split in (Split.EXPLORE, Split.CONFIRM):  # history generation for these items
                a = agg["history"]
                for item in items:
                    hitm = [hitems[h] for h in item.history_item_ids]
                    for _, pol in ((HIST_R, Policy.R), (HIST_P, Policy.P)):
                        for turn in range(1, 5):
                            prev = ["x" * hist_chars] * (turn - 1)
                            ev = history_turn_events(texts, pol, hitm, prev)
                            _, ntok = renderer.render(NeutralConversation("est", m.id, ev))
                            a[0] += 1
                            a[1] += ntok or 0
                            a[2] += int(comp.get("history_turn", 300))
            calls = sum(v[0] for v in agg.values())
            ptok = sum(v[1] for v in agg.values())
            ctok = sum(v[2] for v in agg.values())
            calls, ptok, ctok = (int(x * (1 + trunc)) for x in (calls, ptok, ctok))
            hours = (ptok * (1 - cache_hit) / t["prefill_tps"] + ctok / t["decode_tps"]) / 3600
            lines.append(Line(m.id, phases[split], calls, ptok, ctok, round(hours, 2)))
    return lines


def format_table(lines: list[Line]) -> str:
    rows = [
        "| model | phase | calls | prompt tokens | completion tokens | est. GPU-hours |",
        "|---|---|---|---|---|---|",
    ]
    for ln in lines:
        rows.append(
            f"| {ln.model_id} | {ln.phase} | {ln.calls:,} | {ln.prompt_tokens:,} | "
            f"{ln.completion_tokens:,} | {ln.gpu_hours} |"
        )
    total = sum(ln.gpu_hours for ln in lines)
    rows.append(
        f"| **total** | | {sum(ln.calls for ln in lines):,} | "
        f"{sum(ln.prompt_tokens for ln in lines):,} | "
        f"{sum(ln.completion_tokens for ln in lines):,} | **{round(total, 1)}** |"
    )
    return "\n".join(rows)
