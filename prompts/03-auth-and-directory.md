# Stage 03: Authentication, roles and faculty directory

Roles: architect, backend-engineer, math-verifier, reviewer.
Graphify: start protocol, then end protocol.

## Goal

Secure login with role-based access, and a faculty directory that is the single source of truth for initials.

## Tasks

1. Auth use cases: register by admin invite, login, refresh, logout, change password. Argon2id hashing. Access JWT 15 minutes with `sub`, `role`, `dept`, `exp`, `iat`, `jti`. Refresh token: random 256-bit, stored as SHA-256 hash, rotated on every use, family revocation on reuse. Refresh cookie httpOnly, Secure (configurable for local dev), SameSite=Lax, path `/api/auth`.
2. Authorisation policy object in `application/` that every use case calls: FACULTY acts only on own resources, HOD on own department, ADMIN everywhere. Routers call use cases only.
3. Directory use cases: create, update, deactivate faculty; bulk import faculty from csv or xlsx with columns `full_name, initials, email, aliases` returning a per-row report (created, updated, rejected with reason). Reject duplicate initials within a department.
4. Academic term and holiday management for ADMIN and HOD, including bulk holiday import.
5. Rate limits: login 5 per minute per IP and per account; refresh 30 per minute.
6. AuditLog on every ADMIN or HOD write.
7. Seed command `make seed`: one department, one admin, one HOD, eight faculty with realistic synthetic names and initials, the current term, and a holiday list. Synthetic data only.

## Maths to specify first

- Token lifetimes and the rotation and reuse-detection rule as a small state table.
- Rate limit as a fixed window or sliding window: pick one, give the formula and why.

## Tests

- Reuse of a rotated refresh token revokes the family (integration).
- Policy matrix test: for each role and each resource ownership case, allowed or denied matches a table written in MATHS.md.
- Bulk import report is correct for a file with valid rows, duplicate initials, bad emails and missing fields.

## Acceptance criteria

- Login, refresh, logout demonstrated with curl showing cookies and status codes.
- FACULTY receives 403 on another faculty member's resources; HOD receives 403 outside their department.
- Bulk import of `samples/faculty.csv` (create it) produces the expected report.
