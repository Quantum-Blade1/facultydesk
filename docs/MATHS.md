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


### 1.2 Half-Open Interval Invariant and Overlap Arithmetic

1. **Idea**:
All scheduling intervals (time slots, event durations, academic terms, and quiet hour boundaries) are represented as half-open intervals $[t_{\text{start}}, t_{\text{end}})$. The interval includes the start instant $t_{\text{start}}$ and excludes the end instant $t_{\text{end}}$. This ensures that back-to-back consecutive events (e.g. 09:00–10:00 followed by 10:00–11:00) share no common points and never trigger a false conflict.

2. **Formula and Invariants**:
Let $I = [t_{\text{start}}, t_{\text{end}})$ be a temporal interval.
- **Strict Positivity Invariant**:
$$t_{\text{start}} < t_{\text{end}}$$
Any interval with $t_{\text{start}} \ge t_{\text{end}}$ violates domain invariants and raises `InvariantViolation`.

- **Intersection Condition**:
Two half-open intervals $I_1 = [s_1, e_1)$ and $I_2 = [s_2, e_2)$ overlap if and only if:
$$\operatorname{overlap}(I_1, I_2) \iff \max(s_1, s_2) < \min(e_1, e_2)$$
Equivalently:
$$\operatorname{overlap}(I_1, I_2) \iff (s_1 < e_2) \land (s_2 < e_1)$$

- **Boundary Condition (Adjacent intervals)**:
If $e_1 = s_2$, then $\max(s_1, s_2) = s_2$ and $\min(e_1, e_2) = e_1 = s_2$. Because $s_2 < s_2$ is false:
$$\operatorname{overlap}([s_1, e_1), [e_1, e_2)) = \text{False}$$

3. **Worked Example**:
- Event A: 09:00 to 10:00 ($s_1 = 09:00, e_1 = 10:00$).
- Event B: 10:00 to 11:00 ($s_2 = 10:00, e_2 = 11:00$).
$$\max(09:00, 10:00) = 10:00, \quad \min(10:00, 11:00) = 10:00$$
$$10:00 < 10:00 \implies \text{False (no clash)}$$
- Event C: 09:30 to 10:30 ($s_3 = 09:30, e_3 = 10:30$).
$$\max(09:00, 09:30) = 09:30, \quad \min(10:00, 10:30) = 10:00$$
$$09:30 < 10:00 \implies \text{True (clash detected over }[09:30, 10:00)\text{)}$$

4. **Edge Cases**:
- Point intervals ($s = e$): Disallowed by strict inequality $s < e$. Zero-duration events must be represented as instantaneous markers or explicit deadlines, not intervals.
- Day boundary crossings for local time: Local recurring time slots like `QuietHours` (e.g. 22:00 to 07:00) cross midnight. A crossing quiet hour is partitioned into two disjoint half-open intervals in wall-clock day coordinates: $[s, 24:00)$ and $[00:00, e)$.

