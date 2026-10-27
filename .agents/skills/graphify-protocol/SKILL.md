---
name: graphify-protocol
description: Start-of-stage and end-of-stage procedure for using the Graphify knowledge graph to understand and protect the FacultyDesk codebase. Use at the beginning and end of every stage and before touching any module.
---

# Graphify Protocol

## Start of stage

1. Confirm the tool: `graphify --version`. If missing, install with `uv tool install graphifyy` (fallback `pipx install graphifyy`).
2. Update the graph: `/graphify . --update` (terminal fallback: `graphify update .`). On the very first build use `/graphify .`.
3. Read `graphify-out/GRAPH_REPORT.md` end to end.
4. List the modules this stage will touch. For each one, query its neighbours and the shortest paths to the `api` and `domain` communities. Note dependents that could break.
5. Write into the stage report:
   - Modules touched
   - Dependents at risk
   - Communities involved

## Before writing a helper or new class

Query the graph for existing symbols with similar names or roles. Reuse or extend instead of duplicating.

## End of stage

1. `/graphify . --update`.
2. Re-read `GRAPH_REPORT.md` and check:
   - No new orphan nodes from this stage's files.
   - No duplicate concept nodes (two classes modelling the same thing).
   - The domain community has no edges into `infrastructure`, `api` or `workers`.
3. If a check fails, fix the code and repeat.
4. Stage `graphify-out/GRAPH_REPORT.md` in the commit.
