---
trigger: always_on
description: The three-document rule and how each document is written
---

# Documentation Rule

`docs/` holds exactly three Markdown files. Never create a fourth. Exported diagram images may live in `docs/diagrams/`.

## docs/PROJECT.md (what the system is)

Audience: the faculty guide evaluating the OOAD project and a new developer.

Sections, kept current every stage:
1. Problem and users (actors: Admin, HOD, Faculty, System Scheduler).
2. Features that exist right now (only what is built, never what is planned).
3. Architecture overview with a mermaid component diagram.
4. OOAD diagrams in mermaid: use case (as a flowchart with actor nodes), class diagram, sequence diagrams for the main flows, state diagrams for Circular and ScheduledNotification, activity diagram for timetable ingestion, ER diagram, deployment diagram.
5. How to run, test and deploy.

## docs/MATHS.md (how the logic is proven)

For every algorithm, in this order:
1. Plain-language explanation a second-year student can follow.
2. The formula or pseudocode, with every symbol defined.
3. One worked example with real numbers or real strings.
4. Edge cases and how each is handled.
5. Time and space complexity.
6. The test names that prove it.

Required sections (fill as stages reach them): Time and Recurrence, Clash Detection, Reminder Scheduling, Exactly-Once Delivery, Initials and Name Matching, OCR Confidence, Date and Time Extraction, Task Priority and Alerts, Retry Backoff, Security Limits.

## docs/DECISIONS.md (what was done and why)

One entry per stage, newest at the bottom, in this shape:

- **Stage NN: title**
- What we built (three to six bullets).
- Why this way (justification tied to a requirement or a constraint).
- What we rejected and why.
- Risks and how they are contained.
- A small mermaid diagram of what changed.

## Writing style for all three

Short sentences. Plain words. No marketing tone, no emojis, no padding. Prefer a diagram or a table over a long paragraph. Every mermaid block must render: validate syntax before saving (use `npx -y @mermaid-js/mermaid-cli` to render each block to `docs/diagrams/` when a stage changes it).
