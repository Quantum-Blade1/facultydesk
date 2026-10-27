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

### 1.4 Recurrence Expansion and Rolling 21-Day Materialisation Window

1. **Idea**:
Timetable slots define recurring weekly classes associated with an academic term. Materialising the entire term (often 16 to 20 weeks) up front creates hundreds of redundant event records, complicates timetable updates, and produces dead rows if a timetable is revised mid-term. Conversely, computing occurrences on the fly on every calendar request and reminder query requires expensive rule evaluation and repeated holiday lookups on hot API paths. FacultyDesk adopts a deterministic rolling 21-day materialisation window: occurrences are materialised in the database for $[D_{\text{today}}, D_{\text{today}} + 21\text{ days}]$, refreshed nightly by a Celery Beat task and immediately upon timetable confirmation.

2. **Formula and Invariants**:
Let $T = [D_{\text{term\_start}}, D_{\text{term\_end}}]$ be the academic term date range.
Let $w \in \{0, 1, 2, 3, 4, 5, 6\}$ be the zero-indexed day of the week ($0 = \text{Monday}, \dots, 6 = \text{Sunday}$).
Let $H = \{h_1, h_2, \dots, h_m\}$ be the set of holiday dates within the term.
The full theoretical recurrence set $R(w, T, H)$ is defined as:
$$R(w, T, H) = \{ d \in [D_{\text{term\_start}}, D_{\text{term\_end}}] \mid \operatorname{weekday}(d) = w \} \setminus H$$

For a current local date $D_{\text{today}}$ in `Asia/Kolkata`, the rolling 21-day window is defined as:
$$W_{21}(D_{\text{today}}) = [D_{\text{today}}, D_{\text{today}} + 21\text{ days}]$$
The materialisation date set $M$ for slot $s$ is the intersection:
$$M(s, D_{\text{today}}) = R(s.\text{day\_of\_week}, T, H) \cap W_{21}(D_{\text{today}})$$

For each $d \in M(s, D_{\text{today}})$:
Given slot wall-clock time boundaries $[\tau_{\text{start}}, \tau_{\text{end}})$ with $\tau_{\text{start}} < \tau_{\text{end}}$:
1. Combine into local timezone-aware datetimes in $Z = \text{Asia/Kolkata}$:
$$L_{\text{start}} = \operatorname{datetime}(d, \tau_{\text{start}}, \operatorname{ZoneInfo}(Z))$$
$$L_{\text{end}} = \operatorname{datetime}(d, \tau_{\text{end}}, \operatorname{ZoneInfo}(Z))$$
2. Convert to canonical UTC:
$$U_{\text{start}} = \operatorname{astimezone}(L_{\text{start}}, \text{UTC})$$
$$U_{\text{end}} = \operatorname{astimezone}(L_{\text{end}}, \text{UTC})$$

Idempotent Upsert Invariant:
Every materialised timetable class event is keyed by the tuple:
$$K = (\text{slot\_id}, d)$$
where $\text{slot\_id} = s.\text{id}$ and $d \in M(s, D_{\text{today}})$.
A second materialisation run on the same date window performs an idempotent `DO NOTHING` or update, guaranteeing zero duplicates.

3. **Worked Example**:
- Term: 2026-08-01 to 2026-12-15.
- Slot: Wednesday ($w = 2$), 10:00 to 11:45 IST.
- Holiday: Wednesday 2026-10-28 (Diwali Holiday).
- Current date: Monday 2026-10-26.
- Window $W_{21}$: $[2026-10-26, 2026-11-16]$.
Candidate Wednesdays in window:
- 2026-10-28: in holiday set $H \implies$ skipped.
- 2026-11-04: $\notin H \implies$ materialised:
  - Local: `2026-11-04 10:00:00+05:30` to `2026-11-04 11:45:00+05:30`
  - UTC: `2026-11-04T04:30:00Z` to `2026-11-04T06:15:00Z`.
- 2026-11-11: $\notin H \implies$ materialised:
  - Local: `2026-11-11 10:00:00+05:30` to `2026-11-11 11:45:00+05:30`
  - UTC: `2026-11-11T04:30:00Z` to `2026-11-11T06:15:00Z`.

4. **Edge Cases**:
- Term boundaries: If $D_{\text{today}} + 21\text{ days} > D_{\text{term\_end}}$, occurrences truncate at $D_{\text{term\_end}}$.
- Slot removal or revision: When a timetable is re-confirmed or slots are replaced, future materialised events ($start\_utc \ge now$) from old slots are deleted before generating new ones.

5. **Complexity**:
- Time complexity: For $S$ slots over $K \le 4$ weeks, $O(S \cdot K)$ date calculations. With $S \approx 50$, $50 \times 4 = 200$ operations ($< 5\text{ ms}$).
- Space complexity: $O(S \cdot K)$ rows.

6. **Proof Plan**:
- `test_recurrence_expansion_skips_holidays`: Property test verifying no generated date matches $H$.
- `test_recurrence_expansion_matching_weekday`: Property test verifying $\operatorname{weekday}(d) = w$ for all generated dates.
- `test_recurrence_expansion_utc_roundtrip`: Property test verifying $U_{\text{start}} \to Z \equiv (d, \tau_{\text{start}})$.

## 2. Clash Detection and Calendar Operations

### 2.1 Half-Open Overlap Predicate

1. **Idea**:
Two events conflict if and only if their active intervals share at least one non-zero duration temporal intersection. Using half-open intervals $[s, e)$, adjacent events where $e_1 = s_2$ do not clash.

2. **Formula**:
$$\operatorname{overlap}(I_1, I_2) \iff (I_1.\text{start} < I_2.\text{end}) \land (I_2.\text{start} < I_1.\text{end})$$
For attendee $f$, events $E_1, E_2$ clash iff $f \in E_1.\text{attendees} \land f \in E_2.\text{attendees} \land \operatorname{overlap}(E_1, E_2)$.

