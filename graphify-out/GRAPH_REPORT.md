# Graph Report - facultydesk  (2026-10-27)

## Corpus Check
- 175 files · ~90,397 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: (none) 10, .csv 2, .example 1)

## Summary
- 1649 nodes · 4054 edges · 130 communities (96 shown, 34 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 523 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3a0e66d0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- parsers/__init__.py
- server.cjs
- domain/repositories.py
- main.py
- User
- calendar.py
- directory.py
- InvariantViolation
- domain/__init__.py
- get_settings
- Test-Driven Development (TDD)
- UnitOfWork
- auth.py
- db/__init__.py
- package.json
- Principal
- FacultyProfile
- Executing Plans
- test_domain_invariants.py
- test_timetable_pipeline.py
- deps.py
- Visual Companion Guide
- Creation Log: Systematic Debugging Skill
- compilerOptions
- timetable.py
- AcademicTerm
- 4. OOAD diagrams
- Root Cause Tracing
- Systematic Debugging
- RefreshToken
- components.json
- Condition-Based Waiting
- dependencies
- clash_detector.py
- Circular
- .__aenter__
- db.py
- Course
- Room
- Domain (backend/app/domain)
- with_server.py
- Defense-in-Depth Validation
- Writing Plans
- devDependencies
- Brainstorming
- Department
- Stage 01: Foundation, environment, Graphify, trusted skills
- FacultyDesk Agent Contract
- Verification Before Completion
- AsyncSession
- scripts
- helper.js
- layout.tsx
- Web Application Testing
- bulk_import.py
- NotificationRepositoryImpl
- page.tsx
- Stage 02: Domain model and persistence (OOAD core)
- Graphify Protocol
- Trusted External Skills
- stop-server.sh
- Frontend Design
- Section
- Task
- User
- Stage 03: Authentication, roles and faculty directory
- Stage 07: Meeting circular scanning, extraction and review queue
- Stage 08: Documentation tasks, priority scoring and alerts
- Code Quality Bar
- Documentation Rule
- Build Loop
- Math First
- ._transition
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- Stage 06: Reminder engine with exactly-once delivery
- Stage 10: Security, reliability and observability hardening
- Start here
- Architect
- Backend Engineer
- Frontend Engineer
- Math Verifier
- Orchestrator
- Reviewer
- Graphify Protocol
- Slop Review
- Pressure Test 1: Emergency Production Fix
- Pressure Test 2: Sunk Cost + Exhaustion
- Pressure Test 3: Authority + Social Pressure
- Stage 09: Frontend installable web app
- Stage 11: Production deployment, CI and end-to-end smoke test
- Stage 12: OOAD diagram pack and final audit
- DevOps Engineer
- Docs Writer
- OOAD Diagrammer
- Security and Safety
- eslint.config.mjs
- frontend/README.md
- Kickoff prompt (paste this into the Antigravity agent)
- start-server.sh
- builder-check-prompt.md
- ooad-diagrams/SKILL.md
- stage-verify/SKILL.md
- find-polluter.sh
- test-academic.md
- frontend/AGENTS.md
- facultydesk-backend

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 90 edges
2. `Principal` - 63 edges
3. `Clock` - 62 edges
4. `InvariantViolation` - 49 edges
5. `FacultyProfile` - 47 edges
6. `Event` - 44 edges
7. `User` - 36 edges
8. `Initials` - 36 edges
9. `AcademicTerm` - 33 edges
10. `AuditLog` - 33 edges

## Surprising Connections (you probably didn't know these)
- `5.4 Merged-Cell Period Expansion` --references--> `TimetableSlot`  [INFERRED]
  docs/MATHS.md → backend/app/domain/entities.py
- `Pipeline` --references--> `Circular`  [INFERRED]
  prompts/07-circular-ocr.md → backend/app/domain/entities.py
- `5.1 Initials Value Object Invariant` --references--> `InvariantViolation`  [INFERRED]
  docs/MATHS.md → backend/app/domain/errors.py
- `Persistence` --references--> `UnitOfWork`  [INFERRED]
  prompts/02-domain-model.md → backend/app/domain/repositories.py
- `10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix` --references--> `AuthorisationPolicy`  [INFERRED]
  docs/MATHS.md → backend/app/application/security/policy.py

## Import Cycles
- None detected.

## Communities (130 total, 34 thin omitted)

### Community 0 - "parsers/__init__.py"
Cohesion: 0.07
Nodes (42): OCR and Parsing Engineer, Responsibilities, Rules, split_co_teachers(), tokenize_cell(), CsvTimetableParser, _get_col(), _parse_clock_time() (+34 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 2 - "domain/repositories.py"
Cohesion: 0.04
Nodes (8): AcademicTermRepository, AuditLogRepository, CircularRepository, EventRepository, FacultyProfileRepository, NotificationRepository, TimetableSlotRepository, TimetableUploadRepository

### Community 3 - "main.py"
Cohesion: 0.09
Nodes (6): configure_logging(), RequestIdMiddleware, domain_exception_handler(), healthz(), lifespan(), readyz()

### Community 4 - "User"
Cohesion: 0.17
Nodes (15): ChangePasswordUseCase, LoginResult, LoginUseCase, RefreshResult, RefreshTokenUseCase, UnauthorizedError, create_access_token(), decode_token() (+7 more)

### Community 5 - "calendar.py"
Cohesion: 0.05
Nodes (42): CalendarEventResponse, cancel_calendar_event(), check_event_clashes(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots() (+34 more)

### Community 6 - "directory.py"
Cohesion: 0.10
Nodes (23): AcademicTermResponse, add_holiday(), bulk_import_faculty(), bulk_import_holidays(), BulkImportResponse, create_faculty(), create_term(), CreateAcademicTermRequest (+15 more)

### Community 7 - "InvariantViolation"
Cohesion: 0.13
Nodes (6): Holiday, PushSubscription, ReminderRule, InvariantViolation, holiday_to_domain(), 2. Features that exist now

### Community 8 - "domain/__init__.py"
Cohesion: 0.32
Nodes (11): EventAttendee, AttendeeResponse, CircularStatus, EventKind, EventSource, NotificationChannel, NotificationStatus, Role (+3 more)

### Community 9 - "get_settings"
Cohesion: 0.11
Nodes (11): get_uow(), get_settings(), Settings, SqlAlchemyUnitOfWork, get_storage_service(), materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation() (+3 more)

### Community 10 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 12 - "UnitOfWork"
Cohesion: 0.12
Nodes (6): get_clock(), Clock, SystemClock, UnitOfWork, Stage 01: Foundation, environment, Graphify, trusted skills, Tasks

### Community 13 - "auth.py"
Cohesion: 0.15
Nodes (15): change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest, LoginResponse (+7 more)

### Community 14 - "db/__init__.py"
Cohesion: 0.12
Nodes (14): Base, AcademicTermModel, AuditLogModel, EventAttendeeModel, EventModel, HolidayModel, PushSubscriptionModel, ReminderRuleModel (+6 more)

### Community 15 - "package.json"
Cohesion: 0.08
Nodes (25): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+17 more)

### Community 16 - "Principal"
Cohesion: 0.17
Nodes (18): require_admin(), require_hod_or_admin(), CreateFacultyUseCase, DeactivateFacultyUseCase, ManageTermsUseCase, UpdateFacultyUseCase, AuthorisationPolicy, Principal (+10 more)

### Community 18 - "FacultyProfile"
Cohesion: 0.36
Nodes (4): FacultyProfile, FacultyProfileModel, faculty_profile_to_domain(), FacultyProfileRepositoryImpl

### Community 19 - "Executing Plans"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 20 - "test_domain_invariants.py"
Cohesion: 0.06
Nodes (35): FrozenClock, QuietHours, test_clock_always_returns_utc_property(), test_frozen_clock_advance_property(), test_frozen_clock_rejects_naive_datetime(), test_circular_state_machine_exhaustive(), test_event_invariants(), test_initials_invalid_property() (+27 more)

### Community 21 - "test_timetable_pipeline.py"
Cohesion: 0.20
Nodes (5): ConfirmTimetableUseCase, ParseTimetableUseCase, UploadTimetableUseCase, MinioStorageService, test_timetable_upload_parse_and_confirm_pipeline()

### Community 22 - "deps.py"
Cohesion: 0.20
Nodes (7): get_current_principal(), get_rate_limiter(), get_storage(), RateLimitExceededError, get_redis_client(), RedisSlidingWindowRateLimiter, test_sliding_window_rate_limiter()

### Community 23 - "Visual Companion Guide"
Cohesion: 0.10
Nodes (19): Browser Events Format, Cards (visual designs), Cleaning Up, CSS Classes Available, Design Tips, File Naming, How It Works, Mock elements (wireframe building blocks) (+11 more)

### Community 24 - "Creation Log: Systematic Debugging Skill"
Cohesion: 0.10
Nodes (19): Bulletproofing Elements, Creation Log: Systematic Debugging Skill, Enhancement 1: TDD Reference, Extraction Decisions, Final Outcome, Initial Version, Iterations, Key Insight (+11 more)

### Community 25 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 26 - "timetable.py"
Cohesion: 0.17
Nodes (8): confirm_timetable(), ConfirmTimetableResponse, get_faculty_slots(), get_timetable_upload(), TimetableSlotResponse, TimetableUploadDetailResponse, upload_timetable(), UploadTimetableResponse

### Community 27 - "AcademicTerm"
Cohesion: 0.29
Nodes (10): expand_slot_recurrence(), AcademicTerm, TimetableSlot, TimeSlot, test_timeslot_half_open_overlap(), test_recurrence_expansion_matching_weekday(), test_recurrence_expansion_skips_holidays(), test_recurrence_expansion_utc_roundtrip() (+2 more)

### Community 28 - "4. OOAD diagrams"
Cohesion: 0.11
Nodes (17): 1. Problem and users, 3. Architecture, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine, 4.4 ScheduledNotification State Machine, 4.5 Entity-Relationship (ER) Diagram, 4.6 Authentication & Token Rotation Sequence (+9 more)

### Community 29 - "Root Cause Tracing"
Cohesion: 0.12
Nodes (15): 1. Observe the Symptom, 2. Find Immediate Cause, 3. Ask: What Called This?, 4. Keep Tracing Up, 5. Find Original Trigger, Adding Stack Traces, Finding Which Test Causes Pollution, Key Principle (+7 more)

### Community 30 - "Systematic Debugging"
Cohesion: 0.12
Nodes (15): Common Rationalizations, Overview, Phase 1: Root Cause Investigation, Phase 2: Pattern Analysis, Phase 3: Hypothesis and Testing, Phase 4: Implementation, Quick Reference, Red Flags - STOP and Follow Process (+7 more)

### Community 31 - "RefreshToken"
Cohesion: 0.19
Nodes (5): RefreshToken, RefreshTokenRepository, RefreshTokenModel, refresh_token_to_domain(), RefreshTokenRepositoryImpl

### Community 32 - "components.json"
Cohesion: 0.12
Nodes (15): aliases, components, hooks, lib, ui, utils, rsc, $schema (+7 more)

### Community 33 - "Condition-Based Waiting"
Cohesion: 0.15
Nodes (12): Common Mistakes, Condition-Based Waiting, Core Pattern, waitForEvent(), waitForEventCount(), waitForEventMatch(), Implementation, Overview (+4 more)

### Community 34 - "dependencies"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 35 - "clash_detector.py"
Cohesion: 0.12
Nodes (12): upgrade(), upgrade(), upgrade(), Interval, intervals_overlap(), pairwise_clashes(), SweepLineClashDetector, cleanup_db_connections() (+4 more)

### Community 36 - "Circular"
Cohesion: 0.24
Nodes (4): Circular, TimetableUpload, InvalidTransition, test_round_trip_all_aggregates()

### Community 37 - ".__aenter__"
Cohesion: 0.19
Nodes (6): TimetableSlotModel, TimetableUploadModel, timetable_slot_to_domain(), timetable_upload_to_domain(), TimetableSlotRepositoryImpl, TimetableUploadRepositoryImpl

### Community 38 - "db.py"
Cohesion: 0.18
Nodes (7): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_db(), main(), seed_database()

### Community 39 - "Course"
Cohesion: 0.26
Nodes (5): Course, CourseRepository, CourseModel, course_to_domain(), CourseRepositoryImpl

### Community 40 - "Room"
Cohesion: 0.26
Nodes (5): Room, RoomRepository, RoomModel, room_to_domain(), RoomRepositoryImpl

### Community 41 - "Domain (backend/app/domain)"
Cohesion: 0.30
Nodes (11): DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged, TimetableConfirmed, test_event_reschedule() (+3 more)

### Community 43 - "Defense-in-Depth Validation"
Cohesion: 0.17
Nodes (11): Applying the Pattern, Defense-in-Depth Validation, Example from Session, Key Insight, Layer 1: Entry Point Validation, Layer 2: Business Logic Validation, Layer 3: Environment Guards, Layer 4: Debug Instrumentation (+3 more)

### Community 44 - "Writing Plans"
Cohesion: 0.17
Nodes (11): Execution Handoff, File Structure, Overview, Plan Document Header, Scope Check, Self-Review, Step Granularity, Task Right-Sizing (+3 more)

### Community 45 - "devDependencies"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, eslint-config-next, openapi-typescript, prettier, prettier-plugin-tailwindcss, tailwindcss, @tailwindcss/turbopack (+4 more)

### Community 46 - "Brainstorming"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 47 - "Department"
Cohesion: 0.20
Nodes (5): Department, DepartmentRepository, DepartmentModel, department_to_domain(), DepartmentRepositoryImpl

### Community 48 - "Stage 01: Foundation, environment, Graphify, trusted skills"
Cohesion: 0.50
Nodes (3): Acceptance criteria, Goal, Stage 01: Foundation, environment, Graphify, trusted skills

### Community 51 - "FacultyDesk Agent Contract"
Cohesion: 0.20
Nodes (9): Architecture law, Communication style, Definition of done for every stage, FacultyDesk Agent Contract, Fixed tech stack (do not substitute), How work is organised, Non-negotiables, Product in one paragraph (+1 more)

### Community 52 - "Verification Before Completion"
Cohesion: 0.20
Nodes (9): Common Failures, Key Patterns, Overview, Rationalization Prevention, Red Flags - STOP, The Gate Function, The Iron Law, Verification Before Completion (+1 more)

### Community 53 - "AsyncSession"
Cohesion: 0.12
Nodes (3): CircularModel, circular_to_domain(), CircularRepositoryImpl

### Community 54 - "scripts"
Cohesion: 0.20
Nodes (10): scripts, build, dev, fmt, format:check, generate:api, lint, start (+2 more)

### Community 55 - "helper.js"
Cohesion: 0.42
Nodes (7): connect(), nextReconnectDelay(), reloadAfterRecovery(), sessionKey(), setStatus(), showTombstone(), websocketUrl()

### Community 58 - "layout.tsx"
Cohesion: 0.22
Nodes (5): nextConfig, geistMono, geistSans, metadata, next

### Community 59 - "Web Application Testing"
Cohesion: 0.25
Nodes (7): Best Practices, Common Pitfall, Decision Tree: Choosing Your Approach, Example: Using with_server.py, Reconnaissance-Then-Action Pattern, Reference Files, Web Application Testing

### Community 60 - "bulk_import.py"
Cohesion: 0.25
Nodes (5): BulkImportFacultyUseCase, BulkImportReport, RowImportResult, Initials, test_bulk_import_from_sample_csv()

### Community 61 - "NotificationRepositoryImpl"
Cohesion: 0.36
Nodes (3): ScheduledNotificationModel, notification_to_domain(), NotificationRepositoryImpl

### Community 62 - "page.tsx"
Cohesion: 0.39
Nodes (5): fetchInitialReadiness(), Home(), ReadinessData, ReadinessView(), react

### Community 63 - "Stage 02: Domain model and persistence (OOAD core)"
Cohesion: 0.25
Nodes (7): Acceptance criteria, Diagrams, Goal, Maths to specify first (MATHS.md), Persistence, Stage 02: Domain model and persistence (OOAD core), Tests

### Community 65 - "Graphify Protocol"
Cohesion: 0.29
Nodes (6): During the stage, End of every stage, Graphify Protocol, Install (stage 01 only, verify in every later stage), Start of every stage, Version control

### Community 66 - "Trusted External Skills"
Cohesion: 0.29
Nodes (6): 1. obra/superpowers (Jesse Vincent, MIT), 2. anthropics/skills (Anthropic, official), 3. safishamsi/graphify (Graphify), Local project skills (already in `.agents/skills/`), Trusted External Skills, Vetting rule for anything else

### Community 67 - "stop-server.sh"
Cohesion: 0.52
Nodes (6): command_has_server_id(), command_line_for_pid(), is_brainstorm_server(), mark_stopped(), read_expected_server_id(), stop-server.sh script

### Community 68 - "Frontend Design"
Cohesion: 0.29
Nodes (6): Design principles, Frontend Design, Ground your designs in the subject matter, More on writing in design, Process: plan, review against the brief, build, critique, Restraint and self-critique

### Community 69 - "Section"
Cohesion: 0.29
Nodes (5): Section, SectionRepository, SectionModel, section_to_domain(), SectionRepositoryImpl

### Community 70 - "Task"
Cohesion: 0.26
Nodes (5): Task, TaskRepository, TaskModel, task_to_domain(), TaskRepositoryImpl

### Community 71 - "User"
Cohesion: 0.30
Nodes (4): User, UserRepository, user_to_domain(), UserRepositoryImpl

### Community 73 - "Stage 03: Authentication, roles and faculty directory"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Maths to specify first, Stage 03: Authentication, roles and faculty directory, Tasks, Tests

### Community 74 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Corpus and tests, Goal, Maths to specify first, Pipeline, Stage 07: Meeting circular scanning, extraction and review queue

### Community 75 - "Stage 08: Documentation tasks, priority scoring and alerts"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Maths to specify first, Stage 08: Documentation tasks, priority scoring and alerts, Tasks, Tests

### Community 76 - "Code Quality Bar"
Cohesion: 0.33
Nodes (5): Code Quality Bar, Forbidden patterns (slop detector), Python, Review before you finish, TypeScript

### Community 77 - "Documentation Rule"
Cohesion: 0.33
Nodes (5): docs/DECISIONS.md (what was done and why), docs/MATHS.md (how the logic is proven), docs/PROJECT.md (what the system is), Documentation Rule, Writing style for all three

### Community 78 - "Build Loop"
Cohesion: 0.33
Nodes (5): Build Loop, Finish, Loop, progress.json shape, Stop conditions

### Community 79 - "Math First"
Cohesion: 0.33
Nodes (5): Math First, Step 1: Specify, Step 2: Test, Step 3: Implement, Step 4: Prove

### Community 82 - "Stage 05: Calendar core, recurrence, clash detection, ICS feed"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 05: Calendar core, recurrence, clash detection, ICS feed, Tests

### Community 83 - "Stage 06: Reminder engine with exactly-once delivery"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 06: Reminder engine with exactly-once delivery, Tests

### Community 84 - "Stage 10: Security, reliability and observability hardening"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 10: Security, reliability and observability hardening, Tasks

### Community 85 - "Start here"
Cohesion: 0.33
Nodes (5): Before you start (one time, about 10 minutes), Run, Start here, What this folder is, What to show your guide

### Community 86 - "Architect"
Cohesion: 0.40
Nodes (4): Architect, Design checks, Output for every design task, Responsibilities

### Community 87 - "Backend Engineer"
Cohesion: 0.40
Nodes (4): Backend Engineer, Responsibilities, Standards you are held to, Working method

### Community 88 - "Frontend Engineer"
Cohesion: 0.40
Nodes (4): Design bar, Frontend Engineer, Responsibilities, Rules

### Community 89 - "Math Verifier"
Cohesion: 0.40
Nodes (4): After implementation, Before implementation, Core specifications this project needs (owner of each section), Math Verifier

### Community 90 - "Orchestrator"
Cohesion: 0.40
Nodes (4): Orchestrator, Ownership table, Responsibilities, You never

### Community 91 - "Reviewer"
Cohesion: 0.40
Nodes (4): Output, Procedure, Reviewer, Things you always look for

### Community 92 - "Graphify Protocol"
Cohesion: 0.40
Nodes (4): Before writing a helper or new class, End of stage, Graphify Protocol, Start of stage

### Community 93 - "Slop Review"
Cohesion: 0.40
Nodes (4): Judgement checks, Mechanical checks (run them, paste results), Output, Slop Review

### Community 94 - "Pressure Test 1: Emergency Production Fix"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 1: Emergency Production Fix, Scenario, Your Options

### Community 95 - "Pressure Test 2: Sunk Cost + Exhaustion"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 2: Sunk Cost + Exhaustion, Scenario, Your Options

### Community 96 - "Pressure Test 3: Authority + Social Pressure"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 3: Authority + Social Pressure, Scenario, Your Options

### Community 97 - "Stage 09: Frontend installable web app"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 09: Frontend installable web app, Tasks

### Community 98 - "Stage 11: Production deployment, CI and end-to-end smoke test"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 11: Production deployment, CI and end-to-end smoke test, Tasks

### Community 99 - "Stage 12: OOAD diagram pack and final audit"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 12: OOAD diagram pack and final audit, Tasks

### Community 100 - "DevOps Engineer"
Cohesion: 0.50
Nodes (3): DevOps Engineer, Responsibilities, Rules

### Community 101 - "Docs Writer"
Cohesion: 0.50
Nodes (3): Docs Writer, Responsibilities, Style

### Community 102 - "OOAD Diagrammer"
Cohesion: 0.50
Nodes (3): Diagram set (kept in docs/PROJECT.md, exported to docs/diagrams/), OOAD Diagrammer, Rules

### Community 103 - "Security and Safety"
Cohesion: 0.50
Nodes (3): Agent safety while building, Application security, Security and Safety

### Community 104 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): eslintConfig, eslint, eslint-config-next

### Community 105 - "frontend/README.md"
Cohesion: 0.50
Nodes (3): Deploy on Vercel, Getting Started, Learn More

### Community 106 - "Kickoff prompt (paste this into the Antigravity agent)"
Cohesion: 0.50
Nodes (3): Kickoff prompt (paste this into the Antigravity agent), Resuming in a new conversation, Running a single stage manually

## Knowledge Gaps
- **23 isolated node(s):** `RFC-6455`, `facultydesk-backend`, `clsx`, `@fullcalendar/core`, `@fullcalendar/daygrid` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 695 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `domain/repositories.py`, `User`, `calendar.py`, `directory.py`, `domain/__init__.py`, `get_settings`, `Domain (backend/app/domain)`, `auth.py`, `Principal`, `test_timetable_pipeline.py`, `deps.py`, `timetable.py`, `AcademicTerm`, `bulk_import.py`, `Stage 02: Domain model and persistence (OOAD core)`, `RefreshToken`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RFC-6455`, `facultydesk-backend`, `clsx` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `parsers/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06751054852320675 - nodes in this community are weakly interconnected._
- **Why does `Clock` connect `UnitOfWork` to `User`, `calendar.py`, `directory.py`, `InvariantViolation`, `get_settings`, `auth.py`, `Principal`, `FacultyDesk Agent Contract`, `test_domain_invariants.py`, `test_timetable_pipeline.py`, `deps.py`, `Backend Engineer`, `timetable.py`, `bulk_import.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `Principal` (e.g. with `require_admin()` and `require_hod_or_admin()`) actually correct?**
  _`Principal` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._