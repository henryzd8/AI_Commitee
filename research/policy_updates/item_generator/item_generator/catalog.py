"""Explicit family definitions; editing one family does not edit the engine."""
from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from .templates import ProblemTemplate, TEMPLATE_FACTORIES

CATALOG_PATH = Path(__file__).with_name('families.json')


@dataclass(frozen=True)
class ProblemFamily:
    family_id: str
    history_family_id: str
    seed_slot: int
    heldout: bool
    probe: ProblemTemplate
    history: ProblemTemplate

    def __post_init__(self):
        if any(not isinstance(v,str) or not v.strip() for v in (self.family_id,self.history_family_id)) or self.family_id==self.history_family_id:
            raise ValueError('Probe and history need distinct, nonempty family IDs.')
        if type(self.seed_slot) is not int or self.seed_slot<0 or type(self.heldout) is not bool:
            raise ValueError('Use a nonnegative integer seed_slot and boolean heldout flag.')

    def generate(self, *, seed: str, index: int = 0, split: str = 'preview', history: bool = False, registration=None) -> dict:
        from .generator import generate_instance
        return generate_instance(self, split=split, seed=seed, index=index, history=history,registration=registration)

    def describe(self) -> dict:
        return {'family_id': self.family_id, 'history_family_id': self.history_family_id,
                'seed_slot': self.seed_slot, 'heldout': self.heldout,
                'probe': self.probe.describe(), 'history': self.history.describe()}


@lru_cache(maxsize=8)
def _parse_catalog(text: str) -> tuple[ProblemFamily, ...]:
    records = json.loads(text)
    if not isinstance(records,list):
        raise ValueError('The family catalog must be a JSON list of definitions.')
    result = []
    for row in records:
        if not isinstance(row,dict) or set(row) != {'family_id','history_family_id','seed_slot','heldout','probe','history'}:
            raise ValueError('Family definitions need IDs, seed_slot, heldout, probe, and history.')
        if not isinstance(row['probe'],dict) or not isinstance(row['history'],dict):
            raise ValueError('Probe and history templates must be JSON objects.')
        if type(row['seed_slot']) is not int or row['seed_slot'] < 0 or type(row['heldout']) is not bool:
            raise ValueError('seed_slot must be a nonnegative integer and heldout a boolean.')
        try:
            probe = TEMPLATE_FACTORIES[row['probe']['type']](row['probe'])
            history = TEMPLATE_FACTORIES[row['history']['type']](row['history'])
        except KeyError as exc:
            raise ValueError(f"Unknown template type in {row['family_id']}.") from exc
        result.append(ProblemFamily(row['family_id'],row['history_family_id'],row['seed_slot'],row['heldout'],probe,history))
    all_ids = [value for f in result for value in (f.family_id,f.history_family_id)]
    if not result or any(not isinstance(v,str) or not v.strip() for v in all_ids) or len(set(all_ids)) != len(all_ids):
        raise ValueError('Family IDs must be nonempty and globally unique.')
    if len({f.seed_slot for f in result}) != len(result):
        raise ValueError('seed_slot values must be unique; never reuse a retired slot.')
    return tuple(sorted(result, key=lambda f: f.seed_slot))


def load_families() -> tuple[ProblemFamily, ...]:
    return _parse_catalog(CATALOG_PATH.read_text(encoding='utf-8'))


def get_family(family_id: str) -> ProblemFamily:
    for family in load_families():
        if family.family_id == family_id:
            return family
    raise ValueError(f'Unknown probe family {family_id!r}. Use the list command to see IDs.')
