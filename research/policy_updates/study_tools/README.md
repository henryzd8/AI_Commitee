# Task 5: blinding, gate scripts, and statistical analysis

Development implementation of assignment 5. Independent of task 1's package.
The checker integration test uses the existing task-4 module. Gate methods still
require committee approval before freezing; real-response validation remains pending.

```sh
python -m pip install -e ../policy_checker -e .
python -m unittest discover -s tests -v
```

See [verification notes](VERIFICATION.md) for original combined implementation results;
the PR records separate-package test results after this organizational split.

## Task 5: data contracts and blinding

`blind INPUT.jsonl NEW_DIRECTORY` exports opaque, random request IDs and only
problem/response text. All original metadata lives in `private/key.json`. Arbitrary
extra fields are excluded from public output. `blinding.restore` verifies untouched
public text and IDs before recovering records. This complements task 4's annotation
sheets; it does not replace them or generate model requests.

The original phrase "condition key held only by the blinded analyst" is ambiguous:
someone reading the key is no longer condition-blinded. Here the key belongs to a
trusted coordinator/independent gate analyst; prompt tuners receive only pilot
PASS/FAIL. Public data remain condition-blinded except for clues in the actual text.
Separation is organizational, not filesystem permissions or encryption.

Gate inputs:

- `screen`: `family_id,item_id,model_id,policy,given`; one frozen no-history frame,
  40 identical item IDs across R/P and each model, binary GIVEN. Supply explicit
  `--models` so missing models cannot silently disappear.
- `manipulation`: the same fields plus `channel` (C3/C4), 100 paired items per
  model/channel. Separation is GIVEN(P) minus GIVEN(R).
- `label-gate`: the actual task-4 `validate` JSON report; does not accept a bare
  `gate_pass: true`. Rechecks metrics, uncertainty, and annotation completeness.
- `pilot` and `analyze`: task-4 scored JSONL (nested `scoring`) or flat synthetic
  outcomes. Required metadata: item/family/model/channel/direction/condition/
  history_type/remedy. Outcomes: `y`, `refuse_proxy`, and known `truncated=false`.
  Requires all five primary cells × two directions × C3/C4 × supplied models.
  Filter descriptive records explicitly. Duplicate rows, missing cells, unknown
  truncation, and unresolved truncation cause an error, never silent pair deletion.

```sh
python -m study_tools screen screen.jsonl runs/screen.json --models M1 M2 M3 M4
python -m study_tools manipulation manipulation.jsonl runs/manipulation.json --models M1 M2 M3 M4
python -m study_tools label-gate validation-report.json
python -m study_tools pilot scored-exploration.jsonl --models M1 M2 M3 M4
python -m study_tools analyze scored-final.jsonl runs/analysis.json --items final-items.jsonl --models M1 M2 M3 M4
```

## Explicit gate choices requiring review before freezing

`gates_v0.json` is a versioned **development** configuration. Use
`freeze-config NEW.json --reviewer NAME` after methodological review; it records
the reviewer, UTC time, and parent hash. Supply it with `--config NEW.json` before
the subcommand. Reports include the exact configuration hash. A frozen flag does
not claim preregistration or empirical validation.

| Gate | Implementation |
|---|---|
| Family pooled lower ≥ .85 for both policies | Mean of simultaneous per-model one-sided exact Clopper–Pearson lower bounds, Bonferroni across models, default alpha .05. Conservative, permits correlated models on shared items. Not an independence-assuming pooled binomial interval. |
| No clearly failing model | Per-model one-sided 90% exact upper bound must not fall below .80. |
| Manipulation separation ≥ .50 | One-sided 95% family-cluster CR2 lower bound in each primary channel. Degenerate-variance fallback uses a conservative bounded-family Hoeffding bound. |
| Label validation | Sensitivity/specificity .90, refusal agreement .85, GIVEN and refusal kappas .80, complete pre-adjudication overlap ratings. |
| Pilot futility | FAIL only if both H1 direction estimates < .03 and both one-sided 95% upper bounds < .06. Prints only PASS or FAIL, not estimates. Undefined variance yields PASS (insufficient evidence of futility). |

