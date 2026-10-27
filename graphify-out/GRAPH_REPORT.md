# Graph Report - facultydesk  (2026-10-27)

## Corpus Check
- 117 files · ~57,770 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: (none) 10, .example 1, .ini 1)

## Summary
- 1111 nodes · 1886 edges · 98 communities (71 shown, 27 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 211 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2c3c19e3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- server.cjs
- security.py
- FacultyDeskError
- Test-Driven Development (TDD)
- package.json
- Executing Plans
- Visual Companion Guide
- Creation Log: Systematic Debugging Skill
- compilerOptions
- app/main.py
- Root Cause Tracing
- Systematic Debugging
- components.json
- Condition-Based Waiting
- dependencies
- Defense-in-Depth Validation
- Writing Plans
- config.py
- ScheduledNotification
- devDependencies
- Brainstorming
- Verification Before Completion
- with_server.py
- env.py
- scripts
- helper.js
- layout.tsx
- Web Application Testing
- db/repositories.py
- logging.py
- page.tsx
- Stage 04: Timetable upload, parsing and initials resolution
- Graphify Protocol
- Trusted External Skills
- stop-server.sh
- Frontend Design
- FacultyDesk
- Stage 03: Authentication, roles and faculty directory
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- Stage 06: Reminder engine with exactly-once delivery
- Circular
- Stage 08: Documentation tasks, priority scoring and alerts
- Code Quality Bar
- Documentation Rule
- Build Loop
- Math First
- Stage 10: Security, reliability and observability hardening
- Start here
- Frontend Engineer
- Math Verifier
- Orchestrator
- Reviewer
- Graphify Protocol
- Slop Review
- Pressure Test 1: Emergency Production Fix
- Pressure Test 2: Sunk Cost + Exhaustion
- Pressure Test 3: Authority + Social Pressure
- RequestIdMiddleware
- Stage 09: Frontend installable web app
- Stage 11: Production deployment, CI and end-to-end smoke test
- Stage 12: OOAD diagram pack and final audit
- DevOps Engineer
- Docs Writer
- OCR and Parsing Engineer
- OOAD Diagrammer
- Security and Safety
- eslint.config.mjs
- frontend/README.md
- Kickoff prompt (paste this into the Antigravity agent)
- start-server.sh
- AcademicTerm
- builder-check-prompt.md
- ooad-diagrams/SKILL.md
- stage-verify/SKILL.md
- find-polluter.sh
- test-academic.md
- frontend/AGENTS.md
- domain/__init__.py
- facultydesk-backend
- ScheduledNotification
- Department
- Stage 02: Domain model and persistence (OOAD core)
- sqlalchemy
- Architect

## God Nodes (most connected - your core abstractions)
1. `InvariantViolation` - 44 edges
2. `ScheduledNotification` - 33 edges
3. `Event` - 31 edges
4. `Circular` - 29 edges
5. `Domain (backend/app/domain)` - 29 edges
6. `Task` - 26 edges
7. `Stage 02: Domain model and persistence (OOAD core)` - 25 edges
8. `FacultyProfile` - 24 edges
9. `2. Features that exist now` - 24 edges
10. `Base` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Persistence` --references--> `UnitOfWork`  [INFERRED]
  prompts/02-domain-model.md → backend/app/domain/repositories.py
- `Standards you are held to` --references--> `Clock`  [INFERRED]
  .agents/agents/backend-engineer.md → backend/app/core/clock.py
- `Non-negotiables` --references--> `Clock`  [INFERRED]
  AGENTS.md → backend/app/core/clock.py
- `2. Features that exist now` --references--> `Clock`  [INFERRED]
  docs/PROJECT.md → backend/app/core/clock.py
- `2. Features that exist now` --references--> `SystemClock`  [INFERRED]
  docs/PROJECT.md → backend/app/core/clock.py

## Import Cycles
- None detected.

## Communities (98 total, 27 thin omitted)

### Community 0 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 1 - "security.py"
Cohesion: 0.06
Nodes (29): Backend Engineer, Responsibilities, Standards you are held to, Working method, Architecture law, Communication style, Definition of done for every stage, FacultyDesk Agent Contract (+21 more)

### Community 2 - "FacultyDeskError"
Cohesion: 0.25
Nodes (7): ConflictError, FacultyDeskError, ForbiddenError, InvalidTransition, NotFoundError, UnauthorizedError, ValidationError

### Community 3 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 4 - "package.json"
Cohesion: 0.08
Nodes (25): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+17 more)

### Community 5 - "Executing Plans"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 6 - "Visual Companion Guide"
Cohesion: 0.10
Nodes (19): Browser Events Format, Cards (visual designs), Cleaning Up, CSS Classes Available, Design Tips, File Naming, How It Works, Mock elements (wireframe building blocks) (+11 more)

### Community 7 - "Creation Log: Systematic Debugging Skill"
Cohesion: 0.10
Nodes (19): Bulletproofing Elements, Creation Log: Systematic Debugging Skill, Enhancement 1: TDD Reference, Extraction Decisions, Final Outcome, Initial Version, Iterations, Key Insight (+11 more)

### Community 8 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 9 - "app/main.py"
Cohesion: 0.14
Nodes (4): domain_exception_handler(), healthz(), lifespan(), readyz()

### Community 10 - "Root Cause Tracing"
Cohesion: 0.12
Nodes (15): 1. Observe the Symptom, 2. Find Immediate Cause, 3. Ask: What Called This?, 4. Keep Tracing Up, 5. Find Original Trigger, Adding Stack Traces, Finding Which Test Causes Pollution, Key Principle (+7 more)

### Community 11 - "Systematic Debugging"
Cohesion: 0.12
Nodes (15): Common Rationalizations, Overview, Phase 1: Root Cause Investigation, Phase 2: Pattern Analysis, Phase 3: Hypothesis and Testing, Phase 4: Implementation, Quick Reference, Red Flags - STOP and Follow Process (+7 more)

### Community 12 - "components.json"
Cohesion: 0.12
Nodes (15): aliases, components, hooks, lib, ui, utils, rsc, $schema (+7 more)

### Community 13 - "Condition-Based Waiting"
Cohesion: 0.15
Nodes (12): Common Mistakes, Condition-Based Waiting, Core Pattern, waitForEvent(), waitForEventCount(), waitForEventMatch(), Implementation, Overview (+4 more)

### Community 14 - "dependencies"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 15 - "Defense-in-Depth Validation"
Cohesion: 0.17
Nodes (11): Applying the Pattern, Defense-in-Depth Validation, Example from Session, Key Insight, Layer 1: Entry Point Validation, Layer 2: Business Logic Validation, Layer 3: Environment Guards, Layer 4: Debug Instrumentation (+3 more)

### Community 16 - "Writing Plans"
Cohesion: 0.17
Nodes (11): Execution Handoff, File Structure, Overview, Plan Document Header, Scope Check, Self-Review, Step Granularity, Task Right-Sizing (+3 more)

### Community 18 - "ScheduledNotification"
Cohesion: 0.09
Nodes (25): QuietHours, test_circular_state_machine_exhaustive(), test_event_invariants(), test_initials_invalid_property(), test_initials_valid_property(), test_notification_state_machine_exhaustive(), test_quiet_hours_midnight_crossing(), test_task_invariants() (+17 more)

### Community 19 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, eslint-config-next, openapi-typescript, prettier, prettier-plugin-tailwindcss, tailwindcss, @tailwindcss/turbopack (+4 more)

### Community 20 - "Brainstorming"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 22 - "Verification Before Completion"
Cohesion: 0.20
Nodes (9): Common Failures, Key Patterns, Overview, Rationalization Prevention, Red Flags - STOP, The Gate Function, The Iron Law, Verification Before Completion (+1 more)

### Community 24 - "env.py"
Cohesion: 0.29
Nodes (5): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_settings()

### Community 25 - "scripts"
Cohesion: 0.20
Nodes (10): scripts, build, dev, fmt, format:check, generate:api, lint, start (+2 more)

### Community 26 - "helper.js"
Cohesion: 0.42
Nodes (7): connect(), nextReconnectDelay(), reloadAfterRecovery(), sessionKey(), setStatus(), showTombstone(), websocketUrl()

### Community 27 - "layout.tsx"
Cohesion: 0.22
Nodes (5): nextConfig, geistMono, geistSans, metadata, next

### Community 28 - "Web Application Testing"
Cohesion: 0.25
Nodes (7): Best Practices, Common Pitfall, Decision Tree: Choosing Your Approach, Example: Using with_server.py, Reconnaissance-Then-Action Pattern, Reference Files, Web Application Testing

### Community 29 - "db/repositories.py"
Cohesion: 0.09
Nodes (29): Base, get_db(), AuditLog, User, AuditLogRepository, UserRepository, AcademicTermModel, AuditLogModel (+21 more)

### Community 31 - "page.tsx"
Cohesion: 0.39
Nodes (5): fetchInitialReadiness(), Home(), ReadinessData, ReadinessView(), react

### Community 32 - "Stage 04: Timetable upload, parsing and initials resolution"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Input formats to support, Maths to specify first, Stage 04: Timetable upload, parsing and initials resolution, Tests

### Community 33 - "Graphify Protocol"
Cohesion: 0.29
Nodes (6): During the stage, End of every stage, Graphify Protocol, Install (stage 01 only, verify in every later stage), Start of every stage, Version control

### Community 34 - "Trusted External Skills"
Cohesion: 0.29
Nodes (6): 1. obra/superpowers (Jesse Vincent, MIT), 2. anthropics/skills (Anthropic, official), 3. safishamsi/graphify (Graphify), Local project skills (already in `.agents/skills/`), Trusted External Skills, Vetting rule for anything else

### Community 35 - "stop-server.sh"
Cohesion: 0.52
Nodes (6): command_has_server_id(), command_line_for_pid(), is_brainstorm_server(), mark_stopped(), read_expected_server_id(), stop-server.sh script

### Community 36 - "Frontend Design"
Cohesion: 0.29
Nodes (6): Design principles, Frontend Design, Ground your designs in the subject matter, More on writing in design, Process: plan, review against the brief, build, critique, Restraint and self-critique

### Community 37 - "FacultyDesk"
Cohesion: 0.14
Nodes (13): 1. Problem and users, 3. Architecture, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine, 4.4 ScheduledNotification State Machine, 4.5 Entity-Relationship (ER) Diagram, 4. OOAD diagrams (+5 more)

### Community 38 - "Stage 03: Authentication, roles and faculty directory"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Maths to specify first, Stage 03: Authentication, roles and faculty directory, Tasks, Tests

### Community 39 - "Stage 05: Calendar core, recurrence, clash detection, ICS feed"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 05: Calendar core, recurrence, clash detection, ICS feed, Tests

### Community 40 - "Stage 06: Reminder engine with exactly-once delivery"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 06: Reminder engine with exactly-once delivery, Tests

### Community 41 - "Circular"
Cohesion: 0.06
Nodes (20): Circular, FacultyProfile, Task, CircularRepository, FacultyProfileRepository, TaskRepository, Initials, circular_to_domain() (+12 more)

### Community 42 - "Stage 08: Documentation tasks, priority scoring and alerts"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Maths to specify first, Stage 08: Documentation tasks, priority scoring and alerts, Tasks, Tests

### Community 43 - "Code Quality Bar"
Cohesion: 0.33
Nodes (5): Code Quality Bar, Forbidden patterns (slop detector), Python, Review before you finish, TypeScript

### Community 44 - "Documentation Rule"
Cohesion: 0.33
Nodes (5): docs/DECISIONS.md (what was done and why), docs/MATHS.md (how the logic is proven), docs/PROJECT.md (what the system is), Documentation Rule, Writing style for all three

### Community 45 - "Build Loop"
Cohesion: 0.33
Nodes (5): Build Loop, Finish, Loop, progress.json shape, Stop conditions

### Community 46 - "Math First"
Cohesion: 0.33
Nodes (5): Math First, Step 1: Specify, Step 2: Test, Step 3: Implement, Step 4: Prove

### Community 48 - "Stage 10: Security, reliability and observability hardening"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 10: Security, reliability and observability hardening, Tasks

### Community 49 - "Start here"
Cohesion: 0.33
Nodes (5): Before you start (one time, about 10 minutes), Run, Start here, What this folder is, What to show your guide

### Community 50 - "Frontend Engineer"
Cohesion: 0.40
Nodes (4): Design bar, Frontend Engineer, Responsibilities, Rules

### Community 51 - "Math Verifier"
Cohesion: 0.40
Nodes (4): After implementation, Before implementation, Core specifications this project needs (owner of each section), Math Verifier

### Community 52 - "Orchestrator"
Cohesion: 0.40
Nodes (4): Orchestrator, Ownership table, Responsibilities, You never

### Community 53 - "Reviewer"
Cohesion: 0.40
Nodes (4): Output, Procedure, Reviewer, Things you always look for

### Community 54 - "Graphify Protocol"
Cohesion: 0.40
Nodes (4): Before writing a helper or new class, End of stage, Graphify Protocol, Start of stage

### Community 55 - "Slop Review"
Cohesion: 0.40
Nodes (4): Judgement checks, Mechanical checks (run them, paste results), Output, Slop Review

### Community 56 - "Pressure Test 1: Emergency Production Fix"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 1: Emergency Production Fix, Scenario, Your Options

### Community 57 - "Pressure Test 2: Sunk Cost + Exhaustion"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 2: Sunk Cost + Exhaustion, Scenario, Your Options

### Community 58 - "Pressure Test 3: Authority + Social Pressure"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 3: Authority + Social Pressure, Scenario, Your Options

### Community 60 - "Stage 09: Frontend installable web app"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 09: Frontend installable web app, Tasks

### Community 61 - "Stage 11: Production deployment, CI and end-to-end smoke test"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 11: Production deployment, CI and end-to-end smoke test, Tasks

### Community 62 - "Stage 12: OOAD diagram pack and final audit"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 12: OOAD diagram pack and final audit, Tasks

### Community 63 - "DevOps Engineer"
Cohesion: 0.50
Nodes (3): DevOps Engineer, Responsibilities, Rules

### Community 64 - "Docs Writer"
Cohesion: 0.50
Nodes (3): Docs Writer, Responsibilities, Style

### Community 65 - "OCR and Parsing Engineer"
Cohesion: 0.50
Nodes (3): OCR and Parsing Engineer, Responsibilities, Rules

### Community 66 - "OOAD Diagrammer"
Cohesion: 0.50
Nodes (3): Diagram set (kept in docs/PROJECT.md, exported to docs/diagrams/), OOAD Diagrammer, Rules

### Community 67 - "Security and Safety"
Cohesion: 0.50
Nodes (3): Agent safety while building, Application security, Security and Safety

### Community 68 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): eslintConfig, eslint, eslint-config-next

### Community 69 - "frontend/README.md"
Cohesion: 0.50
Nodes (3): Deploy on Vercel, Getting Started, Learn More

### Community 70 - "Kickoff prompt (paste this into the Antigravity agent)"
Cohesion: 0.50
Nodes (3): Kickoff prompt (paste this into the Antigravity agent), Resuming in a new conversation, Running a single stage manually

### Community 72 - "AcademicTerm"
Cohesion: 0.14
Nodes (6): AcademicTerm, Holiday, AcademicTermRepository, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 85 - "domain/__init__.py"
Cohesion: 0.06
Nodes (40): Course, Event, EventAttendee, PushSubscription, ReminderRule, Room, Section, TimetableSlot (+32 more)

### Community 96 - "ScheduledNotification"
Cohesion: 0.11
Nodes (5): ScheduledNotification, NotificationRepository, notification_to_domain(), NotificationRepositoryImpl, SqlAlchemyUnitOfWork

### Community 97 - "Department"
Cohesion: 0.11
Nodes (4): Department, DepartmentRepository, department_to_domain(), DepartmentRepositoryImpl

### Community 102 - "Stage 02: Domain model and persistence (OOAD core)"
Cohesion: 0.25
Nodes (7): Acceptance criteria, Diagrams, Goal, Maths to specify first (MATHS.md), Persistence, Stage 02: Domain model and persistence (OOAD core), Tests

### Community 106 - "Architect"
Cohesion: 0.40
Nodes (4): Architect, Design checks, Output for every design task, Responsibilities

## Knowledge Gaps
- **23 isolated node(s):** `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 601 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `2. Features that exist now` connect `domain/__init__.py` to `ScheduledNotification`, `security.py`, `Department`, `FacultyDesk`, `AcademicTerm`, `Circular`, `db/repositories.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `InvariantViolation` (e.g. with `AcademicTerm` and `AuditLog`) actually correct?**
  _`InvariantViolation` has 19 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._
- **Why does `Clock` connect `security.py` to `domain/__init__.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `ScheduledNotification` (e.g. with `InvalidTransition` and `InvariantViolation`) actually correct?**
  _`ScheduledNotification` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `security.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05656565656565657 - nodes in this community are weakly interconnected._