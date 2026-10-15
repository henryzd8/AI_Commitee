"""JSONL and hashing helpers. JSONL files are append-only; new versions get new files."""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

from pu.schemas import to_dict


def canonical_json(obj: Any) -> str:
    return json.dumps(to_dict(obj), sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def read_jsonl(path: str | Path) -> Iterator[dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                # A crash can leave a half-written last line; skip it (it will be redone).
                with open(path, encoding="utf-8") as g:
                    total = sum(1 for _ in g)
                if lineno == total:
                    return
                raise


def repair_tail(path: str | Path) -> bool:
    """Drop a half-written last line left by a crash, so the next append starts on a fresh line.
    Returns True if the file was repaired."""
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        return False
    with open(path, "rb+") as f:
        f.seek(-1, os.SEEK_END)
        if f.read(1) == b"\n":
            return False
        f.seek(0)
        data = f.read()
        cut = data.rfind(b"\n") + 1  # 0 if there is no complete line at all
        f.truncate(cut)
        f.flush()
        os.fsync(f.fileno())
    return True


def append_jsonl(path: str | Path, records: Iterable[Any]) -> int:
    """Append records and fsync, so a crash loses at most the in-flight batch."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    repair_tail(path)
    n = 0
    with open(path, "a", encoding="utf-8") as f:
        for r in records:
            f.write(canonical_json(r) + "\n")
            n += 1
        f.flush()
        os.fsync(f.fileno())
    return n


def write_jsonl_atomic(path: str | Path, records: Iterable[Any]) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    n = 0
    with open(tmp, "w", encoding="utf-8") as f:
        for r in records:
            f.write(canonical_json(r) + "\n")
            n += 1
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    return n


def write_json_atomic(path: str | Path, obj: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(to_dict(obj), f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def derive_seed(*parts: object) -> int:
    """Deterministic 31-bit seed from arbitrary parts."""
    digest = hashlib.sha256(":".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(digest[:8], "big") % (2**31 - 1)