5. **Complexity**:
- Time complexity: $O(1)$ comparisons.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_interval_start_must_precede_end`: Hypothesis test proving $s \ge e$ raises `InvariantViolation`.
- `test_half_open_interval_adjacent_no_overlap`: Property test proving $[s_1, m)$ and $[m, e_2)$ never overlap.
- `test_half_open_interval_overlapping_pair`: Property test proving overlap occurs iff $s_1 < e_2 \land s_2 < e_1$.

### 1.3 State Machine Transition Algebras

1. **Idea**:
Aggregates with lifecycles (`Circular`, `ScheduledNotification`) follow deterministic finite state automata. A transition from state $s$ to state $s'$ is permitted if and only if $(s, s') \in \delta$. All other pairs in $S \times S$ are strictly forbidden and immediately raise `InvalidTransition`.

2. **Transition Specifications**:

#### Circular State Machine
State set:
$$S_{\text{circ}} = \{\text{UPLOADED}, \text{PROCESSING}, \text{NEEDS\_REVIEW}, \text{CONFIRMED}, \text{REJECTED}, \text{FAILED}\}$$
Initial state: $s_0 = \text{UPLOADED}$.
Permitted transition relation $\delta_{\text{circ}} \subset S_{\text{circ}} \times S_{\text{circ}}$:
$$\begin{aligned}
\delta_{\text{circ}} = \{ &(\text{UPLOADED}, \text{PROCESSING}), \\
&(\text{PROCESSING}, \text{NEEDS\_REVIEW}), \\
&(\text{PROCESSING}, \text{CONFIRMED}), \\
&(\text{PROCESSING}, \text{FAILED}), \\
&(\text{NEEDS\_REVIEW}, \text{CONFIRMED}), \\
&(\text{NEEDS\_REVIEW}, \text{REJECTED}), \\
&(\text{FAILED}, \text{PROCESSING}) \}
\end{aligned}$$
Total pairs in $S \times S$: $|S_{\text{circ}}|^2 = 6 \times 6 = 36$.
Legal transitions: $|\delta_{\text{circ}}| = 7$.
Illegal transitions: $36 - 7 = 29$.

#### ScheduledNotification State Machine
State set:
$$S_{\text{notif}} = \{\text{PENDING}, \text{SENDING}, \text{SENT}, \text{FAILED}, \text{CANCELLED}\}$$
Initial state: $s_0 = \text{PENDING}$.
Permitted transition relation $\delta_{\text{notif}} \subset S_{\text{notif}} \times S_{\text{notif}}$:
$$\begin{aligned}
\delta_{\text{notif}} = \{ &(\text{PENDING}, \text{SENDING}), \\
&(\text{SENDING}, \text{SENT}), \\
&(\text{SENDING}, \text{FAILED}), \\
&(\text{FAILED}, \text{PENDING}), \\
&(\text{PENDING}, \text{CANCELLED}) \}
\end{aligned}$$
Retry bound invariant: A transition $(\text{FAILED}, \text{PENDING})$ is permitted only if $\text{attempts} < \text{max\_attempts}$.
Total pairs in $S \times S$: $|S_{\text{notif}}|^2 = 5 \times 5 = 25$.
Legal transitions: $|\delta_{\text{notif}}| = 5$.
Illegal transitions: $25 - 5 = 20$.

3. **Worked Example**:
A circular in state `UPLOADED` attempting transition to `CONFIRMED`:
$$(\text{UPLOADED}, \text{CONFIRMED}) \notin \delta_{\text{circ}} \implies \text{raise InvalidTransition}$$
The circular must first transition $\text{UPLOADED} \to \text{PROCESSING}$, then $\text{PROCESSING} \to \text{CONFIRMED}$ or $\text{PROCESSING} \to \text{NEEDS\_REVIEW} \to \text{CONFIRMED}$.

4. **Edge Cases**:
- Reflexive transitions $(s, s)$: Not permitted in $\delta$. Re-entering the identical state is a no-op or error, rejecting duplicate transition dispatches.
- Retrying a notification exceeding maximum retry count: Transition $(\text{FAILED}, \text{PENDING})$ is disallowed if $\text{attempts} \ge \text{max\_attempts}$.

5. **Complexity**:
- Time complexity: $O(1)$ set membership test.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_circular_state_machine_exhaustive`: Cartesian product property test over all 36 $(s_1, s_2) \in S_{\text{circ}} \times S_{\text{circ}}$, verifying that exactly the 7 transitions succeed and the remaining 29 raise `InvalidTransition`.
- `test_notification_state_machine_exhaustive`: Cartesian product property test over all 25 $(s_1, s_2) \in S_{\text{notif}} \times S_{\text{notif}}$, verifying that exactly the 5 transitions succeed and the remaining 20 raise `InvalidTransition`.

## 2. Clash Detection

## 3. Reminder Scheduling

## 4. Exactly-Once Delivery

## 5. Initials and Name Matching

### 5.1 Initials Value Object Invariant

1. **Idea**:
Faculty members are referenced in academic timetables and departmental circulars by standard initials (e.g., `KKS`, `CN`, `RSV`). An Initials value object enforces formatting constraints at construction time, preventing corrupted strings from entering the domain.

2. **Formula and Invariants**:
Let $\Sigma = \{A, B, C, \dots, Z\}$ be the set of uppercase Latin alphabetic characters.
An initials string $I$ satisfies:
$$I \in \Sigma^+ \quad \land \quad 2 \le |I| \le 5$$
Regex representation:
$$I \in \mathcal{L}(\verb!^[A-Z]{2,5}$!)$$
Department-level uniqueness constraint:
$$\forall p_1, p_2 \in \text{FacultyProfile}, \quad (p_1.\text{department\_id} = p_2.\text{department\_id} \land p_1.\text{initials} = p_2.\text{initials}) \implies p_1.\text{id} = p_2.\text{id}$$

3. **Worked Example**:
- Valid initials: `"KKS"` ($|I| = 3, \text{all uppercase}$), `"CN"` ($|I| = 2$), `"ABCDE"` ($|I| = 5$).
- Invalid initials:
  - `"kks"`: lower case $\implies$ raises `InvariantViolation`.
  - `"K"`: length $1 < 2 \implies$ raises `InvariantViolation`.
  - `"ABCDEF"`: length $6 > 5 \implies$ raises `InvariantViolation`.
  - `"K.K.S."`: punctuation $\notin \Sigma \implies$ raises `InvariantViolation`.