### 2.2 Sweep-Line Interval Clash Detection Algorithm

1. **Idea**:
Detecting all pairwise clashes among $n$ events by brute force takes $O(n^2)$. Using a sweep-line algorithm with a priority queue (min-heap), active events are maintained as the sweep line moves forward in time, achieving $O(n \log n + k)$ where $k$ is the number of reporting clashes.

2. **Algorithm**:
- Input: Array of $n$ events $E = [e_1, e_2, \dots, e_n]$, each with half-open interval $[s_i, e_i)$.
- Step 1: Sort $E$ by start time ascending: $s_1 \le s_2 \le \dots \le s_n$.
- Step 2: Initialize min-heap $H = \emptyset$, where each node is $(e_j, j)$, keyed by interval end time $e_j$.
- Step 3: For $i = 1$ to $n$:
  - While $H \ne \emptyset$ and $H.\operatorname{peek}().\text{end} \le s_i$:
    $H.\operatorname{pop}()$ (interval $j$ ended at or before $s_i$, cannot overlap $e_i$ or any subsequent event).
  - For every $(e_j, j) \in H$:
    Report clash $(e_j, e_i)$ (since $s_j \le s_i < e_j$ and $s_j < e_i$, intervals overlap).
  - $H.\operatorname{push}((e_i, i))$.
- Output: Set of all clashing event pairs $\mathcal{C}$.

3. **Worked Example**:
Events:
- $E_1: [09:00, 10:00)$
- $E_2: [09:30, 10:30)$
- $E_3: [10:00, 11:00)$
- $E_4: [10:15, 10:45)$

Trace:
- $i=1 (E_1)$: $H = \emptyset$. Push $(10:00, E_1)$. $H = \{(10:00, E_1)\}$.
- $i=2 (E_2)$: $s_2 = 09:30 < 10:00$. No pop.
  - Check $H$: $E_1$ in $H \implies$ Report clash $(E_1, E_2)$.
  - Push $(10:30, E_2)$. $H = \{(10:00, E_1), (10:30, E_2)\}$.
- $i=3 (E_3)$: $s_3 = 10:00$.
  - While $H.\operatorname{peek}().\text{end} \le 10:00$: pop $(10:00, E_1)$.
  - Remaining in $H$: $\{(10:30, E_2)\}$.
  - $10:30 > 10:00 \implies$ Report clash $(E_2, E_3)$.
  - Push $(11:00, E_3)$. $H = \{(10:30, E_2), (11:00, E_3)\}$.
- $i=4 (E_4)$: $s_4 = 10:15$.
  - Min end in $H$ is $10:30 > 10:15$. No pop.
  - Report clashes: $(E_2, E_4)$ and $(E_3, E_4)$.
  - Push $(10:45, E_4)$.

Total Clashes Reported: $(E_1, E_2), (E_2, E_3), (E_2, E_4), (E_3, E_4)$.
Notice $(E_1, E_3)$ is NOT reported because $E_1$ ended at $10:00$ and $E_3$ started at $10:00$ (adjacent half-open intervals do not clash).

4. **Edge Cases**:
- Multiple events starting at the exact same instant $s_i = s_{i+1}$: Handled naturally; heap pop only occurs for $e_j \le s_i$.
- Enclosed intervals ($I_1 \subset I_2$): Correctly identified since $e_2 > s_1$.

5. **Complexity**:
- Time complexity: $O(n \log n)$ for sorting + $O(n \log k + C)$ heap operations where $k$ is maximum concurrency and $C$ is number of overlaps.
- Space complexity: $O(n)$ for event list and heap.

6. **Proof Plan**:
- `test_sweep_line_clash_detection_matches_pairwise_property`: Hypothesis property test comparing sweep-line results against $O(n^2)$ exhaustive pairwise checks across random intervals.
- `test_adjacent_intervals_no_clash`: Property test verifying $[s, m)$ and $[m, e)$ produce zero clashes.

### 2.3 Multi-Attendee Common Free-Slot Finder

1. **Idea**:
To schedule departmental meetings or collaborative reviews, the HOD or faculty member requires common free slots where all candidate attendees are available. The algorithm collects busy intervals of all attendees, merges overlapping or contiguous busy intervals, and computes the complement within daily working hours $[08:00, 18:00)$ in `Asia/Kolkata`. Any free interval with duration $\ge \Delta_{\text{req}}$ is returned.

2. **Algorithm**:
- Inputs:
  - Attendees $A = \{a_1, a_2, \dots, a_m\}$.
  - Search range: $[D_{\text{start}}, D_{\text{end}}]$.
  - Working hours in local time: $[\tau_{\text{start}}, \tau_{\text{end}})$ (e.g., $08:00$ to $18:00$).
  - Minimum duration: $\Delta_{\text{req}}$ minutes.
- Step 1 (Busy Interval Union):
  Query all events for each attendee $a \in A$ intersecting $[D_{\text{start}}, D_{\text{end}}]$.
  Form the union set of busy intervals:
  $$\mathcal{B} = \bigcup_{a \in A} \{ [e.\text{start\_utc}, e.\text{end\_utc}) \mid e \in \operatorname{events}(a) \}$$
- Step 2 (Merge Busy Intervals):
  Sort $\mathcal{B}$ by start time.
  Merge any overlapping or contiguous intervals:
  $$\text{if } s_{k+1} \le e_k \implies [s_k, \max(e_k, e_{k+1}))$$
  Result: ordered, disjoint busy intervals $\mathcal{M} = [ [s_1, e_1), [s_2, e_2), \dots, [s_p, e_p) ]$.
