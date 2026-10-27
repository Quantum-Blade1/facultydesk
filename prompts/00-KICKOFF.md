# Kickoff prompt (paste this into the Antigravity agent)

Copy everything inside the block into a new Antigravity agent conversation opened on this folder. Use the strongest reasoning model available in your Antigravity model picker.

```
You are the lead engineer on FacultyDesk. This workspace is already configured for you.

Before doing anything else, read in this order:
1. AGENTS.md
2. Every file in .agents/rules/
3. .agents/agents/orchestrator.md
4. .agents/skills/build-loop/SKILL.md
5. .agents/state/progress.json

Then run the build-loop skill and keep running it, stage after stage, until every stage in progress.json is done or a stop condition in that skill is reached.

Hard requirements for the whole run:
- Run the Graphify protocol at the start and end of every stage and use the graph to locate code before opening files.
- Install only the trusted skills listed in .agents/rules/05-trusted-skills.md, and read each SKILL.md before keeping it.
- Specify every algorithm in docs/MATHS.md before implementing it, and prove it with targeted tests.
- No comments in code, no TODOs, no placeholders, no fake logic. Senior-level code only.
- Keep exactly three Markdown files in docs/: PROJECT.md, MATHS.md, DECISIONS.md, written in plain human language with mermaid diagrams.
- Do not mark a stage done without pasted evidence for every acceptance criterion.
- Update .agents/state/progress.json after every stage so the build can resume in a new conversation.

Start now with stage 01.
```

## Resuming in a new conversation

If the conversation gets long or Antigravity stops, open a new agent conversation and paste:

```
Read AGENTS.md, .agents/rules/, .agents/skills/build-loop/SKILL.md and .agents/state/progress.json. Resume the build-loop from the first stage that is not done. If a stage is in_progress, run the graphify start protocol, check what was already completed against its task list, and continue from there.
```

## Running a single stage manually

```
Read AGENTS.md and .agents/rules/. Execute prompts/NN-name.md only, following the build-loop steps 3 to 13 for that one stage, then stop.
```