4. **Edge Cases**:
- Whitespace surrounding input: In constructor, whitespace is stripped and uppercase normalized or rejected if normalization is outside value object scope. We reject non-matching raw strings or enforce normalized uppercase.
- Non-ASCII unicode characters: Rejected. Only $[A-Z]$ allowed.

5. **Complexity**:
- Time complexity: $O(|I|) = O(1)$ since $|I| \le 5$.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_initials_valid_property`: Hypothesis test generating strings of 2–5 uppercase letters, verifying valid instantiation.
- `test_initials_invalid_property`: Hypothesis test generating invalid strings (length $< 2$ or $> 5$, numbers, lowercase, symbols), verifying `InvariantViolation`.

## 6. OCR Confidence

## 7. Date and Time Extraction

## 8. Task Priority and Alerts

## 9. Retry Backoff

## 10. Security Limits

### 10.1 Token Lifetimes, Rotation, and Family Reuse Detection

1. **Idea**:
Authentication uses short-lived access JWTs (15 minutes) and long-lived refresh tokens (7 days). Every refresh token belongs to a cryptographically tracked token family $\mathcal{F}$. Upon every refresh request, the presenting token is immediately consumed (invalidated) and replaced with a newly minted child token in the same family. If an already-consumed token is presented again (indicating token theft or replay), the system detects a breach and revokes every active token in family $\mathcal{F}$.

2. **Formula and Invariants**:
Let a refresh token $T_k$ be represented as:
$$T_k = (h_k, \mathcal{F}, \text{revoked}_k, \text{exp}_k)$$
where:
- $\text{raw}_k \xleftarrow{\$} \{0, 1\}^{256}$ is a random 256-bit cryptographically secure token.
- $h_k = \operatorname{SHA-256}(\text{raw}_k)$ is the stored database hash.
- $\mathcal{F} \in \text{UUID}$ is the family identifier shared across all rotations.
- $\text{revoked}_k \in \{\text{True}, \text{False}\}$.
- $\text{exp}_k = t_{\text{issued}} + \Delta_{\text{refresh}}$ where $\Delta_{\text{refresh}} = 7\text{ days}$.

**Valid Rotation State Transition**:
Given client token $\text{raw}$ presented at time $t$:
$$\begin{aligned}
h(\text{raw}) = h_k \land \neg \text{revoked}_k \land (t < \text{exp}_k) \implies \{ \\
&\text{revoked}_k \leftarrow \text{True}, \\
&\text{issue } T_{k+1} = (\operatorname{SHA-256}(\text{raw}_{k+1}), \mathcal{F}, \text{False}, t + \Delta_{\text{refresh}}), \\
&\text{issue } \text{JWT}_{\text{access}} \text{ with exp} = t + 15\text{ minutes} \\
\}
\end{aligned}$$

**Reuse Detection and Family Revocation**:
$$\begin{aligned}
h(\text{raw}) = h_k \land \text{revoked}_k = \text{True} \implies \{ \\
&\forall T \in \mathcal{F}, \quad T.\text{revoked} \leftarrow \text{True}, \\
&\text{raise } \text{UnauthorizedError}(\text{"Compromised token family detected"}) \\
\}
\end{aligned}$$

3. **Worked Example**:
- Client logs in: Family $\mathcal{F}_1$ created with token $T_1$.
- 1st Refresh: Client presents $T_1$. Valid. $T_1$ marked revoked. $T_2$ issued in $\mathcal{F}_1$.
- Attacker steals and presents $T_1$:
  $T_1.\text{revoked} == \text{True} \implies$ Reuse detected!
  $T_2$ is immediately marked revoked. Family $\mathcal{F}_1$ terminated.
  Legitimate user's next request fails, prompting fresh login.

4. **Edge Cases**:
- Expired non-revoked token presented: Rejected with standard 401; does not trigger whole family revocation unless consumed token was presented.
- Concurrent requests with identical token: Database row-level lock or unique constraint on consumed state ensures atomic transition.

5. **Complexity**:
- Time complexity: $O(1)$ lookup via index on `token_hash`, $O(m)$ update where $m$ is number of tokens in family ($m \le 100$).
- Space complexity: $O(1)$ per token.

6. **Proof Plan**:
- `test_refresh_token_rotation_success`: Integration test verifying $T_k \to T_{k+1}$ transition.
- `test_refresh_token_reuse_revokes_family`: Integration test proving reuse of $T_k$ revokes $T_{k+1}$ and invalidates future requests.

### 10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix

1. **Idea**:
Authorization decisions are evaluated by a centralized `AuthorisationPolicy` object in the application layer before any use case execution. The policy strictly binds `FACULTY` to their own records, `HOD` to their own department, and `ADMIN` to system-wide administration.

2. **Formula and Invariants**:
Let Principal $P = (u_P, r_P, d_P)$ where $u_P \in \text{UUID}$ is user ID, $r_P \in \{\text{ADMIN}, \text{HOD}, \text{FACULTY}\}$ is role, and $d_P \in \text{UUID}$ is department ID.
Let Resource $R = (u_R, d_R)$ where $u_R$ is resource owner user ID and $d_R$ is resource department ID.

The permission predicate $\operatorname{Permit}(P, R, \text{action})$ is defined by:
$$\operatorname{Permit}(P, R, \text{action}) = \begin{cases}
\text{True} & \text{if } r_P = \text{ADMIN} \\
d_P = d_R & \text{if } r_P = \text{HOD} \\
u_P = u_R & \text{if } r_P = \text{FACULTY} \\
\text{False} & \text{otherwise}
\end{cases}$$

Policy Truth Table:
| Principal Role | Resource Owner | Resource Dept | Result |
|---|---|---|---|
| `ADMIN` | Any | Any | `ALLOW` |
| `HOD` | Any | Matches HOD Dept | `ALLOW` |
| `HOD` | Any | Differs from HOD Dept | `DENY (403)` |
| `FACULTY` | Matches Faculty User | Any | `ALLOW` |
| `FACULTY` | Differs from Faculty User | Any | `DENY (403)` |

3. **Worked Example**:
- Principal: Faculty Alice ($u_A, \text{FACULTY}, d_1$).
- Resource: Task assigned to Bob ($u_B, d_1$).
$$u_A = u_B \implies \text{False} \implies \operatorname{Permit} = \text{False (403 Forbidden)}$$

4. **Edge Cases**:
- Unassigned or null department on resource: Disallowed for HOD, allowed for ADMIN.
- Inactive user: Rejected at authentication boundary before policy evaluation.

5. **Complexity**:
- Time complexity: $O(1)$ boolean evaluation.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_policy_matrix_exhaustive`: Unit test verifying all permutations in the RBAC policy truth table.

