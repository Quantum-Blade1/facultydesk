---
name: slop-review
description: Mechanical and judgement checks that reject AI-slop code before a stage closes. Use on every stage diff in the reviewer role.
---

# Slop Review

## Mechanical checks (run them, paste results)

```bash
git diff --name-only HEAD | tee /tmp/changed.txt
grep -nE "TODO|FIXME|XXX|NotImplementedError" $(cat /tmp/changed.txt) || true
grep -nE "^\s*#|^\s*//" $(grep -E "\.(py|ts|tsx)$" /tmp/changed.txt) | grep -vE "#!/|# type:|// @ts-expect-error never|eslint-disable never" || true
grep -nE "datetime\.now\(|datetime\.utcnow\(" backend/app || true
grep -nE "except Exception|except:" backend/app || true
grep -nE ":\s*any\b|as any|@ts-ignore" frontend -r --include=*.ts --include=*.tsx || true
cd backend && uv run ruff check . && uv run mypy --strict app && cd ..
cd frontend && pnpm lint && pnpm typecheck && cd ..
```

Any hit from the grep lines is a finding unless it is a docstring on a route handler or a justified boundary.

## Judgement checks

For each changed function ask:

1. Is there a branch with no reason to exist?
2. Is there a return value that is constant but pretends to be computed?
3. Is there logic duplicated elsewhere in the graph?
4. Is there an abstraction with one implementation that is not a documented seam?
5. Is a name vague (`data`, `info`, `handle`, `process`, `manager`, `util`)? Rename to what it is.
6. Does the test assert behaviour from MATHS.md, or does it only assert that code ran?
7. Is any timestamp naive, any retried write non-idempotent, any input unvalidated?

## Output

Findings as `severity | file:line | problem | fix`. Blockers and majors must be fixed before the stage closes.
