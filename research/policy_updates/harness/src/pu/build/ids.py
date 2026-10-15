"""Opaque request IDs (handbook §11).

IDs are HMAC-SHA256(salt, condition) formatted as a UUID. Without the salt (kept in keys/,
blinded analyst only) an ID reveals nothing about its condition; with the same salt the IDs
are reproducible, which makes building and running resumable.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from pathlib import Path

SALT_FILE = "salt.txt"


def new_salt() -> str:
    return secrets.token_hex(32)


def load_or_create_salt(keys_dir: str | Path) -> str:
    keys_dir = Path(keys_dir)
    keys_dir.mkdir(parents=True, exist_ok=True)
    p = keys_dir / SALT_FILE
    if p.exists():
        return p.read_text().strip()
    salt = new_salt()
    p.write_text(salt + "\n")
    p.chmod(0o600)
    return salt


def opaque_id(salt: str, *parts: object) -> str:
    msg = "\x1f".join(str(p) for p in parts).encode("utf-8")
    digest = hmac.new(bytes.fromhex(salt), msg, hashlib.sha256).digest()
    return str(uuid.UUID(bytes=digest[:16], version=4))
