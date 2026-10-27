# Stage 08: Documentation tasks, priority scoring and alerts

Roles: math-verifier, backend-engineer, architect.
Graphify: start protocol, then end protocol.

## Goal

Faculty never miss documentation work. Tasks are ranked by a transparent priority score and alerts escalate as deadlines approach.

## Tasks

1. Task use cases: create own task; HOD assigns to one faculty, many faculty, or the whole department (creates one task per assignee linked to a parent assignment); update; complete; reopen; delete own unassigned task.
2. Fields: title, description, deadline (local date and time input, stored UTC), importance 1..5, category (Academic documentation, Exam work, Accreditation, Administrative, Personal), optional recurrence (weekly or monthly) for recurring paperwork.
3. Templates for common documentation work the HOD can assign quickly: CO-PO mapping, IA marks upload, attendance shortage report, lab manual update, course file submission. Templates are data seeded by `make seed`, not hard-coded.
4. Alerts: deadline reminders at 72 h, 24 h and 2 h before; then an overdue alert every day at 09:00 local until completed. All through the stage 06 engine with idempotency keys.
5. Escalation: when an assigned task becomes overdue by 24 h, the assigner (HOD) gets one summary alert per day listing overdue assignees.
6. HOD dashboard data: completion rate per assignment, overdue count per faculty.
7. A `DEADLINE` event appears on the calendar for each task deadline.

## Maths to specify first

- Priority score `P = w_I * (I - 1)/4 + w_U * exp(-h / tau)` where `I` is importance, `h` hours remaining (clamped at 0), `tau = 48`, `w_I = 0.4`, `w_U = 0.6`; overdue tasks get `P = 1 + min(days_overdue, 7) / 7` so they always rank first. Show a worked table of five tasks and their order. Justify each constant.
- Alert schedule set `A = { D - 72h, D - 24h, D - 2h } intersected with (now, D)` plus daily overdue times.
- Completion rate formula for the dashboard.

## Tests

- Property: `P` is within `[0, 1]` for non-overdue tasks, strictly greater than 1 for overdue ones, monotonically non-increasing in `h`, non-decreasing in `I`.
- Worked table reproduced exactly.
- Completing a task cancels all its pending alerts (integration).

## Acceptance criteria

- HOD assigns a template task to three faculty; each receives it and its alerts are planned.
- The task list API returns tasks sorted by `P`, with the score exposed.
- Marking complete stops further alerts.
