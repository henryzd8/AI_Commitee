# Editing families without changing the generation engine

## Change an existing inventory family

1. Find its `family_id` in `item_generator/families.json`.
2. Edit its probe/history context or operation sequence. Keep the IDs and `seed_slot`
   stable unless intentionally defining a new family. Do not reuse a retired seed slot.
3. Preview both sides, then generate several review samples.
4. Run the tests and get human review/static screening before using the revised family.

Example structure (edit the existing record; do not append a duplicate):

```json
{
  "family_id": "F01",
  "history_family_id": "H01",
  "seed_slot": 0,
  "heldout": false,
  "probe": {
    "type": "inventory",
    "domain": "library books",
    "operations": ["add", "add", "add", "mul"]
  },
  "history": {
    "type": "inventory",
    "domain": "observatory star cards",
    "operations": ["sub", "add", "mul", "sub"]
  }
}
```

Use `python -m item_generator preview F01 --seed A` and the same command with
`--history`. Generate a new review pack rather than overwriting reviewers' notes.

Changing a family changes its content and the source fingerprint. A changed family
needs a new review/version; reproducibility does not mean edits should preserve old
outputs. Catalog *reordering* is safe because sampling uses the explicit seed slot.

## Add a different mathematical structure

Do not force every problem into the inventory operation list. Implement the
`ProblemTemplate` interface in a package module:

- `sample(rng) -> Candidate`: sample inputs and render the problem. Return its
  text, 3–5 exact solution-step values (last value is the answer), and all input values.
- `solve(text) -> tuple[Fraction, ...]`: independently extract inputs from the
  rendered text and solve it. Do not read the generated Candidate or cached answers.
- `describe() -> dict`: return serializable settings that describe the template.
- `domain`: a readable description for previews and review sheets.

Use the supplied `rng` only; do not use global randomness, time, or external services.
Keep arithmetic exact with integers or `Fraction`. The shared engine rejects
nonpositive/nonintegral steps, invalid answer ranges, and final-answer collisions.
It retries invalid sampled parameters, but fails immediately on solver disagreement.

Register a factory in `templates.TEMPLATE_FACTORIES`. The factory validates the
JSON settings and constructs your template object. Set a family's `probe.type`
or `history.type` to that factory's name, with the parameters the factory accepts.
The CLI, bundle workflow, and review exporter use the same interface automatically.

For a concrete working example of a different dependency structure, see
`test_custom_branched_template_needs_no_engine_changes` in `tests/test_usability.py`:
it calculates adult and child ticket subtotals independently, combines them, and
subtracts a fee. It is a test fixture, not an approved study family.

You can construct a `ProblemFamily` directly for prototyping before registering it:

```python
from item_generator import ProblemFamily, get_family

# ticket_template is your ProblemTemplate implementation.
prototype = ProblemFamily(
    family_id="T01", history_family_id="TH01", seed_slot=100,
    heldout=False, probe=ticket_template, history=get_family("F01").history,
)
example = prototype.generate(seed="trial-A")  # preview split by default
```

Adding a strategy does not require changing split logic, the runner adapter, or the
checker. Changing the study's family count does require revisiting allocation and
statistics: the current protocol requires 40 families and 8 held out.

## Acceptance checklist

- Re-solve at least five examples independently; inspect for ambiguity and leaked answers.
- Exercise edge cases: small/large inputs, exact division, and alternate reasonable interpretations.
- Verify the solver actually parses the rendered question; changing a number in the text should change its answer.
- Compare against other families for algebraic equivalence and shared shortcuts.
- Add tests for this strategy and for bad inputs/solver disagreement.
- Confirm the probe/history pair differs meaningfully and uses consistent units.
- Preserve reviewer decisions; get committee approval before freezing or confirmation.
