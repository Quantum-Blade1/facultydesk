---
trigger: always_on
description: Senior-level code quality bar that every line of code must meet
---

# Code Quality Bar

## Python

- `mypy --strict` and `ruff check` with the project config pass with zero ignores added by you.
- Full type hints. `Any` is allowed only at an I/O boundary and must be validated into a typed model on the next line.
- Functions do one thing. If a function needs a comment to explain a block, extract that block into a well-named function instead.
- Prefer frozen dataclasses or Pydantic models for value objects. Enforce invariants in constructors and raise domain exceptions, never return sentinel values.
- Errors: domain raises typed exceptions from `domain/errors.py`. The API layer maps them to HTTP status codes in one exception handler. No bare `except`, no swallowed exceptions.
- Async all the way through I/O paths. No blocking calls (OCR, image work) on the event loop; those run in Celery workers.
- Database: no N+1 queries. Use `selectinload` or explicit joins. Every query that runs on a hot path has a supporting index declared in the migration.
- Migrations are reversible. `alembic downgrade -1` must work for every revision.

## TypeScript

- `strict: true`, `noUncheckedIndexedAccess: true`. No `any`, no `as unknown as`, no `@ts-ignore`, no non-null assertions on data from the network.
- API types come only from `openapi-typescript` generation. Never hand-write a response type.
- Server state through TanStack Query only. Forms through react-hook-form with zod schemas.
- Components are small and named for what they show. No god components over about 150 lines.
- Accessibility: every interactive element is keyboard reachable and labelled. Colour is never the only signal.

## Forbidden patterns (slop detector)

Reject your own change if it contains any of these:

- `TODO`, `FIXME`, `XXX`, `pass` as a body, `...` as a body, `NotImplementedError` in shipped paths.
- Hard-coded demo data in application code (seed data belongs only in `backend/app/infrastructure/seed/` and runs only via `make seed`).
- Functions that return a constant pretending to be a computed result.
- Catch-all `except Exception` that logs and continues without a reason tied to a documented failure mode.
- Duplicate logic that already exists elsewhere in the graph. Query Graphify before writing a helper.
- Unused imports, variables, parameters, files or dependencies.
- Comments of any kind in code, including section banners.
- Over-engineering: interfaces with a single implementation that is not a documented Strategy or Repository seam.

## Review before you finish

Before marking any task complete, re-read the diff as a hostile reviewer would. Ask: does every branch have a reason, does every input get validated, is every time value timezone-aware, would this survive a retry, would a new teammate understand it without comments. Fix what fails.
