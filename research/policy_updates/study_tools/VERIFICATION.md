# Development verification — 2026-10-14

## Executed checks

- 19 new tests pass, plus all 28 existing checker tests (47 total).
- Replayed five instances from each of 80 candidate families (400 checks), including
  the independent text solver, answer bounds, intermediate-value constraints, and
  exclusion of final answers from numbers printed in the problems.
- Generated and checked development screening/exploration/manipulation/validation
  splits. Tested confirmatory allocation and its refusal without registration;
  **no confirmatory item set was generated**.
- Tested history collisions against fake histories, retained paraphrases, the four
  history-problem export, and existing-checker-to-analysis integration.
- Checked CR2 against a separately implemented dense-matrix reference with unequal
  cluster sizes and a known balanced family-mean t-test result.
- Checked Holm values, equivalence/non-inferiority boundary signs, blinding,
  missing/duplicate/truncated observations, and missing whole items against a manifest.
- A synthetic 600-item, 40-family, four-model analysis with 1,000 family-bootstrap
  draws completed. All outcomes are simulated; this is not the confirmatory set.
- Ran 40 replications in each of nine baseline/effect settings plus 40 with shuffled
  condition labels (400 total). No invalid replicate was reported.

## What the initial simulation does and does not establish

The 40-replication, 3%-baseline null scenario rejected H1-L in 4/40 runs; the other
two null baselines rejected H1-L in 2/40 and 1/40. These small batches do not certify
nominal error control. A separately seeded 200-replication follow-up completed at
the 3%-baseline null setting with no invalid replicates:

- H1-L: 2/200 rejections (1%); H1-T: 2/200; H3-L: 3/200; H3-T: 0/200; H6: 1/200.
- At least one primary rejection: 8/200 (4%), with an exact 95% Monte Carlo interval
  of 1.74%–7.73%. This is consistent with nominal 5% familywise error, not proof of
  calibration under every possible dependence pattern.
- Mean estimated H1-L: 0.000516 (about 0.052 percentage points).

There were 600 simulation replications altogether (400 initial, 200 follow-up).

All six nonzero-effect scenarios detected H1-L in 40/40 runs, and the synthetic
joint harm gate passed in 40/40 in each scenario. These optimistic figures are
conditional on the chosen correlation and heterogeneity assumptions. They do not
validate the original proposal's power estimates. Do not use them to promise study
power or shrink the sample. Shuffled-label runs rejected none of the primary tests.

Runtime: Python 3.14.3, NumPy 2.4.2, SciPy 1.17.1. Reproduction scripts are
`dry_run.py` and `null_check.py`; raw synthetic reports remain in ignored `runs/`.
The R/clubSandwich reference script was not executed because R was unavailable.

## Remaining research work

- Human review and substantive differentiation of candidate families, followed by
  empirical static screening. Automated mathematical checks are not human review.
- Committee review/freeze of confidence-bound defaults, paraphrases, and gate config.
- Real-response manipulation and annotation checks; generator/runner integration.
- Exploration-calibrated dependence/effect assumptions and a much larger power run.
- Prespecified treatment of incomplete/truncated outcomes; the current analysis
  rejects these rather than silently removing them.
