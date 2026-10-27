---
trigger: always_on
description: Mandatory Graphify protocol for understanding the codebase in every stage
---

# Graphify Protocol

Graphify turns this repository into a knowledge graph in `graphify-out/` (`graph.json`, `graph.html`, `GRAPH_REPORT.md`). Use it instead of blind file searching.

## Install (stage 01 only, verify in every later stage)

- Package name on PyPI is `graphifyy` with a double y. The command it installs is `graphify`.
- Preferred install: `uv tool install graphifyy`. Fallback: `pipx install graphifyy`. Avoid plain `pip install` on macOS because it can land in a different Python than the skill resolves at runtime.
- Register for Antigravity: `graphify antigravity install` (if that subcommand is not recognised by the installed version, run `graphify install --project` and read `graphify --help` for the Antigravity target, then record what worked in `docs/DECISIONS.md`).
- Rebuild on every commit: `graphify hook install`.
- Verify: `graphify --version` prints a version and `graphify-out/GRAPH_REPORT.md` exists after the first build.

## Start of every stage

1. Run `/graphify . --update` (or `graphify update .` from the terminal if the slash form is unavailable).
2. Read `graphify-out/GRAPH_REPORT.md` fully.
3. For each module you expect to touch, query its neighbours and dependents to learn the blast radius before you open any file.
4. Write a three-line summary in the stage report: modules touched, dependents affected, communities involved.

## During the stage

- Before creating a new helper, query the graph for an existing one with a similar name or role.
- Before renaming or moving a symbol, query every path that reaches it.
- Read raw files only when you are about to edit them or the graph lacks the detail.

## End of every stage

1. Run `/graphify . --update` again.
2. Confirm in `GRAPH_REPORT.md` that no new orphan nodes and no duplicate concept nodes were introduced by this stage.
3. Confirm the domain community has no edges into infrastructure or api modules. If it does, the architecture law was broken; fix it before finishing.

## Version control

Commit `graphify-out/GRAPH_REPORT.md`. Ignore the rest of `graphify-out/` in `.gitignore`.
