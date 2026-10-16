"""Template strategies: sampling and independent text solving are separate paths."""
from dataclasses import dataclass
from fractions import Fraction
from random import Random
import re
from typing import Protocol


@dataclass(frozen=True)
class Candidate:
    text: str
    steps: tuple[Fraction, ...]
    input_values: tuple[int, ...]


class ProblemTemplate(Protocol):
    """Implement this interface for a new kind of problem; last step is the answer."""
    domain: str
    def sample(self, rng: Random) -> Candidate: ...
    def solve(self, text: str) -> tuple[Fraction, ...]: ...
    def describe(self) -> dict: ...


def solve_inventory(text: str) -> tuple[Fraction, ...]:
    initial = re.search(r'Start with (\d+) units\.', text)
    if not initial:
        raise ValueError('Inventory problem has no starting quantity.')
    value = Fraction(int(initial[1]))
    steps = []
    for sentence in text.split('. '):
        match = re.search(r'(Add|Remove|Multiply the current quantity by|Divide the current quantity by) (\d+)', sentence)
        if not match:
            continue
        verb, number = match[1], int(match[2])
        if verb == 'Add':
            value += number
        elif verb == 'Remove':
            value -= number
        elif verb.startswith('Multiply'):
            value *= number
        else:
            value /= number
        steps.append(value)
    if not 3 <= len(steps) <= 5:
        raise ValueError('Expected 3–5 arithmetic steps.')
    return tuple(steps)


@dataclass(frozen=True)
class InventoryTemplate:
    domain: str
    operations: tuple[str, ...]

    def __post_init__(self):
        if not isinstance(self.domain,str) or not self.domain.strip() or not isinstance(self.operations,(list,tuple)) or not 3 <= len(self.operations) <= 5:
            raise ValueError('Inventory templates need a context and 3–5 operations.')
        object.__setattr__(self,'operations',tuple(self.operations))
        if any(op not in ('add', 'sub', 'mul', 'div') for op in self.operations):
            raise ValueError(f'Unknown operation in {self.domain}.')

    def sample(self, rng: Random) -> Candidate:
        start = rng.randint(40, 200)
        operands = [rng.randint(2, 5) if op == 'div' else rng.randint(2, 9)
                    if op == 'mul' else rng.randint(10, 80) for op in self.operations]
        value = Fraction(start)
        steps = []
        for op, operand in zip(self.operations, operands):
            if op == 'add': value += operand
            elif op == 'sub': value -= operand
            elif op == 'mul': value *= operand
            else: value /= operand
            steps.append(value)
        verbs = {'add': 'Add', 'sub': 'Remove', 'mul': 'Multiply the current quantity by',
                 'div': 'Divide the current quantity by'}
        text = f'An inventory exercise concerns {self.domain}. Start with {start} units. '
        text += '. '.join(f'{verbs[op]} {n}' for op, n in zip(self.operations, operands))
        text += '. How many units remain?'
        return Candidate(text, tuple(steps), (start, *operands))

    def solve(self, text: str) -> tuple[Fraction, ...]:
        return solve_inventory(text)

    def describe(self) -> dict:
        return {'type': 'inventory', 'domain': self.domain, 'operations': list(self.operations)}


def inventory_factory(config: dict) -> ProblemTemplate:
    if set(config) != {'type', 'domain', 'operations'}:
        raise ValueError('Inventory definition must contain only type, domain, operations.')
    return InventoryTemplate(config['domain'], tuple(config['operations']))


# Add a factory for a new mathematical structure here. JSON never executes code.
TEMPLATE_FACTORIES = {'inventory': inventory_factory}
