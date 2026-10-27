# Stage 02: Domain model and persistence (OOAD core)

Roles: architect (design first), math-verifier, backend-engineer, ooad-diagrammer, docs-writer.
Graphify: start protocol, then end protocol.
Skills: superpowers `brainstorming` for the design pass, `math-first` for invariants.

## Goal

A complete, framework-free domain layer with enforced invariants, plus the database schema and repositories that persist it.

## Domain (backend/app/domain)

Entities and value objects:

- `Department`, `User` (role ADMIN | HOD | FACULTY), `FacultyProfile` (full_name, initials, aliases, email, phone optional, department).
- `Initials` value object: uppercase letters only, length 2 to 5, unique per department.
- `AcademicTerm` (start_date, end_date, timezone name), `Holiday` (date, label).
- `Room`, `Course` (code, name), `Section`.
- `TimeSlot` value object (weekday, start_time, end_time) with `end_time > start_time`.
- `TimetableUpload` (file key, status, parse report), `TimetableSlot` (TimeSlot, course, section, room, faculty, source cell reference).
- `Event` aggregate root (kind CLASS | MEETING | DEADLINE | CUSTOM, title, start_utc, end_utc, location, source TIMETABLE | CIRCULAR | MANUAL | TASK, source_id) with `EventAttendee` (faculty, response).
- `Circular` aggregate (file key, ocr text, extracted fields, confidence, status) with State pattern: UPLOADED -> PROCESSING -> NEEDS_REVIEW | CONFIRMED; NEEDS_REVIEW -> CONFIRMED | REJECTED; PROCESSING -> FAILED -> PROCESSING (retry).
- `ReminderRule` (user, event kind, offsets in minutes, channels), `QuietHours` (start, end in local time, may cross midnight).
- `ScheduledNotification` with State pattern: PENDING -> SENDING -> SENT | FAILED; FAILED -> PENDING (retry, bounded); PENDING -> CANCELLED. Fields: target (event occurrence or task), user, channel, fire_at_utc, idempotency_key, attempts, last_error.
- `PushSubscription`, `Task` (title, description, deadline_utc, importance 1..5, status, assignee, assigner), `AuditLog`.
- Domain events: `EventScheduled`, `EventRescheduled`, `EventCancelled`, `TaskCreated`, `TaskDeadlineChanged`.
- Repository interfaces as ABCs and a `UnitOfWork` interface.
- `errors.py` with typed domain exceptions including `InvalidTransition` and `InvariantViolation`.

## Maths to specify first (MATHS.md)

- State machine definitions as transition tables, with the rule that any transition not in the table raises.
- Interval invariant `start < end` and the half-open interval convention `[start, end)` used everywhere.

## Persistence

- SQLAlchemy models in `infrastructure/db/models/`, mappers between models and domain objects, repository implementations, SQLAlchemy `UnitOfWork`.
- One Alembic revision. `timestamptz` everywhere. Foreign keys with explicit `ON DELETE`. Indexes: `(status, fire_at_utc)` on notifications, `(faculty_id, start_utc)` on attendees joined to events, unique `(department_id, initials)`, unique `idempotency_key`, `(assignee_id, deadline_utc)` on tasks. Check constraints for `end_utc > start_utc` and importance range.

## Tests

- Property tests: every legal transition succeeds, every illegal one raises (generate all pairs from the enum).
- Invariant tests for Initials, TimeSlot, Event.
- Integration test: round-trip each aggregate through its repository against the real Postgres in compose.

## Diagrams

Class diagram of the domain, state diagrams for Circular and ScheduledNotification, ER diagram. All in PROJECT.md and rendered.

## Acceptance criteria

- Graphify shows no edges from `domain` to any other layer.
- `alembic upgrade head`, `downgrade base`, `upgrade head` all succeed.
- All tests pass; state-machine property test enumerates every enum pair.
