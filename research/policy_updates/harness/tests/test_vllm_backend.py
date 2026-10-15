"""Checks VLLMBackend wiring against a fake `vllm` module (no GPU, no real vLLM)."""

import sys
import types

from pu.run.backend import GenRequest, VLLMBackend


class _Out:
    def __init__(self, text, reason, toks):
        self.text, self.finish_reason, self.token_ids = text, reason, toks


class _Req:
    def __init__(self, out, ptoks):
        self.outputs, self.prompt_token_ids = [out], ptoks


def test_vllm_backend_wiring(monkeypatch):
    seen = {}

    class FakeLLM:
        def __init__(self, **kw):
            seen["init"] = kw

        def generate(self, prompts, params, **kw):
            seen["prompts"], seen["params"], seen["kw"] = prompts, params, kw
            return [_Req(_Out(f"out {p}", "stop", [1, 2, 3]), [9] * 7) for p in prompts]

    class FakeSP:
        def __init__(self, **kw):
            self.kw = kw

    fake = types.SimpleNamespace(LLM=FakeLLM, SamplingParams=FakeSP, __version__="0.31.0")
    monkeypatch.setitem(sys.modules, "vllm", fake)

    b = VLLMBackend("m1", "Qwen/Qwen3-8B", revision="abc123", weights_hash="h")
    assert seen["init"]["enable_prefix_caching"] is True
    assert seen["init"]["revision"] == "abc123" and seen["init"]["model"] == "Qwen/Qwen3-8B"
    res = b.generate([GenRequest("p1", 0.7, 1024, 11), GenRequest("p2", 0.7, 2048, 12)])
    assert [p.kw for p in seen["params"]] == [
        {"temperature": 0.7, "max_tokens": 1024, "seed": 11},
        {"temperature": 0.7, "max_tokens": 2048, "seed": 12},
    ]
    assert seen["kw"]["tokenization_kwargs"] == {"add_special_tokens": False}
    assert res[0].text == "out p1" and res[0].completion_tokens == 3 and res[0].prompt_tokens == 7
    assert b.engine_version == "0.31.0"
