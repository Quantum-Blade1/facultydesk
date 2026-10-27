# Stage 11: Production deployment, CI and end-to-end smoke test

Roles: devops-engineer, frontend-engineer, reviewer.
Graphify: start protocol, then end protocol.
Skills: anthropics `webapp-testing`.

## Goal

One command deploys the whole system with HTTPS, CI guards every push, and an automated end-to-end test proves the main journeys work.

## Tasks

1. `docker-compose.prod.yml`: production images (multi-stage, non-root, no source mounts), Caddy with automatic HTTPS for a domain from `.env`, restart policies, resource limits, healthchecks.
2. A college-LAN mode documented for running on a single department server without a public domain (Caddy internal TLS).
3. GitHub Actions: backend lint, typecheck, tests with Postgres and Redis services; frontend lint, typecheck, build; mermaid render check for docs.
4. Playwright smoke suite (one file per journey, not dozens of tests):
   - HOD logs in, uploads sample timetable, confirms; faculty calendar shows classes.
   - Faculty uploads a circular sample, HOD reviews and confirms; attendees see the meeting.
   - A meeting 2 minutes ahead with a 1-minute reminder produces a notification record marked SENT.
   - HOD assigns a template task; faculty completes it; alerts are cancelled.
5. `make demo`: fresh database, seed, sample uploads processed, so the app is ready for a live demonstration.

## Acceptance criteria

- `docker compose -f docker-compose.prod.yml up -d` on a clean machine reaches healthy and serves HTTPS.
- CI workflow file validated and passing locally with `act` or by push.
- Playwright suite passes; paste the report summary.
