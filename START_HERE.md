# Start here

## What this folder is

An Antigravity workspace that builds FacultyDesk by itself, stage by stage, until the product is finished.

```
facultydesk/
  AGENTS.md                 main rules Antigravity loads every session
  START_HERE.md             this file
  prompts/
    00-KICKOFF.md           the one prompt you paste to start
    01 ... 12               the stages, run in order by the agent
  .agents/
    rules/                  always-on rules (quality, graphify, docs, security, trusted skills)
    agents/                 roles: orchestrator, architect, backend, ocr, frontend, devops,
                            math-verifier, reviewer, ooad-diagrammer, docs-writer
    skills/                 build-loop, graphify-protocol, math-first, slop-review,
                            stage-verify, ooad-diagrams
    state/progress.json     where the loop records progress
  docs/
    PROJECT.md  MATHS.md  DECISIONS.md   the only three docs
```

## Before you start (one time, about 10 minutes)

1. Install Docker Desktop and make sure it is running.
2. Install `uv` (`brew install uv`) and `pnpm` (`brew install pnpm`), and Node 20 or newer.
3. Open this folder in Antigravity as the workspace.
4. In Antigravity settings, allow the agent to run terminal commands without asking each time for this workspace, otherwise the loop will pause on every command.
5. Pick the strongest model in the model picker.

## Run

1. Open `prompts/00-KICKOFF.md`.
2. Copy the first block into a new agent conversation.
3. Let it run. Check `.agents/state/progress.json` to see which stage it is on.
4. If it stops on a blocker, it will say exactly what it needs (for example SMTP details). Answer, then paste the resume prompt from the same file.

## What to show your guide

After stage 12, `docs/diagrams/` has the OOAD diagrams as SVG and PNG, and `docs/PROJECT.md` has the OOAD summary and the requirements traceability table.
