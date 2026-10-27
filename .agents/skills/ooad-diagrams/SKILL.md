---
name: ooad-diagrams
description: Generate or refresh the OOAD diagram set (use case, class, sequence, state, activity, component, deployment, ER) from the real code and export SVG and PNG for presentation. Use when code structure changes or when presentation diagrams are requested.
---

# OOAD Diagrams

1. Update the graph with `/graphify . --update` and read `GRAPH_REPORT.md`.
2. For each diagram listed in `.agents/agents/ooad-diagrammer.md`, derive content from the graph and the source files, not from memory.
3. Write each diagram as a mermaid block in the matching section of `docs/PROJECT.md`.
4. Extract each block to a temporary `.mmd` file outside `docs/` and render:
   - `npx -y @mermaid-js/mermaid-cli -i <tmp>.mmd -o docs/diagrams/<name>.svg`
   - `npx -y @mermaid-js/mermaid-cli -i <tmp>.mmd -o docs/diagrams/<name>.png -s 2 -b white`
5. Open each rendered file and check it is legible on one slide. Split large diagrams by bounded context.
6. Cross-check: every class name in the class diagram matches a real class; every state matches the enum in code; every table in the ER diagram matches a migration.
7. Delete the temporary `.mmd` files.

File names in `docs/diagrams/`: `01-use-case`, `02-class-domain`, `03-seq-timetable`, `04-seq-circular`, `05-seq-reminder`, `06-state-circular`, `07-state-notification`, `08-activity-timetable`, `09-component`, `10-deployment`, `11-er`.
