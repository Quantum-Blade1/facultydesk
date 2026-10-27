---
name: build-loop
description: Runs the FacultyDesk build stage by stage from prompts/ until every stage is done, updating .agents/state/progress.json after each one. Use when asked to start, continue or resume the build.
---

# Build Loop

This skill is the project's autonomous runner. It replaces legacy workflows.

## Loop

Repeat until a stop condition is met:

1. **Load state.** Read `.agents/state/progress.json`. Find the lowest-numbered stage whose `status` is not `done`. If none remain, go to Finish.
2. **Load context.** Read `AGENTS.md`, every file in `.agents/rules/`, `.agents/agents/orchestrator.md` and the stage file `prompts/<file>`.
3. **Mark started.** Set the stage `status` to `in_progress` and `started_at` to the current time. Save the file.
4. **Graphify start.** Follow the `graphify-protocol` skill, start section.
5. **Plan.** Turn the stage prompt into an ordered task list with an owning role for each task. If superpowers `writing-plans` is installed, use it. Save the list into the stage's `tasks` array in `progress.json`.
6. **Maths first.** For every algorithm in the stage, run the `math-first` skill before writing its code.
7. **Execute.** For each task, adopt its role file and complete it. Run tests after every task, not only at the end. On any failure, use superpowers `systematic-debugging` if installed, otherwise reproduce, isolate, find root cause, then fix. Never weaken a test to make it pass.
8. **Review.** Adopt `reviewer` and run the `slop-review` skill on the stage diff. Fix every blocker and major. Re-review.
9. **Diagrams and docs.** Adopt `ooad-diagrammer`, then `docs-writer`. Update the three docs.
10. **Verify.** Run the `stage-verify` skill. If any check fails, return to step 7 for that item. Allow at most three full verify attempts per stage.
11. **Graphify end.** Follow the `graphify-protocol` skill, end section.
12. **Commit and record.** Commit as `feat(stage-NN): <summary>`. In `progress.json` set `status` to `done`, `finished_at`, `commit`, and a short `evidence` list. Save.
13. **Report.** Print the stage completion report (files changed, commands with results, each acceptance criterion with pass and evidence, known limitations).
14. **Continue** with the next stage without waiting for the user, unless a stop condition applies.

## Stop conditions

Stop the loop, set the stage `status` to `blocked`, write the reason under `blockers`, and tell the user exactly what is needed when:

- A decision cannot be undone and could reasonably go either way (for example deleting data, changing a public contract already in use).
- A required secret or external account is missing (SMTP credentials, VAPID keys you cannot generate, a domain name for production).
- Three verify attempts on the same stage have failed.
- A dependency outside the approved stack would be required.
- The user says stop.

Generating VAPID keys, dev secrets and self-signed dev certificates is not a stop condition; do it and record it.

## Finish

When all stages are `done`: run the full test suite, `make up` from cold, the Playwright smoke test from stage 11, regenerate all diagrams, and print a final summary with the URL to open and the demo logins created by `make seed`.

## progress.json shape

```json
{
  "project": "FacultyDesk",
  "current_stage": "01",
  "stages": [
    {"id": "01", "file": "01-foundation.md", "status": "pending", "started_at": null, "finished_at": null, "commit": null, "tasks": [], "evidence": []}
  ],
  "blockers": [],
  "decisions_pending": []
}
```