- Step 3 (Working Hours Complement):
  For each day $d \in [D_{\text{start}}, D_{\text{end}}]$:
  - Define local working window:
    $$W_d = [ \operatorname{combine}(d, \tau_{\text{start}}), \operatorname{combine}(d, \tau_{\text{end}}) )$$
  - Convert $W_d$ to UTC: $[w_s, w_e)$.
  - Intersect merged busy intervals with $[w_s, w_e)$.
  - Let intersecting busy blocks within the day be $[b_{1,s}, b_{1,e}), \dots, [b_{q,s}, b_{q,e})$.
  - Free gaps within working hours:
    - First candidate: $[w_s, b_{1,s})$ if $b_{1,s} > w_s$.
    - Middle candidates: $[b_{i,e}, b_{i+1,s})$ for $i=1 \dots q-1$.
    - Final candidate: $[b_{q,e}, w_e)$ if $w_e > b_{q,e}$.
    - If no busy intervals exist on date $d$: candidate is entire $[w_s, w_e)$.
  - Filter: keep candidate $[f_s, f_e)$ if $(f_e - f_s) \ge \Delta_{\text{req}}$.
- Output: List of valid free slots $[f_s, f_e)$ sorted chronologically.

3. **Worked Example**:
- Attendees: Faculty A and Faculty B.
- Date: 2026-10-27. Working hours: 09:00 to 17:00 IST ($03:30$ to $11:30$ UTC).
- Faculty A busy: 10:00–11:00 IST ($04:30$–$05:30$ UTC) and 14:00–15:30 IST ($08:30$–$10:00$ UTC).
- Faculty B busy: 10:30–12:00 IST ($05:00$–$06:30$ UTC).
- Merged busy intervals:
  - $[10:00, 11:00) \cup [10:30, 12:00) \implies [10:00, 12:00)$ IST.
  - $[14:00, 15:30)$ IST.
- Gaps in $[09:00, 17:00)$:
  1. $[09:00, 10:00)$ (duration 60 min).
  2. $[12:00, 14:00)$ (duration 120 min).
  3. $[15:30, 17:00)$ (duration 90 min).
- For $\Delta_{\text{req}} = 45\text{ min}$: all 3 gaps returned.
- For $\Delta_{\text{req}} = 90\text{ min}$: gaps 2 and 3 returned.

4. **Edge Cases**:
- Entire working day free: Full day $[w_s, w_e)$ returned.
- Entire working day busy: Empty list returned.
- Multiple attendees with disjoint schedules covering the whole day: Empty list returned.

5. **Complexity**:
- Time complexity: $O(N \log N)$ where $N$ is total events across all attendees.
- Space complexity: $O(N)$.

6. **Proof Plan**:
- `test_free_slots_never_intersect_busy_property`: Property test proving $\forall f \in \text{FreeSlots}, \forall b \in \mathcal{B}, \operatorname{overlap}(f, b) = \text{False}$.
- `test_free_slots_duration_bound_property`: Property test proving $(f.\text{end} - f.\text{start}) \ge \Delta_{\text{req}}$ for all returned slots.

### 2.4 RFC 5545 ICS Feed Specification

1. **Idea**:
Faculty calendar feeds must conform strictly to RFC 5545 Internet Calendaring and Scheduling Core Object Specification (iCalendar) to allow seamless subscription in Google Calendar, Apple Calendar, and Outlook. Feeds are exposed over an unauthenticated, token-gated HTTPS endpoint with a rotatable secret token.

2. **Specification Rules**:
- Container: `BEGIN:VCALENDAR ... END:VCALENDAR`.
- Required VCALENDAR properties:
  - `VERSION:2.0`
  - `PRODID:-//FacultyDesk//Academic Calendar//EN`
  - `CALSCALE:GREGORIAN`
  - `METHOD:PUBLISH`
  - `X-WR-CALNAME:FacultyDesk Schedule`
  - `X-WR-TIMEZONE:UTC`
- Event components (`BEGIN:VEVENT ... END:VEVENT`):
  - `UID`: Globally unique, stable identifier.
    - Timetable occurrences: `UID:slot-<slot_id>-<date>@facultydesk.local`
    - Meetings / manual events: `UID:event-<event_id>@facultydesk.local`
  - `DTSTAMP`: Current timestamp in UTC (`YYYYMMDDTHHMMSSZ`).
  - `DTSTART`: Event start in UTC (`YYYYMMDDTHHMMSSZ`).
  - `DTEND`: Event end in UTC (`YYYYMMDDTHHMMSSZ`).
  - `SUMMARY`: Sanitized event title.
  - `LOCATION`: Room code or meeting venue.
  - `STATUS:CONFIRMED`.
- Line folding: Lines longer than 75 octets are folded per RFC 5545 Section 3.1.
- Character escaping: Commas, semicolons, and backslashes in text fields are escaped with backslash.

3. **Worked Example**:
```text
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//FacultyDesk//Academic Calendar//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:FacultyDesk Schedule
BEGIN:VEVENT
UID:slot-4a94639e-2026-11-04@facultydesk.local
DTSTAMP:20261027T133000Z
DTSTART:20261104T043000Z
DTEND:20261104T061500Z
SUMMARY:CN (KKS)
LOCATION:LH-101
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR
```

4. **Edge Cases**:
- Special characters in title or location (e.g. `Lab A & B, Room 101`): Escaped per RFC 5545.
- Token rotation: When token is rotated, the old token immediately returns HTTP 404, preventing unauthorized access.

5. **Complexity**:
- Time complexity: $O(E)$ where $E$ is number of events in range.
- Space complexity: $O(E)$ memory buffer.

6. **Proof Plan**:
- `test_ics_export_valid_rfc5545`: Validates generated ICS payload with `icalendar.Calendar.from_ical()`.
- `test_ics_export_stable_uids`: Verifies subsequent exports produce identical UIDs for occurrences.

## 3. Reminder Scheduling

### 3.1 Fire Time and Lead-Time Computation

1. **Idea**:
Reminders are scheduled relative to the event start timestamp $T$ (or task deadline) using a lead-time offset $L$. A reminder is created if and only if its computed fire time $f$ lies in the future relative to the current wall-clock time and the source event is active (not cancelled).

