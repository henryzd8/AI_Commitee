"""Run manifests: everything needed to reproduce or audit a run (handbook §6.4)."""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from typing import Any

from pu.config import REPO_ROOT


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _pkg_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def gpu_info() -> list[str]:
    if not shutil.which("nvidia-smi"):
        return []
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
        return [line.strip() for line in out.stdout.splitlines() if line.strip()]
    except (subprocess.SubprocessError, OSError):
        return []


def git_commit() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        dirty = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        ).stdout.strip()
        return out.stdout.strip() + ("-dirty" if dirty else "")
    except (subprocess.SubprocessError, OSError):
        return None


def environment() -> dict[str, Any]:
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "vllm": _pkg_version("vllm"),
        "torch": _pkg_version("torch"),
        "transformers": _pkg_version("transformers"),
        "policy_updates": _pkg_version("policy-updates"),
        "gpus": gpu_info(),
        "git_commit": git_commit(),
    }


def config_hashes(paths: list[str | Path]) -> dict[str, str]:
    from pu.io import sha256_file

    return {str(p): sha256_file(p) for p in paths if Path(p).exists()}
