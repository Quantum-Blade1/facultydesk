# Stage 01: Foundation, environment, Graphify, trusted skills

Roles: devops-engineer, backend-engineer, frontend-engineer, docs-writer.
Graphify: this stage installs it; run the start protocol once the repo has files, and the end protocol before commit.

## Goal

A clean monorepo that boots every service healthy with one command, has Graphify and the trusted skills installed, and has the three docs started.

## Tasks

1. `git init` if needed. Add `.gitignore` covering Python, Node, `.env`, `graphify-out/*` except `graphify-out/GRAPH_REPORT.md`, `docs/diagrams/*.mmd`.
2. Install Graphify per `.agents/rules/02-graphify.md`, register it for Antigravity, install the post-commit hook. Record the exact commands that worked in DECISIONS.md.
3. Install trusted skills per `.agents/rules/05-trusted-skills.md` (superpowers subset, anthropics `frontend-design` and `webapp-testing`). Read each SKILL.md before keeping it. List what was installed and from which commit in DECISIONS.md.
4. Create the structure:

```
backend/
  pyproject.toml  alembic.ini  alembic/
  app/
    main.py
    core/            config.py logging.py clock.py db.py security.py errors.py
    domain/
    application/
    infrastructure/
    api/
    workers/
  tests/unit/  tests/integration/
frontend/
docs/  PROJECT.md  MATHS.md  DECISIONS.md  diagrams/
samples/timetables/  samples/circulars/
docker-compose.yml  docker-compose.prod.yml  Makefile  .env.example
```

5. Backend: uv project on Python 3.12, all stack dependencies pinned. `pydantic-settings` config, structlog JSON logging with a request ID middleware, async engine and session factory, Alembic wired to the async engine, `Clock` protocol with `SystemClock` and `FrozenClock`, `/healthz` (process alive) and `/readyz` (Postgres `SELECT 1`, Redis `PING`, MinIO bucket exists).
6. Celery app with Redis broker, a beat schedule file, and a worker that starts healthy.
7. Frontend: Next.js latest stable with App Router, TypeScript strict plus `noUncheckedIndexedAccess`, Tailwind, shadcn/ui initialised, ESLint and Prettier, a home page that shows backend readiness through a typed fetch.
8. docker-compose.yml: postgres 16, redis 7, minio (with bucket creation init container), backend (uvicorn with reload), worker, beat, frontend. Healthchecks on all. Tesseract with English data installed in the backend image.
9. Makefile targets: `up down logs migrate seed lint typecheck test fmt graph diagrams`.
10. Ruff and mypy strict configs in `pyproject.toml`. Pytest with asyncio mode auto and hypothesis installed.
11. Fill the docs skeletons that already exist in `docs/` (keep their headings): PROJECT.md vision, actors and a component diagram of the services; DECISIONS.md stage 01 entry.
12. Build the first graph with `/graphify .`.

## Acceptance criteria

- `make up` from cold: all services healthy in `docker compose ps`.
- `curl -fsS localhost:8000/healthz` and `/readyz` return 200; stopping Redis makes `/readyz` return 503 with the failing dependency named.
- Frontend at `localhost:3000` shows "ready".
- `make lint typecheck test` pass (test suite contains only a Clock property test at this point).
- `graphify --version` works; `graphify-out/GRAPH_REPORT.md` exists.
- `docs/` contains exactly the three Markdown files.
