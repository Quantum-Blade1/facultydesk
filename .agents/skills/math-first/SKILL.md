---
name: math-first
description: Write the mathematical specification of an algorithm into docs/MATHS.md before implementing it, then prove the code matches with property tests. Use for recurrence, clashes, reminders, idempotency, matching, OCR confidence, priority scoring, backoff and any other computation.
---

# Math First

## Step 1: Specify

In the right section of `docs/MATHS.md`, write:

1. **Idea** in two or three plain sentences.
2. **Formula** with every symbol defined. Use inline code or simple LaTeX that renders on GitHub.
3. **Worked example** with concrete numbers or strings and the exact expected output.
4. **Edge cases**, each with the expected behaviour (empty input, boundaries, equal timestamps, end-of-term, midnight crossing, duplicate initials, OCR noise).
5. **Complexity** in time and space.
6. **Proof plan**: names of the tests that will prove it.

## Step 2: Test

Write the tests named in the proof plan before the implementation:

- One example test that reproduces the worked example exactly.
- One property test with hypothesis per invariant. Examples of invariants:
  - Clash detection agrees with brute-force pairwise check on random interval sets.
  - Every generated recurrence date falls on the slot weekday, lies within the term, and is not a holiday.
  - Fire times are strictly before the event and strictly after now.
  - Idempotency keys are equal iff their four inputs are equal.
  - Similarity is symmetric, in [0, 1], and equals 1 iff strings are equal after normalisation.
  - Backoff delay is in [0, cap].
- Edge-case tests for each listed edge case.

Run them and confirm they fail for the right reason.

## Step 3: Implement

Write the smallest code that makes the tests pass and reads like the formula. Variable names should mirror the symbols in MATHS.md.

## Step 4: Prove

Run the tests, paste output into the stage report, and tick the proof plan in MATHS.md.
