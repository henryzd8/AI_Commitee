# Task 1: candidate item and history generator

Development implementation; family quality still requires committee review.
Start with [the family review pack](FAMILY_REVIEW.md): all 40 pairs, operation sequences,
five development examples per family, and a review checklist. No confirmatory items
are included. A family is a reusable template with varying numbers, not a single problem.

Run from this directory with Python 3.10+:

```sh
python -m pip install -e ../policy_checker -e .
python -m unittest discover -s tests -v
python -m item_generator families runs/families.json
python -m item_generator generate exploration runs/exploration.jsonl --seed A
python -m item_generator histories runs/exploration.jsonl runs/histories.jsonl
```

No new runtime dependencies. Collision checking uses the sibling task-4 checker's
number parser. Files must be new; the runs directory is ignored. The task-5 module
is not required. Use `python export_review.py` to regenerate the committed review
pack, which refuses to overwrite an existing reviewed copy.

## Task 1: generator

- 40 probe families and 40 paired history families. Each has a different inventory
  domain and a distinct four-operation sequence; paired sequences differ.
- Each item stores text, three named intermediate values, final answer, family ID,
  seed, split, instance index, paraphrase, and content/source hashes.
- Positive integer arithmetic is required throughout. The final answer must be
  100–9999 and absent from both the problem's numbers and intermediate values.
- An independent solver reparses the **rendered text** using rational arithmetic;
  it does not reuse the generator's arithmetic results or stored operands.
- Screening: 40 items/family (1,600). Exploration: 100 items from F01–F32.
  F33–F40 are held out from prompt development. Manipulation: fresh 100 across
  all 40 families. Validation: fresh 100 across the development families, a
  documented development default because the assignment gives no item count.
  These are stimulus counts, not the checker's 300-response annotation sample.
- Seeds include split names. Explicit seeds and source fingerprints make output
  reproducible. Split IDs cannot overlap; content duplicates within a generated
  split fail. Archive manifests and check content hashes across any later custom
  seeds/replacements before freezing; distinct seeds alone do not prove unique text.
- Five probe paraphrases are balanced within each family to within one item.
  Exact five-way balance is impossible in exploration families with 3–4 items.
  Confirmatory allocation is exactly 15/family, hence three of each paraphrase.
- `histories` produces four history problems per probe, preserving nesting. The
  runner owns generating assistant responses under R/P (task 3).
- `collisions` accepts JSONL rows with `probe` and `histories` (a list containing
  ALL visible history text from both policies and every model). A collision uses
  the next reserved candidate index in that same family, deterministically. The
  reserved stream advances by 1,000,000 to avoid ordinary split indices. It retains
  the original paraphrase and logs replacements. Run once on the union of histories
  before any probe call so the same replacement is used for every model/channel.
  Exhausting the candidate limit raises an error. Numeric parser limitations from
  the checker apply, including unsupported equivalent arithmetic expressions.

### Confirmatory lock

Only the allocation (600 = 40 × 15) and lock rejection are tested. A real
`python -m item_generator generate confirmatory` call requires `--registration record.json`, containing
`registration_url`, `registered_at`, `generator_hash`, and `family_hash` matching
the source and registry. Obtain hashes with `families`. This is an accidental-use
guard, not external verification of OSF or protection against editing the code.
Do not fill this record with placeholders to run confirmation before registration.

### Family quality boundary

These are **candidate arithmetic inventory templates**, not human-approved natural
word problems. Eighty operation sequences do not establish 80 substantively distinct
reasoning mechanisms. Some sequences share operations or simplify to similar algebra.
Treating them as independent family clusters without review may understate uncertainty.
Review five rendered samples per family, revise overly similar or unnatural families,
and run the static screen. Automated replay of five samples is not that human review.
The five paraphrases are also provisional until the prompt-library owner adopts them.

