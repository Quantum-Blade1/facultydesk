# FacultyDesk Decisions

One entry per stage: what we built, why, what we rejected, risks, and a small diagram. Newest at the bottom.

## Stage 00: Agent setup

- What we set up: rules in `AGENTS.md` and `.agents/rules/`, role files in `.agents/agents/`, local skills in `.agents/skills/`, twelve ordered stage prompts in `prompts/`, and loop state in `.agents/state/progress.json`.
- Why: one agent working through fixed stages with written rules produces consistent code. The loop state lets the build resume in a new conversation without losing track.
- Rejected: legacy Antigravity workflows in `.agents/workflows/`, because they stopped working on 19 October 2026; the loop is a skill instead.
- Risk: an external skill could contain unsafe instructions. Contained by allowing only three named sources and reading each SKILL.md before use.

```mermaid
flowchart LR
    K[Kickoff prompt] --> L[build-loop skill]
    L --> S[Next stage prompt]
    S --> G[Graphify start]
    G --> R[Roles do the tasks]
    R --> V[Review and verify]
    V --> D[Docs and commit]
    D --> P[progress.json]
    P --> L
```

## Stage 01: Foundation, environment, Graphify, trusted skills

- What we built:
  - Git repository initialization and `.gitignore` covering Python, Node, `.env`, and Graphify outputs.
  - Graphify integration: installed `graphifyy` (0.9.93), ran Antigravity registration, and configured Git commit hooks.
  - Trusted skills installed and audited: `obra/superpowers` (commit `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`) and `anthropics/skills` (commit `dbd4588f9e1033efb41dad4bef2f7947c8993d44`).
  - Backend project scaffolded with `uv` on Python 3.12, strict typing, structlog JSON logging with `X-Request-ID`, `Clock` protocol with `SystemClock` and `FrozenClock`, async SQLAlchemy 2 + asyncpg, Alembic, Celery, and `/healthz` & `/readyz` probes.
  - Frontend scaffolded with Next.js 16, TypeScript strict with `noUncheckedIndexedAccess`, Tailwind, shadcn/ui initialised, and typed readiness probe dashboard.
  - Complete Docker Compose development and production architectures with health checks for all services.
- Why this way:
  - Official `minio/minio` Docker Hub community images were deprecated in 2025; `cgr.dev/chainguard/minio` and `cgr.dev/chainguard/minio-client` provide secure, reproducible S3 compatibility.
  - `Clock` abstraction ensures deterministic property testing for all time-based logic.
  - Server-side pre-fetch with client polling on the frontend ensures instant status rendering and reactive live health updates.
- What we rejected:
  - Direct `datetime.now()` calls in business code (violates UTC determinism law).
  - Unpinned dependencies (both `uv.lock` and `pnpm-lock.yaml` are strictly tracked).
  - Legacy workflow files (replaced with clean skill definitions).
- Risks and how they are contained:
  - Host port contention with unrelated local Docker services: host-level collisions documented and isolated; development stack ports mapped cleanly.
  - Network timeouts during service startup: explicit container dependency chains and healthchecks ensure clean startup ordering.

```mermaid
flowchart LR
    Dev["Developer / Make Targets"] --> DC["Docker Compose Stack"]
    DC --> PG["PostgreSQL 16 (Healthy)"]
    DC --> RD["Redis 7 (Healthy)"]
    DC --> MO["MinIO S3 (Healthy)"]
    DC --> BE["FastAPI Backend (Healthy)"]
    DC --> FE["Next.js Frontend (Healthy)"]
    DC --> WK["Celery Worker (Healthy)"]
    DC --> BT["Celery Beat (Healthy)"]
    BE --> Probes["/healthz & /readyz"]
    FE --> BE
```

## Stage 02: Domain model and persistence (OOAD core)

- What we built:
  - Framework-free domain entities and value objects in `backend/app/domain/` with zero I/O imports (`Department`, `User`, `FacultyProfile`, `Initials`, `AcademicTerm`, `Holiday`, `Room`, `Course`, `Section`, `TimetableUpload`, `TimetableSlot`, `Event`, `EventAttendee`, `Circular`, `ScheduledNotification`, `ReminderRule`, `PushSubscription`, `Task`, `AuditLog`).
  - Finite state machine transition tables and algebraic checks for `Circular` and `ScheduledNotification`, enforcing legal paths and raising typed `InvalidTransition` exceptions.
  - Abstract repository interfaces (`DepartmentRepository`, `UserRepository`, etc.) and asynchronous `UnitOfWork` interface.
  - PostgreSQL schema with async SQLAlchemy 2 models, check constraints (`end_utc > start_utc`, `1 <= importance <= 5`), indices, and reversible Alembic migration `8f3198838ebd_initial_schema.py`.
  - SQLAlchemy repository adapters and `SqlAlchemyUnitOfWork`.
  - Property-based tests via Hypothesis for `Initials` ASCII grammar and exhaustive Cartesian state transition matrices.
  - Integration tests verifying aggregate persistence and round-trips against PostgreSQL in Docker.
- Why this way:
  - Clean Architecture layer isolation ensures business rules can be verified purely in memory with zero database or framework overhead.
  - Invariants in entity constructors and value objects guarantee illegal states cannot exist in domain memory.
  - Explicit transition tables prevent invalid status bypasses across background tasks and user flows.
- What we rejected:
  - Framework coupling in `app/domain` (SQLAlchemy declarative models remain strictly in `app/infrastructure/db/models.py`).
  - Loose string representations for `Initials` and `TimeSlot` (encapsulated as immutable, validated value objects).
  - Implicit database rollbacks (managed explicitly via `UnitOfWork` context manager).
- Risks and how they are contained:
  - Lazy loading `MissingGreenlet` errors in async SQLAlchemy: contained by declaring eager `selectinload` options and explicit relation management in repository adapters.
  - Concurrency idempotency collisions: contained via unique `idempotency_key` and composite uniqueness constraints on the database level.

```mermaid
flowchart LR
    subgraph DomainLayer["Domain Layer (Zero I/O Deps)"]
        Entities["Entities & Value Objects"]
        Events["Domain Events"]
        RepoABCs["Repository & UnitOfWork ABCs"]
    end

    subgraph InfraLayer["Infrastructure Layer"]
        RepoImpls["SQLAlchemy Repositories"]
        SQLModels["SQLAlchemy Models"]
        SQLUoW["SqlAlchemyUnitOfWork"]
    end

    subgraph Database["PostgreSQL 16"]
        Tables[("Tables & Check Constraints")]
    end

    RepoImpls -.implements.-> RepoABCs
    SQLUoW -.implements.-> RepoABCs
    RepoImpls --> SQLModels
    SQLModels --> Tables
```


