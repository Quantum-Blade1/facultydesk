# Stage 12: OOAD diagram pack and final audit

Roles: ooad-diagrammer, docs-writer, math-verifier, reviewer, orchestrator.
Graphify: start protocol, then end protocol.
Skills: `ooad-diagrams`.

## Goal

A presentation-ready OOAD pack that matches the real code, and a final audit that the whole product meets its contract.

## Tasks

1. Run the `ooad-diagrams` skill to regenerate all eleven diagrams from the current code and export SVG and PNG to `docs/diagrams/`.
2. In `docs/PROJECT.md`, add an "OOAD summary" section a faculty evaluator can read in ten minutes: actors and use cases, the main classes and why each exists, the design patterns with the exact class that implements each, the state machines, and how the layers enforce separation. Link each diagram.
3. Add a "Requirements traceability" table in PROJECT.md: each original requirement (meeting and class reminders, timetable upload, circular scan, initials detection, faculty calendar, to-do list, documentation work alerts) mapped to use cases, classes, endpoints, screens and the tests that prove it.
4. Math verifier: re-check every MATHS.md section against current code; every proof plan item ticked with a passing test.
5. Reviewer: full-repository slop review, not just the last diff. Fix every blocker and major.
6. Final cold run: `make down`, remove volumes, `make demo`, Playwright suite, full test suite.
7. Final DECISIONS.md entry: what the system does, known limitations, and the next three improvements worth making.

## Acceptance criteria

- Eleven diagrams render and match code (spot-check five class names and all state enums).
- Traceability table has no empty cells.
- Full-repo review has no open blockers or majors.
- Cold demo run succeeds; print the URL and demo logins.
- `progress.json` shows all stages done.
