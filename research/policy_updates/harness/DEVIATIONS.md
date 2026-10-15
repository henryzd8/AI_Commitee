# Deviations and interpretations

Record every departure from `policy_updates_workshop_design.md`. Each entry needs:

- the date;
- what changed;
- the reason;
- who approved it.

Interpretations of points the design leaves open are listed separately, so the lead can confirm them.

## Interpretations awaiting lead confirmation (Task 3, 2026-10-14)

1. **Recognition channel assignment.** The design says "150 items per direction, in C3 and C4" and budgets about 0.9k recognition calls per model.
   - **Implemented:** each item is asked in *one* of C3/C4, alternating (`recognition.channel_assignment: split`). This matches the 0.9k budget.
   - **Alternative:** `both` doubles the calls.
2. **Recognition calibration** ("calibration uses the static cells").
   - **Implemented:** the same question after a NOOP × NEW-SELF prefix (policy unchanged), on the same items. This adds ~0.9k calls per model.
   - **Alternative:** ask the question in no-history static frames. Lead to choose.
3. **C3 tool results.**
   - **Implemented:** the turn-0 result carries only the policy. The switch-point result carries the policy plus the note "Course staff updated the policy.", identically in SWITCH and NOOP (handbook §5.2).
4. **C4 clock convention** (DRAFT, co-owned with Task 2):
   - SWITCH turns are 5 min apart, T is 5 min after turn 4, and turn 5 = T + 10 min.
   - NOOP turns 1–4 fall at T+2…T+5 min, and turn 5 is the same time as in SWITCH.
   - The rule text and current time are therefore identical across frames.
5. **C4 manipulation check:**
   - **Implemented:** the rule reads "Before T: other policy. From T on: delivered policy", with the single turn at T + 10 min.
6. **History generation prompt:**
   - **Implemented:** C1-style system prompt (role + policy + shared lines, with the C1 channel description "this system message").
7. **Truncation retry before Task 4's checker exists:**
   - **Implemented:** every truncated response is retried once at 2,048 tokens. This costs extra calls only, and attempt 1 is always kept.
   - Downstream response selection uses Task 4's disclosure rule. Once Task 4 delivers the checker, pass it to the runner so only no-disclosure truncations are retried, as the design specifies.

## Deviations

*(none yet)*
