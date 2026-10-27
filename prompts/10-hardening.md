# Stage 10: Security, reliability and observability hardening

Roles: reviewer, backend-engineer, devops-engineer, math-verifier.
Graphify: start protocol, then end protocol.

## Goal

The system is safe to put in front of real faculty and recoverable when something breaks.

## Tasks

1. Security review against OWASP ASVS level 1 essentials: auth, session, access control, input validation, file upload, error handling, logging. Record each item as pass or fixed in DECISIONS.md.
2. Upload hardening: byte-level MIME sniffing, size limits, image decompression-bomb guard (pixel count limit), pdf page-count limit, filenames never used as storage keys.
3. Security headers via Caddy and Next.js: CSP, HSTS (prod), X-Content-Type-Options, Referrer-Policy, frame-ancestors none.
4. Dependency audit: `pip-audit` and `pnpm audit`; fix or justify every high or critical finding.
5. Observability: request ID propagated from API into Celery tasks; structured logs for every state transition of Circular and ScheduledNotification; a metrics endpoint with counts of notifications by status, queue depth and dispatch lateness percentiles.
6. Reliability: graceful shutdown for workers, task time limits, dead-letter handling for FAILED notifications visible to ADMIN, idempotent nightly jobs.
7. Backups: nightly `pg_dump` to MinIO with 14-day retention, and `make restore` tested against a fresh database.
8. Performance: seed 120 faculty, 2 terms of timetable, 5,000 tasks; calendar query for one week under 150 ms p95 and dispatch of 1,000 due notifications under 60 s. Add indexes or fix queries as needed and show `EXPLAIN ANALYZE` for the hot queries.

## Maths to specify first

- Lateness percentile computation and the measured numbers against the bound from stage 06.
- Retention arithmetic for backups.

## Acceptance criteria

- Audit reports clean or justified.
- Restore test passes.
- Performance targets met with evidence.
