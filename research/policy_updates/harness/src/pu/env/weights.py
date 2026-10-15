"""Model weight download and hashing (handbook §6.5, §7).

`hash_model_dir` gives one reproducible SHA-256 per model: the hash of the sorted list of
"relative_path sha256" lines over every weight / config / tokenizer file.
"""

from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Any

import yaml

from pu.config import CONFIG_DIR
from pu.io import sha256_file, sha256_text

WEIGHT_PATTERNS = [
    "*.safetensors",
    "*.bin",
    "*.json",
    "*.model",
    "*.txt",
    "*.jinja",
    "*.tiktoken",
    "*.py",
]
SKIP_DIRS = {".cache", ".git"}


def list_model_files(model_dir: str | Path, patterns: list[str] = WEIGHT_PATTERNS) -> list[Path]:
    model_dir = Path(model_dir)
    files = []
    for p in sorted(model_dir.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.relative_to(model_dir).parts):
            continue
        if any(fnmatch.fnmatch(p.name, pat) for pat in patterns):
            files.append(p)
    return files


def hash_model_dir(model_dir: str | Path) -> tuple[str, dict[str, str]]:
    model_dir = Path(model_dir)
    per_file = {str(p.relative_to(model_dir)): sha256_file(p) for p in list_model_files(model_dir)}
    if not per_file:
        raise FileNotFoundError(f"no model files under {model_dir}")
    combined = sha256_text("\n".join(f"{k} {v}" for k, v in sorted(per_file.items())))
    return combined, per_file


def download_model(hf_repo: str, revision: str | None, local_dir: str | Path) -> tuple[str, Path]:
    """Download a snapshot at a pinned revision. Returns (resolved commit sha, local dir).

    Gated repos (Llama, Gemma) need the license accepted on huggingface.co and HF_TOKEN set.
    """
    from huggingface_hub import HfApi, snapshot_download  # lazy: optional dependency

    info = HfApi().model_info(hf_repo, revision=revision)
    sha = info.sha
    path = snapshot_download(
        repo_id=hf_repo,
        revision=sha,
        local_dir=str(local_dir),
        allow_patterns=WEIGHT_PATTERNS,
    )
    return sha, Path(path)


def record_in_models_yaml(
    model_id: str, revision: str, weights_sha256: str, path: str | Path | None = None
) -> None:
    """Write the resolved revision and weight hash into configs/models.yaml (in place)."""
    path = Path(path or CONFIG_DIR / "models.yaml")
    d: dict[str, Any] = yaml.safe_load(path.read_text()) or {}
    for m in d.get("models", []):
        if m["id"] == model_id:
            m["revision"] = revision
            m["weights_sha256"] = weights_sha256
            break
    else:
        raise KeyError(model_id)
    path.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True))
