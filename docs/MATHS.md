# FacultyDesk Maths

Every algorithm in the system is written here before it is coded. Each section follows the same order: idea, formula, worked example, edge cases, complexity, proof (test names).

Conventions used everywhere:

- Time intervals are half-open: `[start, end)`. A class ending at 10:00 and another starting at 10:00 do not overlap.
- All stored times are UTC. Local time is `Asia/Kolkata` and is used only for input and display.

## 1. Time and Recurrence

### 1.1 Canonical Time Representation and Clock Invariant

1. **Idea**:
All internal timestamps, calculations, and persistence operate exclusively in timezone-aware Coordinated Universal Time (UTC). The wall-clock system clock is accessed exclusively via an injected `Clock` protocol to maintain deterministic, reproducible behavior in tests and eliminate clock skew anomalies. Conversion to local wall-clock time (`Asia/Kolkata`, IST = UTC + 05:30) occurs strictly at the I/O boundaries (parsing incoming user input and formatting API / UI responses).

2. **Formula and Invariants**:
Let $\mathcal{T}$ denote the set of timezone-aware datetimes.
Every time value $t$ within the system satisfies:
$$\operatorname{tz}(t) = \text{UTC}$$
Given an input local wall-clock timestamp $(d, \tau)$ in time zone $Z = \text{Asia/Kolkata}$, canonicalization is defined as:
$$t_{\text{utc}} = \operatorname{astimezone}(\operatorname{localize}(d, \tau, Z), \text{UTC})$$
For any injected clock $C \in \mathcal{C}$, the clock invariant is:
$$\forall C, \quad \operatorname{tz}(C.\operatorname{now}()) \equiv \text{UTC}$$
For a `FrozenClock` initialized or set to $t \in \mathcal{T}$ with $\operatorname{tz}(t) = \text{UTC}$:
$$C_{\text{frozen}}(t).\operatorname{now}() = t$$
and after an advance of duration $\Delta t$:
$$C_{\text{frozen}}(t).\operatorname{advance}(\Delta t) \implies C_{\text{frozen}}.\operatorname{now}() = t + \Delta t$$

3. **Worked Example**:
Input: `2026-10-27 10:00:00` in `Asia/Kolkata` (UTC+05:30).
Offset calculation:
$$10:00:00 - 05:30:00 = 04:30:00\text{ UTC}$$
Output stored and processed: `2026-10-27T04:30:00Z`.
Re-conversion for display in `Asia/Kolkata`:
$$04:30:00\text{ UTC} + 05:30:00 = 10:00:00\text{ IST}$$

4. **Edge Cases**:
- Naive datetime passed to `FrozenClock`: Rejected with a domain `TypeError` or `ValueError`; timezone awareness is mandatory.
- Non-UTC timezone passed to `FrozenClock`: Automatically converted to UTC or validated to enforce UTC canonicalization.
- Leap seconds and daylight saving transitions: Indian Standard Time (IST) does not observe DST ($\Delta_{\text{DST}} = 0$). UTC has a constant progression.

5. **Complexity**:
- Time complexity: $O(1)$ for clock read, conversion, and advance.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_clock_always_returns_utc_property`: Hypothesis test proving that `Clock.now().tzinfo == timezone.utc` for random inputs.
- `test_frozen_clock_advance_property`: Hypothesis test proving $C(t + \Delta) = C(t) + \Delta$.
- `test_frozen_clock_rejects_naive_datetime`: Unit test proving naive datetimes are rejected.


## 2. Clash Detection

## 3. Reminder Scheduling

## 4. Exactly-Once Delivery

## 5. Initials and Name Matching

## 6. OCR Confidence

## 7. Date and Time Extraction

## 8. Task Priority and Alerts

## 9. Retry Backoff

## 10. Security Limits
