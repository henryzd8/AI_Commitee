"""Loading configs/run.yaml and configs/models.yaml."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from pu.schemas import Channel

REPO_ROOT = Path(__file__).resolve().parents[2]
# PU_CONFIG_DIR overrides (e.g. inside the Docker image); default is the repo's configs/.
CONFIG_DIR = Path(os.environ.get("PU_CONFIG_DIR", REPO_ROOT / "configs"))


def load_yaml(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@dataclass
class SamplingConfig:
    temperature: float = 0.7
    max_tokens: int = 1024
    retry_max_tokens: int = 2048


@dataclass
class C4Clock:
    """C4 timestamp convention (handbook §5.2). DRAFT values, owned with Task 2."""

    base: str = "2027-03-01 14:00"
    switch_spacing_min: int = 5
    gap_min: int = 10  # g: distance between T and turn 5
    noop_spacing_min: int = 1
    noop_offset_min: int = 2  # NOOP turn 1 = T + offset

    def base_dt(self) -> datetime:
        return datetime.strptime(self.base, "%Y-%m-%d %H:%M")


@dataclass
class RecognitionConfig:
    items_per_direction: int = 150
    samples: int = 3
    channel_assignment: str = "split"  # "split" (each item in one of C3/C4) | "both"
    calibration: bool = True  # NOOP x NEW-SELF prefix + same question


@dataclass
class DescriptiveConfig:
    items_per_direction: int = 300
    channels: list[Channel] = field(default_factory=lambda: [Channel.C1, Channel.C2])


@dataclass
class RunConfig:
    sampling: SamplingConfig = field(default_factory=SamplingConfig)
    primary_channels: list[Channel] = field(default_factory=lambda: [Channel.C3, Channel.C4])
    recognition: RecognitionConfig = field(default_factory=RecognitionConfig)
    descriptive: DescriptiveConfig = field(default_factory=DescriptiveConfig)
    c4_clock: C4Clock = field(default_factory=C4Clock)
    batch_size: int = 256
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str | Path | None = None) -> RunConfig:
        d = load_yaml(path or CONFIG_DIR / "run.yaml")
        rec = d.get("recognition", {})
        desc = d.get("descriptive", {})
        return cls(
            sampling=SamplingConfig(**d.get("sampling", {})),
            primary_channels=[Channel(c) for c in d.get("primary_channels", ["C3", "C4"])],
            recognition=RecognitionConfig(**rec),
            descriptive=DescriptiveConfig(
                items_per_direction=desc.get("items_per_direction", 300),
                channels=[Channel(c) for c in desc.get("channels", ["C1", "C2"])],
            ),
            c4_clock=C4Clock(**d.get("c4_clock", {})),
            batch_size=d.get("runner", {}).get("batch_size", 256),
            raw=d,
        )


@dataclass
class ModelSpec:
    id: str
    hf_repo: str
    revision: str | None = None
    weights_sha256: str | None = None
    size_class: str = "8b"
    tensor_parallel_size: int = 1
    dtype: str = "bfloat16"
    quantization: str | None = None
    max_model_len: int = 8192
    gpu_memory_utilization: float = 0.90
    chat_template_kwargs: dict[str, Any] = field(default_factory=dict)
    support: dict[str, bool | None] = field(default_factory=dict)
    gated: bool = False
    role: str = "candidate"
    notes: str = ""

    def supports(self, channel: Channel) -> bool | None:
        return self.support.get(channel.value)


def load_models(path: str | Path | None = None) -> dict[str, ModelSpec]:
    d = load_yaml(path or CONFIG_DIR / "models.yaml")
    out: dict[str, ModelSpec] = {}
    for m in d.get("models", []):
        spec = ModelSpec(**m)
        out[spec.id] = spec
    return out