The plan does not specify the family lower-bound level/method or pilot upper-bound
level. Those defaults above are implementation choices, not established protocol.
Model-specific screen bounds assume independent generated items within family.
All family-cluster methods assume independence between families; the template-quality
warning therefore matters. Screening replacements and exclusion decisions must be
archived by the study coordinator; this code reports failures but does not silently
replace families or pick favorable models.

## Statistical implementation

1. Pair the relevant cells within each item/model/channel/direction.
2. Average differences equally over the fixed supplied models and C3/C4; H6 also
   averages equally over directions. This produces one difference per item/test.
3. Fit an intercept-only mean with CR2 adjustment on family, using the independent
   homoskedastic working target. Satterthwaite/Bell–McCaffrey df are calculated from
   the adjusted quadratic form. They equal G−1 in the balanced special case, but
   are calculated generally. Confirmatory analysis requires equal family sizes.
4. Holm adjusts H1-L/T (one-sided), H3-L/T (two-sided), and H6 (one-sided).
5. TOST uses ±.05, alpha .01 **per side**, for each of those five contrasts.
6. H7a-L/T test added violations against .03; H7b tests added refusal-proxy rate
   against .05. Each uses one-sided alpha .05; the joint harm gate needs all three.
7. A family bootstrap resamples whole families, using common draws across tests.
   It retains paired item/model/channel structure. Its intervals are descriptive.

The analysis CLI also requires the frozen final item manifest (after history-collision
replacement), so dropping an entire item or family is detected. The Python API can
omit this only for synthetic/development use.

Ordinary 95% intervals are marginal, not Holm-adjusted. Models are fixed targets,
not a random sample of model developers. REFUSE remains a proxy. Zero estimated
variance is not converted into a significant result. Incomplete/truncated outcomes
need the separately prespecified sensitivity analysis; this implementation rejects
them rather than supplying a potentially misleading complete-case result. Per-model
or per-channel descriptive analyses and missingness worst-case bounds are not included
in this initial task-5 module.

The CR2 implementation is restricted to this intercept-only paired design. It is
not a general regression library. Tests compare it against independent dense-matrix
CR2 calculations with unequal clusters and the known balanced family-mean t-test.
`reference_cr2.R` supplies an optional independent clubSandwich cross-check; R was
not available in this environment, so that script has not been executed here.
Reference: [clubSandwich coef_test documentation](https://jepusto.github.io/clubSandwich/reference/coef_test.html).

## Power simulation and dry run

`simulate OUTPUT --repetitions 100` uses 40 families, four fixed synthetic model
IDs, 15 items/family, all primary cells, shared family/item effects, heterogeneous
slopes, and partially shared Bernoulli uniforms across paired cells. The grid spans
baseline .03/.10/.20 and increment scale 0/.05/.08. API parameters allow exploration
variance estimates to replace default SDs, and allow different family/item counts.
The increment scale is **not** guaranteed to equal the marginal effect; achieved
H1-L is reported. These assumptions require recalibration on exploration data.

`python dry_run.py` runs 40 replications per grid cell plus a label-shuffled scenario
and a 1,000-resample bootstrap example, writing only synthetic reports under `runs/`.
It computes joint harm success directly, never by multiplying marginal powers.
Invalid simulations are counted. Monte Carlo standard errors accompany rates.
New simulation reports also include exact binomial Monte Carlo intervals and the
rate of rejecting any of the five primary tests. These quantify simulation error,
not uncertainty in real study effects. `python null_check.py` runs a separate
200-replication null check with independent seeds at the low-baseline setting.
Forty replications are a smoke check, not a reliable publication power estimate;
use thousands once the assumptions and implementation have been reviewed.

No missingness is simulated in this first version. Tests instead verify rejection
of incomplete designs. The simulation is not an empirical reproduction of the
plan's earlier power claims. Review family dependence, target effect calibration,
and model/channel correlations before using it to choose the final study size.
