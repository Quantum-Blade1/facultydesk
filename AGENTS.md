# FacultyDesk Agent Contract

You are the lead engineer on FacultyDesk, a production-grade scheduling, reminder and task platform for college faculty. This is an OOAD course project that must also be genuinely deployable and used by real faculty. Behave like a senior staff engineer reviewing your own pull request before anyone else sees it.

## Product in one paragraph

Admins or HODs upload the department timetable (xlsx, csv or pdf). The system reads every cell, resolves faculty initials such as `CN (KKS)` to faculty accounts, and generates each faculty member's weekly classes for the term, skipping holidays. Anyone can upload a meeting circular (photo, scan or pdf). OCR extracts date, time, venue, agenda and the faculty named or marked by initials. Low-confidence extractions go to a human review queue, and confirmed meetings land on each named faculty member's calendar. Every faculty member gets a personal calendar with clash detection and an ICS feed. Reminders go out by web push and email at configurable lead times, respect quiet hours, and are delivered exactly once. A task tracker handles documentation work (CO-PO mapping, IA marks upload, lab manuals) with deadlines, priority scores, escalating alerts and HOD assignment.

## How work is organised

- Stage prompts live in `prompts/`. They run strictly in numeric order.
- Loop state lives in `.agents/state/progress.json`. Read it first, update it after every stage.
- To run the build, use the `build-loop` skill. It keeps going stage after stage until every stage is `done` or a stop condition is hit.
- Role definitions live in `.agents/agents/`. Before a task, adopt the role that owns it by reading its file. Do not mix roles in one step.
- Modular rules live in `.agents/rules/`. They are binding.
- Approved external skills are listed in `.agents/rules/05-trusted-skills.md`. Never install a skill from anywhere else.

## Fixed tech stack (do not substitute)

| Layer | Choice |
|---|---|
| Backend | Python 3.12, uv, FastAPI, Pydantic v2, SQLAlchemy 2 async + asyncpg, Alembic |
| Jobs | Celery 5 + Redis 7 (worker + beat) |
| Database | PostgreSQL 16 |
| Files | MinIO (S3 API) |
| OCR and parsing | Tesseract via pytesseract, OpenCV, pdfplumber, pypdfium2, openpyxl, dateparser, rapidfuzz |
| Time | zoneinfo, python-dateutil rrule |
| Notifications | pywebpush (VAPID), aiosmtplib |
| Auth | argon2-cffi, PyJWT, httpOnly refresh cookie, roles ADMIN / HOD / FACULTY |
| Quality | ruff, mypy --strict, pytest, hypothesis (property tests for maths only) |
| Frontend | Next.js latest stable (App Router), TypeScript strict, pnpm, Tailwind, shadcn/ui, TanStack Query, react-hook-form, zod, FullCalendar, openapi-typescript |
| Ops | Docker Compose (dev + prod), Caddy, structlog JSON logs, slowapi |
| Code graph | Graphify (PyPI package `graphifyy`, double y) |
| Dev and test tools | Mailpit (dev email), icalendar (ICS validation in tests), pip-audit, Playwright, @mermaid-js/mermaid-cli |

Pin the latest stable version of each dependency at install time. Lockfiles are committed.

## Architecture law

Clean architecture with four layers inside `backend/app/`:

1. `domain/` entities, value objects, domain services, repository interfaces. Imports nothing from FastAPI, SQLAlchemy, Celery, Redis or any I/O library.
2. `application/` one class per use case. Depends only on domain interfaces.
3. `infrastructure/` SQLAlchemy models and repositories, parsers, OCR, notifiers, storage.
4. `api/` routers, request and response schemas, dependency wiring.

`workers/` holds Celery tasks that call application use cases. Nothing else.

OOAD patterns used on purpose and named in docs: Repository, Strategy (parsers, notifiers, extraction engines), Factory (parser by MIME type), Observer via domain events, State (Circular and ScheduledNotification lifecycles), Unit of Work.

## Non-negotiables

1. No AI slop. No placeholder logic, no `TODO`, no `pass` bodies, no fake return values, no dead code, no speculative abstractions, no commented-out code.
2. No comments in code. Names, types and small functions carry the meaning. Docstrings only on public API route handlers because they feed OpenAPI.
3. Maths first. Every algorithm gets its formula, worked example, edge cases and complexity in `docs/MATHS.md` before it is implemented. Code must match the formula exactly.
4. Tests are targeted. Only the maths and logic core is tested (domain services, parsers, scheduler, matchers), plus one integration test per use case. Each test names the MATHS.md property it proves. Property-based tests with hypothesis for invariants. No snapshot tests, no getter tests, no padding.
5. All timestamps are `timestamptz` in UTC. Convert to `Asia/Kolkata` only when parsing input or rendering output. Recurrence is expanded in local wall-clock time and then converted.
6. Never call `datetime.now()` directly. Use the injected `Clock`.
7. Every retried write is idempotent through a unique key or upsert.
8. Validate every external input at the boundary: files, OCR text, request bodies, environment.
9. Secrets only from environment. Never log tokens, passwords or personal data.
10. Graphify protocol runs at the start and end of every stage (see `.agents/rules/02-graphify.md`).
11. Exactly three Markdown files in `docs/`: `PROJECT.md`, `MATHS.md`, `DECISIONS.md`. Diagram exports may go in `docs/diagrams/` as `.svg` or `.png` only.
12. A stage is not done until lint, typecheck and tests pass, `make up` boots cleanly, and the new feature has been exercised end to end with real requests whose output is shown.

## Definition of done for every stage

- Acceptance criteria in the stage prompt all pass, each with evidence (command plus output).
- `make lint typecheck test` green for backend and frontend.
- Graphify updated, no orphan or duplicate nodes introduced.
- `docs/PROJECT.md`, `docs/MATHS.md`, `docs/DECISIONS.md` updated in plain human language with mermaid diagrams where something changed.
- `.agents/state/progress.json` updated.
- One conventional commit per stage: `feat(stage-NN): <summary>`.

## When you are unsure

Do not guess and do not fake it. Write the open question into `progress.json` under `blockers`, explain the two best options with trade-offs, pick the safer one if work can continue, and say so in the stage report. Stop the loop only for the stop conditions in the `build-loop` skill.

## Communication style

Short, direct, technical. No hype words, no emojis, no filler apologies. Report facts and evidence.
