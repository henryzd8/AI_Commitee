"""Cell catalog (handbook §6.1, design §4.4).

A CellSpec is everything about a condition except the item, model and sample index.
"""

from __future__ import annotations

from dataclasses import dataclass

from pu.schemas import Branch, Channel, Direction, Frame, History, Policy, Remedy

DIRECTIONS = (Direction.LOOSEN, Direction.TIGHTEN)
ALL_CHANNELS = (Channel.C1, Channel.C2, Channel.C3, Channel.C4)


@dataclass(frozen=True)
class CellSpec:
    name: str
    branch: Branch
    frame: Frame
    history: History
    remedy: Remedy
    channel: Channel
    direction: Direction | None = None
    policy: Policy | None = None  # STATIC cells only: the delivered policy
    samples: int = 1

    def __post_init__(self) -> None:
        if self.frame == Frame.STATIC:
            assert self.history == History.NONE and self.policy is not None
            assert self.direction is None and self.remedy == Remedy.R0
        else:
            assert self.direction is not None and self.policy is None
            assert self.history != History.NONE

    @property
    def needs_history(self) -> bool:
        return self.history != History.NONE


# The five primary cells, numbered as in the design (§4.4).
PRIMARY = {
    1: (Frame.SWITCH, History.OLD_SELF, Remedy.R0),
    2: (Frame.NOOP, History.NEW_SELF, Remedy.R0),
    3: (Frame.SWITCH, History.NEW_SELF, Remedy.R0),
    4: (Frame.SWITCH, History.OLD_SELF, Remedy.R3),
    5: (Frame.NOOP, History.NEW_SELF, Remedy.R3),
}


def _dyn(
    n: int,
    d: Direction,
    ch: Channel,
    branch: Branch = Branch.PROBE,
    samples: int = 1,
    prefix: str = "cell",
) -> CellSpec:
    frame, hist, rem = PRIMARY[n]
    return CellSpec(
        name=f"{prefix}{n}-{d.value}-{ch.value}",
        branch=branch,
        frame=frame,
        history=hist,
        remedy=rem,
        channel=ch,
        direction=d,
        samples=samples,
    )


def screen_cells() -> list[CellSpec]:
    """Family screen: STATIC-R / STATIC-P, C1 frame, no history."""
    return [
        CellSpec(
            name=f"screen-{p.value}",
            branch=Branch.SCREEN,
            frame=Frame.STATIC,
            history=History.NONE,
            remedy=Remedy.R0,
            channel=Channel.C1,
            policy=p,
        )
        for p in (Policy.R, Policy.P)
    ]


def manip_cells(channels: tuple[Channel, ...] = ALL_CHANNELS) -> list[CellSpec]:
    """Manipulation check: R vs P delivered through each channel's own mechanism."""
    return [
        CellSpec(
            name=f"manip-{p.value}-{ch.value}",
            branch=Branch.MANIP,
            frame=Frame.STATIC,
            history=History.NONE,
            remedy=Remedy.R0,
            channel=ch,
            policy=p,
        )
        for ch in channels
        for p in (Policy.R, Policy.P)
    ]


def primary_cells(channels: list[Channel]) -> list[CellSpec]:
    return [_dyn(n, d, ch) for d in DIRECTIONS for ch in channels for n in PRIMARY]


def pilot_cells(channels: list[Channel]) -> list[CellSpec]:
    """Exploration / pilot: primary cells 1 and 2 only."""
    return [_dyn(n, d, ch) for d in DIRECTIONS for ch in channels for n in (1, 2)]


def explore_static_cells() -> list[CellSpec]:
    """Static cells on exploration items, for prompt work (static cells only)."""
    return [
        CellSpec(
            name=f"explore-static-{p.value}",
            branch=Branch.SCREEN,
            frame=Frame.STATIC,
            history=History.NONE,
            remedy=Remedy.R0,
            channel=Channel.C1,
            policy=p,
        )
        for p in (Policy.R, Policy.P)
    ]


def recognition_cells(channels: list[Channel], samples: int, calibration: bool) -> list[CellSpec]:
    """SWITCH x OLD-SELF prefix + recognition question; optional NOOP x NEW-SELF calibration."""
    out = [
        _dyn(1, d, ch, Branch.RECOG, samples, prefix="recog") for d in DIRECTIONS for ch in channels
    ]
    if calibration:
        out += [
            _dyn(2, d, ch, Branch.RECOG, samples, prefix="recogcal")
            for d in DIRECTIONS
            for ch in channels
        ]
    return out


def descriptive_cells(channels: list[Channel]) -> list[CellSpec]:
    return [_dyn(n, d, ch, prefix="desc") for d in DIRECTIONS for ch in channels for n in (1, 2)]
