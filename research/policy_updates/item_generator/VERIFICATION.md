# Usability rewrite verification — 2026-10-15

- All 15 task-1 tests pass, including the original generator checks and new usability tests.
- A fingerprint captured before refactoring matches 400 generated examples after
  refactoring (40 probe families + 40 history families, five examples each): IDs,
  question text, intermediate values, and final answers are unchanged for the
  saved string seed/split. The source fingerprint intentionally changes.
- A separate branched ticket-revenue template works through the common
  ProblemFamily interface without changing the generation engine.
- The one-command development workflow creates 100 probes, 400 linked history
  problems, raw records, runner exports, a catalog snapshot, and file checksums.
- Task-3 exports parse using the actual `pu.schemas.Item` implementation. No
  end-to-end model execution or GPU test was performed.
- Tests cover registry reordering, invalid definitions, solver disagreement,
  repeated collision checks retaining the original histories, no-overwrite behavior,
  clear CLI errors, and confirmatory guards without generating confirmatory items.
- A local 0.2.0 wheel builds successfully and includes all 40 pair definitions and
  the `policy-items` command entry point. No global package installation was needed.

The original candidate family quality limitations remain. Editing definitions still
requires human review and empirical screening; passing these software tests does not
establish 40 independent reasoning families. No task-1 PR was submitted for this rewrite.