2. **Formula and Invariants**:
Let $T \in \text{timestamptz}$ be the event start time in canonical UTC.
Let $L \in \mathbb{N}^+$ be the lead-time offset duration in minutes.
Let $t_{\text{now}} \in \text{timestamptz}$ be the current timestamp from the injected `Clock`.

The theoretical fire timestamp $f \in \text{timestamptz}$ is:
$$f = T - L \times 60\text{ seconds}$$

Scheduling Invariant:
A `ScheduledNotification` record is planned and stored if and only if:
$$f > t_{\text{now}} \quad \land \quad E.\text{status} \ne \text{CANCELLED}$$
If $f \le t_{\text{now}}$, the lead-time window has already passed; no historical notification is created.

Default Offset Sets by Event Kind:
- Class event: $L_{\text{CLASS}} = \{15\}$ minutes.
- Meeting event: $L_{\text{MEETING}} = \{1440, 60, 10\}$ minutes (24 hours, 1 hour, 10 minutes).
- Deadline event: $L_{\text{DEADLINE}} = \{2880, 1440, 120\}$ minutes (48 hours, 24 hours, 2 hours).

Faculty can override default offset sets per event kind via personal `ReminderRule` configuration.

3. **Worked Example**:
- Event start: $T = \text{2026-10-28 10:00:00 UTC}$.
- Current time: $t_{\text{now}} = \text{2026-10-27 19:30:00 UTC}$.
- Meeting lead times: $L_1 = 1440\text{ min}$, $L_2 = 60\text{ min}$, $L_3 = 10\text{ min}$.
  - $f_1 = T - 1440\text{m} = \text{2026-10-27 10:00:00 UTC}$. Here $f_1 \le t_{\text{now}}$ (past) $\implies$ discarded.
  - $f_2 = T - 60\text{m} = \text{2026-10-28 09:00:00 UTC} > t_{\text{now}} \implies$ scheduled.
  - $f_3 = T - 10\text{m} = \text{2026-10-28 09:50:00 UTC} > t_{\text{now}} \implies$ scheduled.

4. **Edge Cases**:
- Event rescheduled: Existing `PENDING` notifications for the event are marked `CANCELLED`, and new notifications are planned with the updated start time $T'$.
- Event cancelled: All associated `PENDING` notifications transition immediately to `CANCELLED`.
- Event start moved into the past: All future planned reminders are pruned or cancelled.

5. **Complexity**:
- Time complexity: $O(|L|)$ date arithmetic calculations per attendee, where $|L| \le 5$.
- Space complexity: $O(|L| \cdot |\text{attendees}| \cdot |\text{channels}|)$.

### 3.2 Quiet Hours Shift with Midnight-Crossing Window

1. **Idea**:
Faculty define personal quiet hours (e.g., 22:00 to 07:00 IST) during which audible alerts must not disturb them. When a computed fire time $f$ falls within this quiet window, it is postponed to the end of the window. However, to guarantee that faculty never miss a class or urgent morning commitment, an exception applies: if the event itself starts before or at the quiet window end, shifting the reminder would place it after the event has already started; in this case, the reminder must fire at $f$ without postponement.

2. **Formula and Invariants**:
Let the quiet hours interval be defined by local wall-clock times $q_s, q_e \in [00:00, 24:00)$ in timezone $Z = \text{Asia/Kolkata}$.
Let $f_{\text{local}} = \operatorname{astimezone}(f, Z).\operatorname{time}()$.
Let $T_{\text{local}} = \operatorname{astimezone}(T, Z)$.

Membership predicate $\operatorname{in\_quiet}(t, q_s, q_e)$:
$$\operatorname{in\_quiet}(t, q_s, q_e) = \begin{cases}
q_s \le t < q_e & \text{if } q_s < q_e \quad (\text{same-day window, e.g. 13:00 to 14:00}) \\
t \ge q_s \lor t < q_e & \text{if } q_s > q_e \quad (\text{overnight window, e.g. 22:00 to 07:00}) \\
\text{False} & \text{if } q_s = q_e \quad (\text{quiet hours disabled})
\end{cases}$$

Shift Rule $\operatorname{AdjustQuiet}(f, T, q_s, q_e, Z)$:
If $\operatorname{in\_quiet}(f_{\text{local}}, q_s, q_e)$ is True:
1. Determine the window end datetime $W_{\text{end}}$ corresponding to the specific occurrence of $f$:
   - If $q_s < q_e$: $W_{\text{end}} = \operatorname{datetime}(f_{\text{local}}.\text{date}(), q_e, Z)$.
   - If $q_s > q_e$:
     - If $f_{\text{local}}.\operatorname{time}() \ge q_s$: $W_{\text{end}} = \operatorname{datetime}(f_{\text{local}}.\text{date}() + 1\text{ day}, q_e, Z)$.
     - If $f_{\text{local}}.\operatorname{time}() < q_e$: $W_{\text{end}} = \operatorname{datetime}(f_{\text{local}}.\text{date}(), q_e, Z)$.
2. Evaluate Event Start Constraint:
   If $T \le \operatorname{astimezone}(W_{\text{end}}, \text{UTC})$:
   $$\operatorname{AdjustQuiet} = f \quad (\text{Urgent: class/event starts before quiet window ends})$$
   Else:
   $$\operatorname{AdjustQuiet} = \operatorname{astimezone}(W_{\text{end}}, \text{UTC})$$
Else:
$$\operatorname{AdjustQuiet} = f$$

