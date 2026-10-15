"""Renderer interface. The real renderer (chat templates, support matrix, diff check) is Task 2's.

Task 3 needs only the interface: NeutralConversation -> exact prompt string. `PlainRenderer`
is a deterministic stand-in for tests and the mock end-to-end run; it is NOT used for real runs.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

from pu.config import SamplingConfig
from pu.io import derive_seed, read_jsonl, sha256_text, write_jsonl_atomic
from pu.schemas import (
    EventType,
    NeutralConversation,
    RenderedRequest,
    Sampling,
    from_dict,
)


class Renderer(Protocol):
    name: str

    def render(self, conv: NeutralConversation) -> tuple[str, int | None]:
        """Return (prompt string after the model's chat template, prompt token count)."""
        ...


class PlainRenderer:
    """Test-only renderer. Approximates tokens as chars/4."""

    name = "plain-test-renderer"

    def render(self, conv: NeutralConversation) -> tuple[str, int | None]:
        parts = []
        for e in conv.events:
            if e.type in (EventType.TOOL_CALL,):
                body = json.dumps({"name": e.name, "args": e.args}, sort_keys=True)
            elif e.type == EventType.TOOL_RESULT:
                body = json.dumps(e.content, sort_keys=True)
            else:
                body = e.text or ""
            parts.append(f"<|{e.type.value}|>\n{body}")
        parts.append("<|assistant|>\n")
        prompt = "\n".join(parts)
        return prompt, max(1, len(prompt) // 4)


def plain_factory(model_spec=None, texts=None) -> PlainRenderer:
    """Factory used with `pu render --renderer pu.render.base:plain_factory` (tests only)."""
    return PlainRenderer()


def request_seed(request_id: str, attempt: int = 1) -> int:
    return derive_seed(request_id, attempt)


def render_conversations(
    convs: Iterable[NeutralConversation],
    renderer: Renderer,
    sampling: SamplingConfig,
    text_lib_hash: str | None,
) -> list[RenderedRequest]:
    out = []
    for c in convs:
        prompt, ntok = renderer.render(c)
        out.append(
            RenderedRequest(
                request_id=c.conv_id,
                model_id=c.model_id,
                prompt=prompt,
                prompt_tokens=ntok,
                sampling=Sampling(
                    temperature=sampling.temperature,
                    max_tokens=sampling.max_tokens,
                    seed=request_seed(c.conv_id, 1),
                ),
                text_lib_hash=text_lib_hash,
                render_hash=sha256_text(f"{renderer.name}\n{prompt}"),
            )
        )
    return out


def render_file(
    convs_path: str | Path,
    out_path: str | Path,
    renderer: Renderer,
    sampling: SamplingConfig,
    text_lib_hash: str | None,
) -> int:
    convs = [from_dict(NeutralConversation, d) for d in read_jsonl(convs_path)]
    reqs = render_conversations(convs, renderer, sampling, text_lib_hash)
    reqs.sort(key=lambda r: r.request_id)
    return write_jsonl_atomic(out_path, reqs)
