"""Generation backends. MockBackend and VLLMBackend share one interface (handbook §6.4).

All tests use MockBackend. VLLMBackend is only exercised on the GPU box.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from pu.io import sha256_text


@dataclass
class GenRequest:
    prompt: str
    temperature: float
    max_tokens: int
    seed: int


@dataclass
class GenResult:
    text: str
    finish_reason: str | None  # "stop" | "length" | ...
    completion_tokens: int | None
    prompt_tokens: int | None = None


class Backend(Protocol):
    name: str
    model_id: str
    weights_hash: str | None
    engine_version: str | None

    def generate(self, requests: list[GenRequest]) -> list[GenResult]: ...


_THINK = re.compile(r"<think>.*?</think>\s*", re.DOTALL)


def strip_reasoning(text: str) -> tuple[str, bool]:
    """Keep visible text only. Thinking should already be off; this is a guard.

    An unterminated <think> block (budget exhausted while thinking) leaves no visible text.
    """
    stripped = False
    if "<think>" in text:
        stripped = True
        text = _THINK.sub("", text)
        if "<think>" in text:
            text = text.split("<think>", 1)[0]
    elif "</think>" in text:  # some templates open the block in the prompt
        stripped = True
        text = text.split("</think>", 1)[1]
    return text.strip(), stripped


class MockCrash(RuntimeError):
    pass


Responder = Callable[[GenRequest], GenResult]


def default_responder(req: GenRequest) -> GenResult:
    """Deterministic fake output. Prompts containing [[TRUNCATE]] are cut off when the budget
    is below 2048 tokens; [[TRUNCATE_ALWAYS]] is cut off at any budget."""
    tag = sha256_text(f"{req.prompt}|{req.seed}")[:8]
    if "[[TRUNCATE_ALWAYS]]" in req.prompt or (
        "[[TRUNCATE]]" in req.prompt and req.max_tokens < 2048
    ):
        return GenResult(
            text=f"Let me work through this carefully {tag} and",
            finish_reason="length",
            completion_tokens=req.max_tokens,
            prompt_tokens=len(req.prompt) // 4,
        )
    return GenResult(
        text=f"MOCK reply {tag}. Here is a hint: start with step one.",
        finish_reason="stop",
        completion_tokens=12,
        prompt_tokens=len(req.prompt) // 4,
    )


class MockBackend:
    name = "mock"
    engine_version = "mock-0"

    def __init__(
        self,
        model_id: str = "mock-model",
        responder: Responder = default_responder,
        crash_after_requests: int | None = None,
    ):
        self.model_id = model_id
        self.weights_hash = "mock-weights"
        self.responder = responder
        self.crash_after_requests = crash_after_requests
        self.n_requests = 0
        self.calls: list[list[GenRequest]] = []

    def generate(self, requests: list[GenRequest]) -> list[GenResult]:
        if (
            self.crash_after_requests is not None
            and self.n_requests + len(requests) > self.crash_after_requests
        ):
            raise MockCrash(f"simulated crash after {self.n_requests} requests")
        self.calls.append(list(requests))
        self.n_requests += len(requests)
        return [self.responder(r) for r in requests]


class VLLMBackend:
    """vLLM offline engine (pinned vllm==0.31.0). Prompts are pre-rendered strings, so we
    tokenize without adding special tokens again (the chat template already contains BOS)."""

    name = "vllm"

    def __init__(
        self,
        model_id: str,
        model_path: str,
        revision: str | None = None,
        weights_hash: str | None = None,
        tensor_parallel_size: int = 1,
        dtype: str = "bfloat16",
        quantization: str | None = None,
        max_model_len: int = 8192,
        gpu_memory_utilization: float = 0.90,
        engine_seed: int = 0,
    ):
        import vllm  # imported lazily: only installed on the GPU box

        self._vllm = vllm
        self.model_id = model_id
        self.weights_hash = weights_hash
        self.engine_version = vllm.__version__
        self.llm = vllm.LLM(
            model=model_path,
            revision=revision,
            tensor_parallel_size=tensor_parallel_size,
            dtype=dtype,
            quantization=quantization,
            max_model_len=max_model_len,
            gpu_memory_utilization=gpu_memory_utilization,
            seed=engine_seed,
            enable_prefix_caching=True,
        )

    def generate(self, requests: list[GenRequest]) -> list[GenResult]:
        params = [
            self._vllm.SamplingParams(
                temperature=r.temperature, max_tokens=r.max_tokens, seed=r.seed
            )
            for r in requests
        ]
        outs = self.llm.generate(
            [r.prompt for r in requests],
            params,
            use_tqdm=False,
            tokenization_kwargs={"add_special_tokens": False},
        )
        results = []
        for o in outs:
            c = o.outputs[0]
            results.append(
                GenResult(
                    text=c.text,
                    finish_reason=c.finish_reason,
                    completion_tokens=len(c.token_ids),
                    prompt_tokens=len(o.prompt_token_ids or []),
                )
            )
        return results