3. **Worked Example**:
- Quiet window: $q_s = \text{22:00}$, $q_e = \text{07:00}$ IST (crosses midnight).
- Case A (Normal shift):
  - Meeting start: $T = \text{2026-10-28 10:00 IST}$ ($T_{\text{UTC}} = \text{04:30Z}$).
  - Lead time: $L = 480\text{ min}$ (8 hours).
  - Unadjusted fire time: $f = \text{2026-10-28 02:00 IST}$.
  - $f_{\text{local}} = 02:00 < 07:00 \implies \operatorname{in\_quiet} = \text{True}$.
  - Window end: $W_{\text{end}} = \text{2026-10-28 07:00 IST}$.
  - $T = \text{10:00 IST} > W_{\text{end}} = \text{07:00 IST} \implies f' = \text{2026-10-28 07:00 IST}$ ($01:30\text{ UTC}$).
- Case B (Urgent morning class exception):
  - Class start: $T = \text{2026-10-28 06:45 IST}$.
  - Lead time: $L = 15\text{ min}$.
  - Unadjusted fire time: $f = \text{2026-10-28 06:30 IST}$.
  - $f_{\text{local}} = 06:30 < 07:00 \implies \operatorname{in\_quiet} = \text{True}$.
  - Window end: $W_{\text{end}} = \text{2026-10-28 07:00 IST}$.
  - $T = \text{06:45 IST} \le W_{\text{end}} = \text{07:00 IST} \implies$ Shifting to 07:00 would miss the class!
  - Rule fires: $f' = f = \text{2026-10-28 06:30 IST}$ ($01:00\text{ UTC}$). The notification is preserved.

4. **Edge Cases**:
- $q_s = q_e$: Predicate evaluates to False; no shift occurs.
- $f$ exactly at $q_s$: Half-open $[q_s, q_e)$ includes $q_s$, shifted to $q_e$.
- $f$ exactly at $q_e$: Half-open excludes $q_e$, fires immediately at $f$.

5. **Complexity**:
- Time complexity: $O(1)$.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_quiet_hours_table`: Tests normal shift, outside window, crossing midnight, exact boundaries, and the emergency class start exception.

## 4. Exactly-Once Delivery

### 4.1 Deterministic Idempotency Key Derivation

1. **Idea**:
To prevent duplicate notification rows across recurring timetable materialisation jobs, concurrent event rescheduling, or retried requests, every scheduled notification carries a cryptographically deterministic natural idempotency key backed by a PostgreSQL unique index.

2. **Formula and Invariants**:
Let $T_{\text{id}} \in \text{UUID}$ be the target ID (Event ID or Task ID).
Let $u_{\text{id}} \in \text{UUID}$ be the recipient User ID.
Let $L \in \mathbb{N}^+$ be the lead-time offset in minutes.
Let $c \in \{\text{EMAIL}, \text{PUSH}\}$ be the delivery channel.

The idempotency key string $k$ is derived via canonical SHA-256:
$$k = \operatorname{SHA-256}\left(\operatorname{str}(T_{\text{id}}) \mathbin{\Vert} \text{":"} \mathbin{\Vert} \operatorname{str}(u_{\text{id}}) \mathbin{\Vert} \text{":"} \mathbin{\Vert} \operatorname{str}(L) \mathbin{\Vert} \text{":"} \mathbin{\Vert} c.\text{value}\right)$$

Database Invariant:
$$\text{CREATE UNIQUE INDEX uq\_notifications\_idempotency\_key ON scheduled\_notifications (idempotency\_key);}$$
Any planning re-execution for the same tuple $(T_{\text{id}}, u_{\text{id}}, L, c)$ executes an idempotent upsert (`ON CONFLICT (idempotency_key) DO UPDATE SET fire_at_utc = EXCLUDED.fire_at_utc WHERE status = 'PENDING'`), guaranteeing at-most-once row creation.

3. **Worked Example**:
- Event ID: `18bd2535-a9db-426c-8daa-a3ab363a2855`
- User ID: `b9b979b8-a05c-4125-83d9-34d25c517867`
- Offset: `15`
- Channel: `EMAIL`
- Input string: `18bd2535-a9db-426c-8daa-a3ab363a2855:b9b979b8-a05c-4125-83d9-34d25c517867:15:EMAIL`
- Key $k = \operatorname{SHA-256}(\dots) = \text{64-character lowercase hexadecimal hash}$.

### 4.2 Distributed Dispatch via Skip-Locked Batch Claiming

1. **Idea**:
When multiple Celery worker processes execute the periodic dispatcher concurrently, they must not claim or deliver the same notifications. We use PostgreSQL row-level locking with `FOR UPDATE SKIP LOCKED`.

2. **Dispatch Algorithm**:
```sql
SELECT id FROM scheduled_notifications
WHERE status = 'PENDING'
  AND fire_at_utc <= :now_utc
