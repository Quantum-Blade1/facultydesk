---
trigger: always_on
description: The only external skill sources allowed, how to install them, and when to use each
---

# Trusted External Skills

Only the sources below may be installed. Each is public, open source, widely used and maintained by a known author or company. Before installing, open the repository and read every `SKILL.md` you will load; a skill is executable instructions, so treat it like code you are about to run.

## 1. obra/superpowers (Jesse Vincent, MIT)

Repository: https://github.com/obra/superpowers

Install for Antigravity: `agy plugin install https://github.com/obra/superpowers`
If the CLI is unavailable, clone the repo and copy only the skills listed below into `.agents/skills/`.

Use these skills, and only these:

| Skill | When to use it in this project |
|---|---|
| `brainstorming` | Start of stage 02 (domain design) and any stage whose prompt says "design first" |
| `writing-plans` | Turning a stage prompt into a task list before coding |
| `executing-plans` | Working through that task list |
| `test-driven-development` | Every domain service, parser, matcher and scheduler. Red, green, refactor |
| `systematic-debugging` | Any failing test, failing boot or unexpected behaviour. Root cause before fix |
| `verification-before-completion` | Before marking any stage done |
| `requesting-code-review` | End of every stage, run against the stage diff in the reviewer role |

Do not use its worktree or branch-finishing skills; this project commits on `main` stage by stage.

## 2. anthropics/skills (Anthropic, official)

Repository: https://github.com/anthropics/skills

Copy only these folders into `.agents/skills/`:

| Skill | When |
|---|---|
| `frontend-design` | Stage 09, before building any screen |
| `webapp-testing` | Stage 11, Playwright smoke test of the running app |

## 3. safishamsi/graphify (Graphify)

Repository: https://github.com/safishamsi/graphify. PyPI package `graphifyy`. Used in every stage per `02-graphify.md`.

## Local project skills (already in `.agents/skills/`)

`build-loop`, `graphify-protocol`, `math-first`, `slop-review`, `stage-verify`, `ooad-diagrams`. These were written for this repository and take priority over any external skill with an overlapping purpose.

## Vetting rule for anything else

Do not add any other skill source. If you believe one is needed, write the case in `progress.json` under `blockers` and continue without it. A human decides.