### 10.3 Sliding Window Log Rate Limiting

1. **Idea**:
Rate limiting protects sensitive endpoints (`/api/auth/login`, `/api/auth/refresh`) against brute-force and resource exhaustion attacks. We employ the **Sliding Window Log** algorithm backed by Redis sorted sets (ZSET). Unlike Fixed Window, Sliding Window Log has no boundary burst anomalies (where double the limit can be sent across the boundary of two minutes).

2. **Formula and Invariants**:
Let $K$ be the rate limit key (e.g., `rate_limit:login:ip:<ip>` or `rate_limit:login:account:<email>`).
Let $W$ be the sliding window duration in seconds ($W = 60\text{s}$).
Let $L$ be the request capacity ($L_{\text{login}} = 5, L_{\text{refresh}} = 30$).
Let $t$ be the current epoch timestamp in milliseconds.

The window interval is:
$$I_{\text{window}} = (t - W \times 1000, t]$$
**Algorithm Execution (Atomic Redis Multi/Exec Pipeline)**:
1. Prune expired entries:
   $$\operatorname{ZREMRANGEBYSCORE}(K, 0, t - W \times 1000)$$
2. Count remaining entries in window:
   $$c = \operatorname{ZCARD}(K)$$
3. If $c < L$:
   $$\operatorname{ZADD}(K, t, \text{request\_uuid}), \quad \operatorname{EXPIRE}(K, W + 1)$$
   $$\implies \text{ALLOW}$$
4. Else:
   $$\implies \text{DENY (429 Too Many Requests)}$$

3. **Worked Example**:
$L = 5, W = 60\text{s}$.
Client sends 5 requests at $t = 10\text{s}, 15\text{s}, 20\text{s}, 25\text{s}, 30\text{s}$.
At $t = 35\text{s}$:
$\operatorname{ZCARD} = 5 \nless 5 \implies \text{DENY (429)}$.
At $t = 72\text{s}$:
Prune elements $\le 72 - 60 = 12\text{s}$. The request at $t = 10\text{s}$ is pruned.
$\operatorname{ZCARD} = 4 < 5 \implies \text{ALLOW}$.

4. **Edge Cases**:
- Clock drift across instances: Redis server epoch time is used as canonical reference.
- Redis connection unavailability: Fail-open or fallback to in-memory sliding window cache.

5. **Complexity**:
- Time complexity: $O(\log N + M)$ where $N$ is entries in set and $M$ is expired entries pruned ($N \le L \le 30$). Negligible overhead ($< 1\text{ms}$).
- Space complexity: $O(L)$ per active key in Redis.

6. **Proof Plan**:
- `test_sliding_window_rate_limiter`: Unit/integration test proving requests up to $L$ succeed and request $L+1$ within $W$ returns 429.