ORDER BY fire_at_utc ASC
LIMIT :batch_size
FOR UPDATE SKIP LOCKED;
```
Within the same database transaction:
```sql
UPDATE scheduled_notifications
SET status = 'SENDING', updated_at_utc = :now_utc
WHERE id = ANY(:claimed_ids);
```
Transaction commits immediately. The lock is released, and claimed rows transition to `SENDING`.

Delivery Execution (Outside Database Transaction):
For each claimed notification:
1. Lookup channel notifier: `notifier = factory.get_notifier(notification.channel)`.
2. Execute transmission: `await notifier.send(notification)`.
3. If transmission succeeds:
   Update database: `status = 'SENT', delivered_at_utc = now_utc`.
4. If transmission fails:
   Update database: `attempts += 1, error_message = err`.
   If `attempts < max_attempts` (5):
     `status = 'PENDING', fire_at_utc = now_utc + backoff(attempts)`.
   Else:
     `status = 'FAILED'`.

### 4.3 Stale SENDING Recovery and Failure Window Bound

1. **Analysis of Exactly-Once vs At-Least-Once Boundary**:
External email (SMTP) and web push (VAPID HTTP) protocols do not support distributed two-phase commit transactions. Therefore:
- The system achieves **strict exactly-once scheduling and storage** ($UNIQUE(\text{idempotency\_key})$).
- The system achieves **strict disjoint dispatch** (`FOR UPDATE SKIP LOCKED`).
- In normal operation (healthy worker and reachable providers), each notification is transmitted **exactly once**.
- **Failure Window Analysis**:
  A duplicate transmission can only occur if a worker experiences a hard crash (e.g. process SIGKILL, host kernel panic, OOM killer) in the narrow temporal interval $\Delta t_{\text{vuln}}$:
  $$\Delta t_{\text{vuln}} = [t_{\text{external\_provider\_ack}}, t_{\text{db\_sent\_commit}}]$$
  where $\Delta t_{\text{vuln}}$ is bounded by the local network database roundtrip:
  $$\mathbb{E}[\Delta t_{\text{vuln}}] \approx 2\text{ to } 8\text{ ms}$$
  If the worker crashes during $\Delta t_{\text{vuln}}$, the stale recovery worker (running every 5 minutes) detects rows stuck in `SENDING` for $t > 5\text{ minutes}$ and transitions them back to `PENDING`, causing a single re-delivery. Under all non-fatal network exceptions and API errors, zero duplicates occur.

### 4.4 Maximum Lateness Bound

1. **Formula**:
Let $I_{\text{poll}} = 30\text{ seconds}$ be the Celery Beat dispatch trigger period.
Let $N_{\text{batch}} = 100$ be the maximum batch claim size.
Let $T_{\text{dispatch}}$ be the batch delivery duration across asynchronous workers ($T_{\text{dispatch}} \le 3.0\text{ s}$).

The upper bound on notification delivery lateness $L_{\text{max}}$ for any due notification is:
$$L_{\text{max}} \le I_{\text{poll}} + T_{\text{dispatch}} = 30.0\text{ s} + 3.0\text{ s} = 33.0\text{ seconds}$$
Under normal load, the expected lateness is:
$$\mathbb{E}[\text{lateness}] = \frac{I_{\text{poll}}}{2} + \mathbb{E}[T_{\text{dispatch}}] \approx 15\text{ s} + 0.5\text{ s} = 15.5\text{ seconds}$$


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

### 5.2 Timetable Cell Tokenization Grammar

1. **Idea**:
Timetable cells in collegiate schedules encode course codes, sections, rooms, and faculty initials within compact, varied textual patterns. The tokenization engine extracts discrete components while handling co-teaching delimiters.

2. **Formula and Grammar Rules**:
Let cell text $C$ be a non-empty string.
Co-teacher delimiter set: $\Delta_{\text{co}} = \{'/', ',', '\&'\}$.
Standard cell topologies:
- Pattern 1 (Parenthesized Initials):
  $$\mathcal{P}_1 = \verb!^(?P<course>[A-Za-z0-9\s\-]+?)\s*\((?P<initials>[A-Za-z0-9\s/,&]+)\)(?:\s+(?P<room>[A-Za-z0-9\-]+))?$!$$
- Pattern 2 (Course, Section, and Initials):
  $$\mathcal{P}_2 = \verb!^(?P<course>[A-Za-z0-9\s]+?)\s*-\s*(?P<section>[A-Za-z0-9]+)\s*\((?P<initials>[A-Za-z0-9\s/,&]+)\)(?:\s+(?P<room>[A-Za-z0-9\-]+))?$!$$
- Pattern 3 (Space-Delimited Course, Initials, Room):
  $$\mathcal{P}_3 = \verb!^(?P<course>[A-Z]{2,6}[0-9]{0,4})\s+(?P<initials>[A-Z]{2,5})(?:\s+(?P<room>[A-Za-z0-9\-]+))?$!$$

Co-teacher splitting rule:
Given raw initials string $S$, token set $T$ is obtained by:
$$T = \{t.\operatorname{strip}() \mid t \in \operatorname{split}(S, \Delta_{\text{co}}) \land t.\operatorname{strip}() \ne \emptyset\}$$

3. **Worked Examples**:
- `CN (KKS)`: Course = `"CN"`, Initials = `["KKS"]`, Room = `None`.
- `DBMS Lab - A1 (RS/PN)`: Course = `"DBMS Lab"`, Section = `"A1"`, Initials = `["RS", "PN"]`.
- `OOAD KKS 301`: Course = `"OOAD"`, Initials = `["KKS"]`, Room = `"301"`.
- `SE - B2 (AP & MKS) 204`: Course = `"SE"`, Section = `"B2"`, Initials = `["AP", "MKS"]`, Room = `"204"`.

4. **Edge Cases**:
- Extra whitespace within parentheses: e.g. `( KKS / PN )` normalized cleanly to `["KKS", "PN"]`.
- Trailing notes: non-matching cells are captured as unparsed raw text and flagged for review rather than dropped.

5. **Complexity**:
- Time complexity: $O(|C|)$ linear regex matching.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_cell_tokenization_patterns`: Unit test verifying extraction across all 4 sample topologies.

### 5.3 Initials Resolution via Normalized Levenshtein Distance

1. **Idea**:
Given an extracted initials token $t$, the system resolves it to a unique `FacultyProfile` in the department. To handle minor OCR errors or typographical slips without false positives, resolution proceeds in three strictly prioritized tiers: exact initials match, exact alias match, and bounded fuzzy matching.

2. **Formula and Invariants**:
Let $t$ be the query token and $F = \{p_1, p_2, \dots, p_N\}$ be the department faculty profiles.
The Levenshtein distance $\operatorname{lev}(a, b)$ is the minimum number of single-character edits (insertions, deletions, substitutions) required to transform $a$ into $b$.
The Normalized Levenshtein Similarity is defined as:
$$\operatorname{sim}(a, b) = 1 - \frac{\operatorname{lev}(a, b)}{\max(|a|, |b|)}$$

Resolution Tiers:
- **Tier 1 (Exact Initials)**:
  $$\exists p \in F \text{ s.t. } p.\text{initials}.value = t \implies \text{Resolved}(p)$$
