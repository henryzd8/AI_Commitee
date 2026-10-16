# Task 1: problem families and study inputs

Create reproducible arithmetic problems, inspect the families, and prepare files
for the task-3 runner. **The 40 probe and 40 history families remain candidates:**
this package checks arithmetic, not educational quality or statistical independence.
No confirmatory item set has been generated during development.

## Start here

From this directory, using Python 3.10+:

```sh
python -m pip install -e ../policy_checker -e .
python -m item_generator list
python -m item_generator preview F01 --count 3 --seed A
python -m item_generator prepare exploration runs/exploration-A --seed A
```

After installation, `policy-items` is a shorter alias for `python -m item_generator`.
Use `--help` on either the main command or a subcommand. Generation and previews
use only the standard library; collision checks use the existing task-4 checker.

`prepare` handles the routine multi-step workflow in one command:

| Output | Purpose |
|---|---|
| `probes.jsonl` | Raw problems, reference answers, intermediate values, seed/index metadata |
| `histories.jsonl` | Four raw history problems linked to every probe |
| `items.jsonl` | Probe records matching task 3's strict `Item` schema |
| `history_items.jsonl` | History records matching that same schema |
| `families.json` | Snapshot of the actual family definitions |
| `manifest.json` | Counts, seed, source/catalog fingerprints, file checksums, and pending collision status |

Give **items.jsonl and history_items.jsonl** to the runner. Retain the other files
for reproducibility. Existing output directories/files are never overwritten.
Input errors identify the missing field or JSONL line instead of printing a long
traceback. Filesystem failures can leave a partial output directory; do not treat
an incomplete bundle as a successful run.

Preparing input files does not run a model or resolve history-answer collisions.
After the runner generates both R/P histories, perform the collision step below
before making any probe calls.

## Inspect and review families

- Open [FAMILY_REVIEW.md](FAMILY_REVIEW.md) for the existing five-sample-per-family review pack.
- Preview a history template with `python -m item_generator preview F01 --history`.
- Make a fresh review pack with `python -m item_generator review runs/review-v2.md`.

Review clarity, arithmetic, meaningful reasoning steps, answer leakage, similarity
between families, and the distinction between probe and history. Record keep/revise/
replace decisions and reviewer initials. The program does not mark families approved.
Held-out families may be reviewed for quality but must not be used to tune prompts.

The initial inventory templates often state arithmetic operations explicitly. They
are a starting point, not 40 certified independent reasoning structures. Different
stories or operation sequences can simplify to the same underlying calculation.

## Edit or extend a family

The definition of each pair lives together in
[`item_generator/families.json`](item_generator/families.json). It contains IDs,
a stable `seed_slot`, a held-out flag, and separate probe/history template settings.
There are no parallel lists whose positions must stay aligned.

```python
from item_generator import get_family

family = get_family("F01")
problem = family.generate(seed="A", index=0)
print(problem["problem"])
print(problem["final_answer"])
```

`ProblemFamily` is an immutable dataclass. A template strategy supplies sampling,
rendering, and a separate solver. The shared engine validates every accepted item.
You do not need to write one class per family. See [ADDING_FAMILIES.md](ADDING_FAMILIES.md)
for the edit workflow and how to add a genuinely different problem type.

## Study rules retained

- Final answers are integers from 100 to 9999, different from the declared inputs,
  printed numeric values, and intermediate values; all solution steps are positive integers.
- The template's independent solver reads the rendered question and must reproduce
  every solution step. It cannot merely return the stored generated answer.
- Screening: 40 items × 40 families. Exploration and validation: 100 items across
  the 32 development families. Manipulation: fresh 100 across all 40 families.
  The validation stimulus count remains a development default, not the checker's
  300-response annotation quota.
- Confirmatory allocation: 15 × 40 = 600, tested as an allocation only.
- Five request paraphrases are balanced within family to within one item; at 15
  items each paraphrase occurs three times. Task 2 still owns the final prompt text.
- The seed includes the split, stable family seed slot, index, and history/probe role.
  Reordering the catalog does not change items. Integer seeds now normalize to text
  consistently; previously supplied string seeds preserve their item content.
- New family IDs/held-out settings are read from the catalog rather than inferred
  from ID spelling. The current study allocation deliberately rejects a catalog
  other than 40 families/8 held out; changing study size requires an explicit design change.

Content duplicates within a generated split fail. Review hashes across separately
chosen seeds or replacement sets before freezing: different seeds are not a proof
of globally unique text. Numeric checks do not understand all mathematical prose;
each new strategy must expose its input values and have its wording reviewed.

## Lower-level commands and collisions

The original commands remain available:

```sh
python -m item_generator generate exploration runs/probes.jsonl --seed A
python -m item_generator histories runs/probes.jsonl runs/histories.jsonl
python -m item_generator collisions collisions-input.jsonl runs/replaced.jsonl
python -m item_generator export-harness runs/replaced.jsonl runs/histories.jsonl runs/runner-final
python -m item_generator families runs/definitions-and-hashes.json
```

Collision input: one JSON object per line, with `probe` (the complete raw probe
record) and `histories` (a list of all visible user/assistant history strings, both
policies and every model). Check their union once so all comparisons use the same
replacement. Never choose replacements after seeing a probe response.

Replacement follows the same family's deterministic reserved stream (index strides
of 1,000,000), preserves the assigned paraphrase and original history link, and
fails when its search limit is exhausted. Rechecking or rebuilding history-problem
files retains the original histories. The checker parser's known format limitations
still apply. Use `--registration RECORD.json` for confirmatory replacements.

Task-3 export includes exactly four history IDs per probe and maps the split names,
text, and named steps to `schemas.Item`. Its integer seed is derived from SHA256
of the original seed string; retain raw files to reproduce generator sampling.

## Confirmatory guard and versioning

Confirmatory `generate`/`prepare` calls require `--registration RECORD.json`, with
the actual `registration_url`, `registered_at`, `generator_hash`, and `family_hash`.
The family-level Python API also checks registration for confirmatory instances.
The fingerprint now covers **all package Python/config files**, not just generator.py.
Export current hashes with `families`; old hashes intentionally do not match this
refactored version. This is an accidental-use guard, not verification of OSF or
protection against someone editing the code. Do not use dummy registration records.

## Tests and layout

```sh
python -m unittest discover -s tests -v
```

Regression tests compare 400 probe/history examples with a fingerprint saved before
the refactor. They also cover custom non-sequential templates, incorrect solvers,
catalog order, the one-command workflow, output checksums, collision/history linkage,
registration guards, and parsing exports with task 3's actual `Item` schema.

| File | Responsibility |
|---|---|
| `catalog.py` / `families.json` | Family objects and explicit definitions |
| `templates.py` | Problem-type strategies and independent solvers |
| `generator.py` | Shared validity rules, deterministic generation, splits, collisions |
| `workflow.py` / `files.py` | Complete bundles, checksums, safe file handling |
| `harness_export.py` | Task-3 schema adapter |
| `review.py` / `__main__.py` | Review packs and command-line interface |

This rewrite changes maintainability and usability, not the scientific approval
status of the candidate families. Task 5 is a separate package and PR.
