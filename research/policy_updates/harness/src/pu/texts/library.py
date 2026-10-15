"""Read-only access to the versioned text library (configs/texts/*.yaml, owned by Task 2).

The builder only composes texts; it never invents wording. Every slot must be filled.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from pu.config import CONFIG_DIR, load_yaml
from pu.io import sha256_file
from pu.schemas import Channel, Policy

_SLOT = re.compile(r"\{[a-zA-Z_]+\}")


class TextLibrary:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path or CONFIG_DIR / "texts" / "v0.yaml")
        self.d: dict[str, Any] = load_yaml(self.path)
        self.version: str = str(self.d.get("version", "unknown"))
        self.hash: str = sha256_file(self.path)

    # -- primitives ---------------------------------------------------------
    @staticmethod
    def _fill(template: str, **kw: Any) -> str:
        out = template.format(**kw)
        if _SLOT.search(out):
            raise ValueError(f"unfilled slot in: {out!r}")
        return out

    @property
    def role(self) -> str:
        return self.d["role"]

    def policy_body(self, p: Policy) -> str:
        return self.d["policy_body"][p.value]

    def policy_text(self, p: Policy) -> str:
        return f"{self.d['policy_label']} {self.policy_body(p)}"

    def shared_lines(self, channel: Channel) -> str:
        staff = self._fill(self.d["staff_line"], channel_desc=self.d["channel_desc"][channel.value])
        return f"{self.d['format_line']}\n{staff}"

    @property
    def update_note(self) -> str:
        return self.d["update_note"]

    def r3_notice(self, current: Policy) -> str:
        return self._fill(self.d["r3_notice"], policy_body=self.policy_body(current))

    @property
    def c3_instruction(self) -> str:
        return self.d["c3_instruction"]

    def c4_schedule(self, t: str, before: Policy, after: Policy) -> str:
        return self._fill(
            self.d["c4_schedule"], T=t, X=self.policy_body(before), Y=self.policy_body(after)
        )

    def c4_log(self, timestamps: list[str]) -> str:
        """timestamps[i] is turn i+1; the last one is the current turn."""
        lines = [self.d["c4_log_header"]]
        for n, ts in enumerate(timestamps[:-1], 1):
            lines.append(self._fill(self.d["c4_log_turn"], n=n, ts=ts))
        lines.append(self._fill(self.d["c4_log_current"], n=len(timestamps), ts=timestamps[-1]))
        return "\n".join(lines)

    def student(self, turn: int, problem: str) -> str:
        key = "help" if turn in (1, 3) else "full"
        return self._fill(self.d["student"][key], problem=problem)

    def probe(self, paraphrase_id: int, problem: str) -> str:
        return self._fill(self.d["probes"][paraphrase_id], problem=problem)

    @property
    def n_probes(self) -> int:
        return len(self.d["probes"])

    def recognition(self, polarity: str, yes_option: str) -> str:
        r = self.d["recognition"]
        a, b = (r["yes"], r["no"]) if yes_option == "A" else (r["no"], r["yes"])
        return self._fill(r[polarity], a=a, b=b)

    @property
    def tool_schema(self) -> dict[str, Any]:
        t = self.d["tool"]
        return {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"],
            },
        }

    @property
    def tool_name(self) -> str:
        return self.d["tool"]["name"]

    # -- composed system prompts ----------------------------------------------
    def system_with_policy(self, p: Policy, channel: Channel) -> str:
        """Role + policy + shared lines (C1, C2, static cells, history generation)."""
        return f"{self.role}\n\n{self.policy_text(p)}\n{self.shared_lines(channel)}"

    def system_neutral(self, channel: Channel) -> str:
        """Role + shared lines, no policy (C2 manipulation check)."""
        return f"{self.role}\n\n{self.shared_lines(channel)}"

    def system_c3(self) -> str:
        return f"{self.role}\n\n{self.c3_instruction}\n{self.shared_lines(Channel.C3)}"

    def system_c4(self, t: str, before: Policy, after: Policy, timestamps: list[str]) -> str:
        return (
            f"{self.role}\n\n{self.c4_schedule(t, before, after)}\n"
            f"{self.shared_lines(Channel.C4)}\n\n{self.c4_log(timestamps)}"
        )