- **Tier 2 (Exact Alias)**:
  $$\exists p \in F \text{ s.t. } t \in p.\text{aliases} \implies \text{Resolved}(p)$$
- **Tier 3 (Fuzzy Matching)**:
  Compute similarities $s_i = \operatorname{sim}(t, p_i.\text{initials}.value)$ for all $p_i \in F$.
  Let $s_{(1)} \ge s_{(2)} \ge \dots \ge s_{(N)}$ be the ordered similarities.
  Resolution condition:
  $$\operatorname{Result}(t) = \begin{cases}
  \text{Resolved}(p_{(1)}) & \text{if } s_{(1)} \ge \theta_{\text{sim}} \land (s_{(1)} - s_{(2)}) \ge \theta_{\text{margin}} \\
  \text{Ambiguous} & \text{otherwise}
  \end{cases}$$
  where:
  $$\theta_{\text{sim}} = 0.85, \quad \theta_{\text{margin}} = 0.10$$

**Threshold Justification**:
- $\theta_{\text{sim}} = 0.85$: Initials are short strings ($2 \le |I| \le 5$). For $|I| = 2$, a 1-character difference yields $\operatorname{sim} = 1 - 1/2 = 0.50 < 0.85$ (preventing dangerous cross-matches like `CN` $\leftrightarrow$ `PN`). For $|I| = 3$, 1 difference yields $1 - 1/3 = 0.67 < 0.85$. Only for $|I| \ge 4$ does 1 single typo achieve $\operatorname{sim} \ge 0.75$, and for $|I| \ge 7$ (such as full surnames or long aliases) does $\operatorname{sim} \ge 0.85$.
- $\theta_{\text{margin}} = 0.10$: Precludes guessing when two faculty have closely related initials (e.g. `KS` vs `KSS`).

3. **Worked Examples**:
- Token `KKS` with profile initials `KKS`: Tier 1 exact match $\implies \operatorname{sim} = 1.0 \implies \text{Resolved}$.
- OCR noise `KS5` with faculty `KS` ($|I|=2$) and `KSS` ($|I|=3$):
  $$\operatorname{sim}(\text{KS5}, \text{KS}) = 1 - 1/3 = 0.67 < 0.85$$
  $$\operatorname{sim}(\text{KS5}, \text{KSS}) = 1 - 1/3 = 0.67 < 0.85$$
  Neither meets $\theta_{\text{sim}} = 0.85$, and margin is $0.00 < 0.10 \implies \text{Ambiguous}$ (safely flagged for human review).

4. **Edge Cases**:
- Empty token: Rejected immediately.
- Multiple exact alias matches: Flagged as ambiguous.
- Tie in top score: $s_{(1)} = s_{(2)} \implies s_{(1)} - s_{(2)} = 0 < 0.10 \implies$ Ambiguous.

5. **Complexity**:
- Time complexity: $O(N \cdot |t| \cdot \bar{L})$ where $N \le 100$ and $|t|, \bar{L} \le 5 \implies < 100\,\mu\text{s}$.
- Space complexity: $O(N)$ for similarity ranking.

6. **Proof Plan**:
- `test_normalized_similarity_properties`: Property tests verifying $\operatorname{sim}(a, b) \in [0, 1]$, symmetry $\operatorname{sim}(a, b) = \operatorname{sim}(b, a)$, and identity $\operatorname{sim}(a, a) = 1$.
- `test_ambiguity_threshold_rejection`: Proving `KS5` against `KS` and `KSS` yields Ambiguous.

### 5.4 Merged-Cell Period Expansion

1. **Idea**:
In collegiate timetables, laboratory practicals, seminars, and project blocks frequently span multiple consecutive periods (e.g., Periods 2 and 3). A spreadsheet merged cell spans columns $k$ through $m$ ($k \le m$). The expansion maps this into a single continuous `TimetableSlot`.

2. **Formula and Invariants**:
Let periods be indexed $1, 2, \dots, P$.
Each period $i$ has start wall-clock time $s(i)$ and end wall-clock time $e(i)$.
Contiguity condition:
$$\forall i \in [k, m-1], \quad s(i) < e(i) \le s(i+1) < e(i+1)$$
The expanded slot interval is:
$$\operatorname{Slot}(k, m) = [s(k), e(m))$$
Duration:
$$\Delta_{\text{duration}} = e(m) - s(k)$$

3. **Worked Example**:
- Period 2: `10:00 - 10:55` ($s(2) = 10:00, e(2) = 10:55$).
- Period 3: `11:00 - 11:55` ($s(3) = 11:00, e(3) = 11:55$).
- Merged Lab spans columns 2 to 3:
  $$\operatorname{Slot} = [10:00, 11:55), \quad \Delta = 1\text{h } 55\text{m}$$

4. **Edge Cases**:
- Single period cell ($k = m$): $\operatorname{Slot}(k, k) = [s(k), e(k))$.
- Missing intermediate period: Validated to ensure $e(m) > s(k)$.

