# Stage 05: Calendar core, recurrence, clash detection, ICS feed

Roles: math-verifier, backend-engineer, architect.
Graphify: start protocol, then end protocol.

## Goal

Each faculty member has a correct personal calendar built from timetable slots, meetings and manual events, with clashes detected and a subscribable ICS feed.

## Tasks

1. Recurrence: for each confirmed TimetableSlot, generate class occurrences for every matching weekday in the term, excluding holidays. Expand in `Asia/Kolkata` wall-clock time with `dateutil.rrule` (`FREQ=WEEKLY`, `BYDAY`, `UNTIL`), then convert each occurrence to UTC.
2. Materialisation: store occurrences in a rolling window (today to today + 21 days) refreshed nightly and whenever slots change, using an idempotent upsert keyed by `(slot_id, local_date)`. Explain in DECISIONS.md why rolling materialisation beats full-term expansion and pure on-the-fly computation for reminders and queries.
3. Manual events: create, update, cancel for own calendar; HOD can create department meetings with attendees.
4. Calendar query: events for a user in a date range, merged across sources, sorted.
5. Clash detection: on create or update, report clashes for each attendee; for HOD-created meetings, return attendees with clashes before saving and require an explicit override flag.
6. Free-slot finder: given attendees, a date range, a duration and working hours, return the earliest common free intervals.
7. ICS feed: per-user secret token URL (rotatable) serving RFC 5545 `VCALENDAR` with `VEVENT`s, `UID` stable per occurrence, `DTSTAMP`, times in UTC. Validate output with the `icalendar` library in tests.
8. Domain events `EventScheduled`, `EventRescheduled`, `EventCancelled` emitted for stage 06.

## Maths to specify first

- Recurrence set definition: `R = { d in [term_start, term_end] : weekday(d) = w } \ H`, each mapped to `[local(d, t_start), local(d, t_end))` then to UTC.
- Overlap predicate on half-open intervals: `overlap(a, b) iff a.start < b.end and b.start < a.end`. Back-to-back classes (`a.end == b.start`) do not clash.
- Sweep algorithm for clash detection: sort by start, keep a min-heap of active end times; O(n log n).
- Free-slot finder: merge busy intervals of all attendees (sort and merge), then take gaps of length at least the requested duration within working hours.

## Tests

- Property: clash sweep result equals brute-force pairwise result on random interval sets.
- Property: every generated occurrence is on weekday w, within term, not a holiday, and its UTC conversion round-trips to the same local wall time.
- Property: free slots never intersect any busy interval and each has length at least the duration.
- Example: a worked example from MATHS.md reproduced exactly.

## Acceptance criteria

- After confirming a sample timetable, a faculty member's calendar API returns the expected classes for the next 3 weeks with holidays skipped.
- Creating a meeting that overlaps a class returns the clash list.
- The ICS URL imports into Google Calendar or Apple Calendar (state which was used and paste the validator output).
