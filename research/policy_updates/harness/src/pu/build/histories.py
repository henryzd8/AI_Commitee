"""History generation and loading (handbook §6.3, design §4.2).

For each probe item and model, two 4-turn histories are generated: R-hist under a plain R prompt
and P-hist under a plain P prompt (C1-style system, no channel frame). Turns are sequential: turn
i's prompt contains turns 1..i-1 of the same history. Turns are batched across items.

Rules: a turn that hits the token cap is regenerated once at double budget; if still truncated it
is kept and flagged. Visible text only. No filtering on policy behaviour (design §4.2).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from pu.build.conversation import HistoryRecord, history_turn_events
from pu.config import SamplingConfig
from pu.io import append_jsonl, derive_seed, read_jsonl
from pu.render.base import Renderer
from pu.run.backend import Backend, GenRequest, strip_reasoning
from pu.schemas import HIST_P, HIST_R, HistoryTurn, Item, NeutralConversation, Policy, from_dict
from pu.texts.library import TextLibrary

HISTS = ((HIST_R, Policy.R), (HIST_P, Policy.P))


def history_seed(model_id: str, item_id: str, hist: str, turn: int, attempt: int) -> int:
    return derive_seed("hist", model_id, item_id, hist, turn, attempt)


def load_turns(path: str | Path) -> list[HistoryTurn]:
    return [from_dict(HistoryTurn, d) for d in read_jsonl(path)]


def load_histories(path: str | Path) -> dict[tuple[str, str], dict[str, HistoryRecord]]:
    """(model_id, probe_item_id) -> {"R-hist": record, "P-hist": record}.

    Complete (4-turn) histories only.
    """
    grouped: dict[tuple[str, str, str], dict[int, HistoryTurn]] = defaultdict(dict)
    for t in load_turns(path):
        grouped[(t.model_id, t.probe_item_id, t.hist)][t.turn] = t  # last write wins
    out: dict[tuple[str, str], dict[str, HistoryRecord]] = defaultdict(dict)
    for (m, item, hist), turns in grouped.items():
        if sorted(turns) == [1, 2, 3, 4]:
            out[(m, item)][hist] = HistoryRecord(m, item, hist, list(turns.values()))
    return dict(out)


@dataclass
class HistorySummary:
    turns_generated: int = 0
    regenerated: int = 0
    still_truncated: int = 0
    reasoning_stripped: int = 0


def generate_histories(
    backend: Backend,
    renderer: Renderer,
    texts: TextLibrary,
    probe_items: list[Item],
    history_items: dict[str, Item],
    out_path: str | Path,
    sampling: SamplingConfig,
    batch_size: int = 256,
) -> HistorySummary:
    out_path = Path(out_path)
    model_id = backend.model_id
    summary = HistorySummary()
    done: dict[tuple[str, str], dict[int, HistoryTurn]] = defaultdict(dict)
    for t in load_turns(out_path):
        if t.model_id == model_id:
            done[(t.probe_item_id, t.hist)][t.turn] = t

    for turn in (1, 2, 3, 4):
        jobs = []  # (item, hist, gen_request)
        for item in probe_items:
            hitems = [history_items[h] for h in item.history_item_ids]
            if len(hitems) != 4:
                raise ValueError(f"{item.item_id} needs exactly 4 history items")
            for hist, policy in HISTS:
                have = done[(item.item_id, hist)]
                if turn in have or any(k not in have for k in range(1, turn)):
                    continue
                prev = [have[k].text for k in range(1, turn)]
                conv = NeutralConversation(
                    conv_id=f"hist:{item.item_id}:{hist}:{turn}",
                    model_id=model_id,
                    events=history_turn_events(texts, policy, hitems, prev),
                )
                prompt, _ = renderer.render(conv)
                seed = history_seed(model_id, item.item_id, hist, turn, 1)
                jobs.append(
                    (
                        item,
                        hist,
                        GenRequest(prompt, sampling.temperature, sampling.max_tokens, seed),
                    )
                )

        for i in range(0, len(jobs), batch_size):
            chunk = jobs[i : i + batch_size]
            results = backend.generate([g for _, _, g in chunk])
            attempts = [1] * len(chunk)
            seeds = [g.seed for _, _, g in chunk]
            # one regeneration at double budget for truncated turns
            redo = [k for k, r in enumerate(results) if r.finish_reason == "length"]
            if redo:
                regen = [
                    GenRequest(
                        chunk[k][2].prompt,
                        sampling.temperature,
                        sampling.retry_max_tokens,
                        history_seed(model_id, chunk[k][0].item_id, chunk[k][1], turn, 2),
                    )
                    for k in redo
                ]
                for k, res in zip(redo, backend.generate(regen), strict=True):
                    results[k] = res
                    attempts[k] = 2
                    seeds[k] = regen[redo.index(k)].seed
                summary.regenerated += len(redo)
            recs = []
            for (item, hist, _), res, att, seed in zip(
                chunk, results, attempts, seeds, strict=True
            ):
                visible, stripped = strip_reasoning(res.text)
                rec = HistoryTurn(
                    model_id=model_id,
                    probe_item_id=item.item_id,
                    hist=hist,
                    turn=turn,
                    text=visible,
                    finish_reason=res.finish_reason,
                    completion_tokens=res.completion_tokens,
                    prompt_tokens=res.prompt_tokens,
                    attempt=att,
                    truncated=res.finish_reason == "length",
                    reasoning_stripped=stripped,
                    seed=seed,
                )
                recs.append(rec)
                done[(item.item_id, hist)][turn] = rec
                summary.still_truncated += rec.truncated
                summary.reasoning_stripped += stripped
            append_jsonl(out_path, recs)
            summary.turns_generated += len(recs)
    return summary
