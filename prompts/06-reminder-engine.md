# Stage 06: Reminder engine with exactly-once delivery

Roles: math-verifier, backend-engineer, devops-engineer, reviewer.
Graphify: start protocol, then end protocol.

## Goal

Every faculty member receives each reminder once, on time, on the channels they chose, with quiet hours respected and no duplicates even with retries and multiple workers.

## Design (implement exactly)

1. Planning: on `EventScheduled`, `EventRescheduled`, `EventCancelled`, `TaskCreated`, `TaskDeadlineChanged`, and in the nightly materialisation job, compute the notifications for each attendee and channel and upsert `ScheduledNotification` rows. Reschedule cancels obsolete rows and creates new ones. Cancel moves PENDING rows to CANCELLED.
2. Defaults: CLASS offsets `[15]` minutes; MEETING `[1440, 60, 10]`; DEADLINE handled in stage 08. Users override per event kind.
3. Dispatch: Celery beat runs `dispatch_due` every 30 seconds. It claims a batch with `SELECT ... WHERE status = 'PENDING' AND fire_at_utc <= now() ORDER BY fire_at_utc LIMIT :n FOR UPDATE SKIP LOCKED`, sets them to SENDING in the same transaction, commits, then sends outside the transaction.
4. Send: `Notifier` Strategy with `WebPushNotifier` (pywebpush, VAPID; remove subscriptions that return 404 or 410) and `EmailNotifier` (aiosmtplib, plain text plus simple HTML). In development, email goes to a Mailpit container added to compose.
5. Outcome: success sets SENT. Failure increments attempts, records the error, and sets PENDING with `fire_at_utc = now + backoff(attempt)` until max attempts (5), then FAILED.
6. Stale SENDING recovery: rows stuck in SENDING longer than 5 minutes return to PENDING (a crashed worker must not lose a reminder).
7. Quiet hours: if `f` falls inside the user's quiet window, move it to the window end, unless the event itself starts before that end, in which case send at `f` (a class reminder must never be suppressed by quiet hours).
8. Notification content: title, local start time, venue, and a deep link to the event in the app.
9. Endpoints: manage reminder rules, quiet hours, push subscriptions; list own upcoming notifications.
10. Generate VAPID keys in a make target and document them in `.env.example`.

## Maths to specify first

- Fire time `f = T - L`; create iff `f > now` and the event is not cancelled.
- Idempotency key `k = SHA-256(target_id | user_id | offset_minutes | channel)` with a unique constraint, so re-planning the same event produces no duplicate.
- Exactly-once argument: unique key prevents duplicate rows; SKIP LOCKED prevents two workers claiming one row; the SENDING state plus stale recovery guarantees at-least-once; the push and email providers do not dedupe, so state precisely where duplicates remain possible (a crash after send and before the SENT commit) and how the window is minimised.
- Maximum lateness bound: `lateness <= poll_interval + batch_processing_time`; give the numbers.
- Backoff with full jitter: `delay(n) = uniform(0, min(cap, base * 2^n))`, base 30 s, cap 30 min.
- Quiet-hours shift rule including windows that cross midnight.

## Tests

- Property: re-running planning any number of times yields the same set of rows.
- Concurrency integration test: two dispatchers in parallel over 500 due rows send each exactly once (count calls on a fake notifier).
- Property: backoff delay is within `[0, cap]`.
- Quiet-hours table test covering inside, outside, crossing midnight and event-before-window-end cases.

## Acceptance criteria

- Creating a meeting 12 minutes from now with a 10-minute offset produces a web push in the browser and an email in Mailpit within the lateness bound. Show timestamps.
- Rescheduling the meeting moves the reminder; cancelling it means no reminder arrives.
- Sequence diagram for dispatch in PROJECT.md and rendered.