5. **Complexity**:
- Time complexity: $O(1)$.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_merged_cell_period_expansion`: Integration test proving merged columns 2–3 produce slot from start of 2 to end of 3.

### 5.5 Header Day and Time Normalization

1. **Idea**:
Timetable files use heterogeneous representations for day names (`Mon`, `Monday`, `MON`) and time intervals (`9:00-9:55`, `9.00 - 9.55`, `09:00 to 09:55`). Canonical normalization maps these into ISO weekday integers ($1 = \text{Monday}, \dots, 6 = \text{Saturday}$) and Python `(time, time)` tuples.

2. **Formula and Grammar**:
Day Normalization Function:
$$\operatorname{norm\_day}(D) = \begin{cases}
1 & \text{if } D \in \{\text{MON}, \text{MONDAY}, \text{M}\} \\
2 & \text{if } D \in \{\text{TUE}, \text{TUES}, \text{TUESDAY}, \text{T}\} \\
3 & \text{if } D \in \{\text{WED}, \text{WEDNESDAY}, \text{W}\} \\
4 & \text{if } D \in \{\text{THU}, \text{THUR}, \text{THURSDAY}, \text{TH}\} \\
5 & \text{if } D \in \{\text{FRI}, \text{FRIDAY}, \text{F}\} \\
6 & \text{if } D \in \{\text{SAT}, \text{SATURDAY}, \text{S}\} \\
\bot & \text{otherwise}
\end{cases}$$

Time Range Grammar:
$$\mathcal{G}_{\text{time}} = \verb!^\s*(\d{1,2})[:.](\d{2})\s*(?:-|to)\s*(\d{1,2})[:.](\d{2})\s*$!$$
Extracted values $(h_1, m_1, h_2, m_2)$ yield:
$$t_{\text{start}} = \operatorname{time}(h_1, m_1), \quad t_{\text{end}} = \operatorname{time}(h_2, m_2)$$
Invariant:
$$t_{\text{start}} < t_{\text{end}}$$

3. **Worked Examples**:
- `"Mon"` $\to 1$, `"WEDNESDAY"` $\to 3$.
- `"9:00-9:55"` $\to (09:00, 09:55)$.
- `"09.00 to 09.55"` $\to (09:00, 09:55)$.

4. **Edge Cases**:
- Sunday: Timetable classes are not scheduled on Sunday; Sunday tokens are rejected.
- PM times without 24-hour offset (e.g. `2:00 - 2:55`): When $h_1 < 8$, add 12 to convert to 24-hour system (`14:00 - 14:55`).

5. **Complexity**:
- Time complexity: $O(1)$.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_header_normalization`: Unit test asserting parsing across varied day and time string formats.

## 6. OCR Confidence

## 7. Date and Time Extraction

## 8. Task Priority and Alerts

## 9. Retry Backoff

### 9.1 Exponential Backoff with Full Jitter

1. **Idea**:
When external notification delivery (SMTP or WebPush) encounters transient network timeouts, rate limits, or connection resets, retries must not execute immediately or in lockstep across worker processes. We implement **Full Jitter Exponential Backoff** (Decorrelated Jitter principle). Full Jitter distributes retry attempts uniformly across the exponential interval $[0, \min(C, B \cdot 2^n)]$, which mathematically minimizes peak server collision and queue congestion compared to fixed or equal jitter backoff.

2. **Formula and Invariants**:
Let $n \in \{0, 1, 2, \dots, n_{\text{max}} - 1\}$ be the zero-indexed retry attempt index.
Let $B = 30.0\text{ seconds}$ be the initial base backoff delay.
Let $C = 1800.0\text{ seconds}$ (30 minutes) be the maximum backoff ceiling cap.
Let $n_{\text{max}} = 5$ be the maximum allowed retry attempts before marking the notification `FAILED`.

The exponential upper bound for attempt $n$ is:
$$\operatorname{ceiling}(n) = \min\left(C, B \cdot 2^n\right)$$

The actual retry delay $\Delta t_{\text{delay}}$ in seconds is sampled uniformly at random:
$$\Delta t_{\text{delay}}(n) \sim \operatorname{Uniform}\left(0, \operatorname{ceiling}(n)\right)$$

Invariants:
$$\forall n \ge 0, \quad 0.0 \le \Delta t_{\text{delay}}(n) \le C$$
$$\mathbb{E}[\Delta t_{\text{delay}}(n)] = \frac{\min(C, B \cdot 2^n)}{2}$$

3. **Worked Example**:
$B = 30\text{s}, C = 1800\text{s}$:
- Attempt 0: $\operatorname{ceiling}(0) = \min(1800, 30 \cdot 1) = 30\text{s} \implies \Delta t \in [0, 30\text{s}], \mathbb{E} = 15\text{s}$.
- Attempt 1: $\operatorname{ceiling}(1) = \min(1800, 30 \cdot 2) = 60\text{s} \implies \Delta t \in [0, 60\text{s}], \mathbb{E} = 30\text{s}$.
- Attempt 2: $\operatorname{ceiling}(2) = \min(1800, 30 \cdot 4) = 120\text{s} \implies \Delta t \in [0, 120\text{s}], \mathbb{E} = 60\text{s}$.
- Attempt 3: $\operatorname{ceiling}(3) = \min(1800, 30 \cdot 8) = 240\text{s} \implies \Delta t \in [0, 240\text{s}], \mathbb{E} = 120\text{s}$.
- Attempt 4: $\operatorname{ceiling}(4) = \min(1800, 30 \cdot 16) = 480\text{s} \implies \Delta t \in [0, 480\text{s}], \mathbb{E} = 240\text{s}$.
- Attempt 5: Exceeds $n_{\text{max}} = 5 \implies$ State transitions to `FAILED`. No further retry scheduled.

4. **Edge Cases**:
- Clock skew during retry: Retry schedule sets $f' = t_{\text{now}} + \Delta t_{\text{delay}}$ in UTC, invariant to timezone transitions.
- $n \to \infty$: Bounded by $C = 1800.0\text{s}$, preventing integer overflow or infinite delays.
- Immediate retry when $n=0$: Full jitter allows delay close to 0s if transient network hiccup resolved immediately, while bounding maximum initial delay at 30s.

5. **Complexity**:
- Time complexity: $O(1)$.
- Space complexity: $O(1)$.

6. **Proof Plan**:
- `test_backoff_bounds`: Property test verifying $\forall n \in [0, 100], \quad 0 \le \operatorname{compute\_backoff}(n) \le 1800.0$.
- `test_backoff_expected_mean`: Hypothesis test proving statistical mean of samples converges to $\frac{\min(C, B \cdot 2^n)}{2}$ within standard deviation confidence bounds.


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
