from __future__ import annotations

import pytest

from pu.config import ModelSpec, RunConfig
from pu.testing.fakes import make_histories, make_items
from pu.texts.library import TextLibrary

ALL_TRUE = {"C1": True, "C2": True, "C3": True, "C4": True}


@pytest.fixture(scope="session")
def texts() -> TextLibrary:
    return TextLibrary()


@pytest.fixture(scope="session")
def cfg() -> RunConfig:
    return RunConfig.load()


@pytest.fixture
def models() -> list[ModelSpec]:
    return [
        ModelSpec(id="mA", hf_repo="fake/a", support=dict(ALL_TRUE)),
        ModelSpec(id="mB", hf_repo="fake/b", support={**ALL_TRUE, "C2": False}),
    ]


@pytest.fixture(scope="session")
def small_items():
    return make_items("confirm", n_families=4, items_per_family=3)


@pytest.fixture(scope="session")
def full_confirm_items():
    """40 families x 15 = 600 items, the confirmatory size."""
    return make_items("confirm", n_families=40, items_per_family=15, heldout_families=8)


@pytest.fixture(scope="session")
def small_histories(small_items):
    probes, _ = small_items
    return make_histories(["mA", "mB"], probes)
