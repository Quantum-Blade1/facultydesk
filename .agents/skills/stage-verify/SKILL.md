---
name: stage-verify
description: Final gate that proves a stage is complete with evidence. Use before marking any stage done.
---

# Stage Verify

A stage passes only if every item below passes with evidence pasted into the report.

1. **Static checks**
   - `make lint` passes.
   - `make typecheck` passes.
2. **Tests**
   - `make test` passes. Report counts and the MATHS.md properties covered.
3. **Cold boot**
   - `make down && make up`; every service reaches healthy. Paste `docker compose ps`.
   - `curl -fsS localhost:8000/readyz` returns 200.
4. **Migrations**
   - `make migrate` applies cleanly. `alembic downgrade -1 && alembic upgrade head` succeeds for this stage's revisions.
5. **Feature exercised end to end**
   - Run every acceptance criterion in the stage prompt against the running stack with real requests or real UI actions. Paste request and response, or describe the UI check with the screen size used.
6. **Docs**
   - `docs/` contains exactly `PROJECT.md`, `MATHS.md`, `DECISIONS.md` (plus `diagrams/`).
   - This stage has a DECISIONS.md entry and every new algorithm has a complete MATHS.md section.
   - Every mermaid block changed this stage renders with mermaid-cli.
7. **Graph**
   - Graphify end checks pass.
8. **Review**
   - Reviewer has no open blockers or majors.

If any item fails, list it, fix it, and run this skill again.
