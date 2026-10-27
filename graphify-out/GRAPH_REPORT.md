# Graph Report - facultydesk  (2026-10-27)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1827 nodes · 4753 edges · 137 communities (104 shown, 33 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 603 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `565c88c6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- parsers/__init__.py
- server.cjs
- datetime
- main.py
- User
- bulk_import_faculty
- directory.py
- clash_detector.py
- db/repositories.py
- get_settings
- Test-Driven Development (TDD)
- Test-Driven Development (TDD)
- UnitOfWork
- UnitOfWork
- package.json
- Principal
- package.json
- reminders.py
- Executing Plans
- reminders/use_cases.py
- Executing Plans
- deps.py
- Visual Companion Guide
- Creation Log: Systematic Debugging Skill
- compilerOptions
- timetable.py
- Visual Companion Guide
- 4. OOAD diagrams
- Root Cause Tracing
- Systematic Debugging
- RefreshToken
- components.json
- Condition-Based Waiting
- dependencies
- InvariantViolation
- ScheduledNotification
- Root Cause Tracing
- Systematic Debugging
- Course
- Room
- domain/__init__.py
- RefreshToken
- Defense-in-Depth Validation
- Writing Plans
- devDependencies
- Brainstorming
- Department
- Room
- Section
- Defense-in-Depth Validation
- FacultyDesk Agent Contract
- Verification Before Completion
- bulk_import.py
- scripts
- helper.js
- Brainstorming
- PushSubscription
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
- web_push.py
- page.tsx
- Stage 02: Domain model and persistence (OOAD core)
- Graphify Protocol
- Stage 03: Authentication, roles and faculty directory
- Stage 07: Meeting circular scanning, extraction and review queue
- Stage 08: Documentation tasks, priority scoring and alerts
- Code Quality Bar
- Documentation Rule
- Build Loop
- Math First
- playwright_sync_api
- ._transition
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- Stage 06: Reminder engine with exactly-once delivery
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
- eslint.config.mjs
- builder-check-prompt.md
- task-done
- task-start
- ooad-diagrams/SKILL.md
- stage-verify/SKILL.md
- ooad-diagrams/SKILL.md
- frontend/AGENTS.md
- api/__init__.py
- application/__init__.py
- infrastructure/__init__.py
- facultydesk-backend

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 137 edges
2. `Principal` - 71 edges
3. `Clock` - 70 edges
4. `FacultyProfile` - 64 edges
5. `ScheduledNotification` - 62 edges
6. `User` - 55 edges
7. `Event` - 50 edges
8. `Initials` - 40 edges
9. `SqlAlchemyUnitOfWork` - 38 edges
10. `InvariantViolation` - 35 edges

## Surprising Connections (you probably didn't know these)
- `10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix` --references--> `AuthorisationPolicy`  [INFERRED]
  docs/MATHS.md → backend/app/application/security/policy.py
- `Standards you are held to` --references--> `Clock`  [INFERRED]
  .agents/agents/backend-engineer.md → backend/app/core/clock.py
- `Non-negotiables` --references--> `Clock`  [INFERRED]
  AGENTS.md → backend/app/core/clock.py
- `Persistence` --references--> `UnitOfWork`  [INFERRED]
  prompts/02-domain-model.md → backend/app/domain/repositories.py
- `5.1 Initials Value Object Invariant` --references--> `InvariantViolation`  [INFERRED]
  docs/MATHS.md → backend/app/domain/errors.py

## Import Cycles
- None detected.

## Communities (137 total, 33 thin omitted)

### Community 0 - "parsers/__init__.py"
Cohesion: 0.06
Nodes (32): BusyInterval, FreeSlotFinder, merge_busy_intervals(), generate_vcalendar_ics(), CancelEventUseCase, CheckClashesUseCase, CreateEventUseCase, FindFreeSlotsUseCase (+24 more)

### Community 1 - "server.cjs"
Cohesion: 0.07
Nodes (35): get_rate_limiter(), change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest (+27 more)

### Community 2 - "datetime"
Cohesion: 0.08
Nodes (36): OCR and Parsing Engineer, Responsibilities, Rules, ParseTimetableUseCase, split_co_teachers(), tokenize_cell(), CsvTimetableParser, _get_col() (+28 more)

### Community 3 - "main.py"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 4 - "User"
Cohesion: 0.06
Nodes (24): FrozenClock, Circular, test_round_trip_all_aggregates(), test_clock_always_returns_utc_property(), test_frozen_clock_advance_property(), test_frozen_clock_rejects_naive_datetime(), test_circular_state_machine_exhaustive(), test_event_invariants() (+16 more)

### Community 5 - "bulk_import_faculty"
Cohesion: 0.07
Nodes (23): AcademicTermResponse, add_holiday(), bulk_import_faculty(), bulk_import_holidays(), BulkImportResponse, create_faculty(), create_term(), CreateAcademicTermRequest (+15 more)

### Community 6 - "directory.py"
Cohesion: 0.09
Nodes (18): expand_slot_recurrence(), TimetableSlot, TimetableSlotRepository, TimeSlot, timetable_slot_to_domain(), TimetableSlotRepositoryImpl, test_timeslot_half_open_overlap(), test_recurrence_expansion_matching_weekday() (+10 more)

### Community 7 - "clash_detector.py"
Cohesion: 0.09
Nodes (27): Interval, intervals_overlap(), pairwise_clashes(), SweepLineClashDetector, test_adjacent_intervals_no_clash(), test_sweep_line_clash_detection_matches_pairwise_property(), test_worked_example_from_maths_md(), 10.1 Token Lifetimes, Rotation, and Family Reuse Detection (+19 more)

### Community 8 - "db/repositories.py"
Cohesion: 0.11
Nodes (10): AuditLogRepository, CircularRepository, CourseRepository, EventRepository, NotificationRepository, PushSubscriptionRepository, RefreshTokenRepository, ReminderRuleRepository (+2 more)

### Community 9 - "get_settings"
Cohesion: 0.09
Nodes (14): CalendarEventResponse, cancel_calendar_event(), check_event_clashes(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots() (+6 more)

### Community 10 - "Test-Driven Development (TDD)"
Cohesion: 0.21
Nodes (13): CreateFacultyUseCase, DeactivateFacultyUseCase, ManageTermsUseCase, UpdateFacultyUseCase, AuthorisationPolicy, Principal, ConflictError, ForbiddenError (+5 more)

### Community 11 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 12 - "UnitOfWork"
Cohesion: 0.17
Nodes (9): ReminderDispatcher, User, NotificationPayload, Notifier, EmailNotifier, CompositeNotifier, ConcurrentMockNotifier, test_concurrency_dispatcher_skip_locked() (+1 more)

### Community 14 - "UnitOfWork"
Cohesion: 0.11
Nodes (3): get_ics_feed(), Clock, UnitOfWork

### Community 15 - "package.json"
Cohesion: 0.15
Nodes (12): Base, AuditLogModel, CircularModel, EventAttendeeModel, EventModel, FacultyProfileModel, TimetableSlotModel, audit_log_to_domain() (+4 more)

### Community 16 - "Principal"
Cohesion: 0.09
Nodes (6): configure_logging(), RequestIdMiddleware, domain_exception_handler(), healthz(), lifespan(), readyz()

### Community 17 - "package.json"
Cohesion: 0.08
Nodes (25): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+17 more)

### Community 18 - "reminders.py"
Cohesion: 0.16
Nodes (12): DeletePushSubscriptionRequest, get_quiet_hours(), get_reminder_rules(), get_upcoming_notifications(), PushSubscriptionRequest, QuietHoursResponse, ReminderRuleResponse, ScheduledNotificationResponse (+4 more)

### Community 19 - "Executing Plans"
Cohesion: 0.15
Nodes (8): upload_timetable(), ConfirmTimetableUseCase, UploadTimetableUseCase, SystemClock, MinioStorageService, test_timetable_upload_parse_and_confirm_pipeline(), Stage 01: Foundation, environment, Graphify, trusted skills, Tasks

### Community 20 - "reminders/use_cases.py"
Cohesion: 0.12
Nodes (6): GetUpcomingNotificationsUseCase, GetUserQuietHoursUseCase, GetUserReminderRulesUseCase, UpdateReminderRuleUseCase, UpdateUserQuietHoursUseCase, ReminderRule

### Community 21 - "Executing Plans"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 22 - "deps.py"
Cohesion: 0.16
Nodes (8): AcademicTerm, Holiday, AcademicTermRepository, AcademicTermModel, HolidayModel, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 23 - "Visual Companion Guide"
Cohesion: 0.16
Nodes (4): FacultyProfile, FacultyProfileRepository, faculty_profile_to_domain(), FacultyProfileRepositoryImpl

### Community 24 - "Creation Log: Systematic Debugging Skill"
Cohesion: 0.12
Nodes (6): upgrade(), upgrade(), upgrade(), upgrade(), get_db(), cleanup_db_connections()

### Community 25 - "compilerOptions"
Cohesion: 0.24
Nodes (10): get_clock(), get_current_principal(), get_storage(), get_uow(), require_admin(), require_hod_or_admin(), FacultyDeskError, InvalidTransition (+2 more)

### Community 26 - "timetable.py"
Cohesion: 0.15
Nodes (8): SqlAlchemyUnitOfWork, main(), seed_database(), _build_dispatcher(), dispatch_due_notifications(), recover_stale_sending_notifications(), _run_dispatch(), _run_recover()

### Community 27 - "Visual Companion Guide"
Cohesion: 0.10
Nodes (19): Browser Events Format, Cards (visual designs), Cleaning Up, CSS Classes Available, Design Tips, File Naming, How It Works, Mock elements (wireframe building blocks) (+11 more)

### Community 28 - "4. OOAD diagrams"
Cohesion: 0.10
Nodes (19): Bulletproofing Elements, Creation Log: Systematic Debugging Skill, Enhancement 1: TDD Reference, Extraction Decisions, Final Outcome, Initial Version, Iterations, Key Insight (+11 more)

### Community 29 - "Root Cause Tracing"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 30 - "Systematic Debugging"
Cohesion: 0.19
Nodes (3): ScheduledNotificationModel, notification_to_domain(), NotificationRepositoryImpl

### Community 31 - "RefreshToken"
Cohesion: 0.29
Nodes (9): adjust_for_quiet_hours(), compute_fire_time(), compute_idempotency_key(), NotificationChannel, QuietHours, test_quiet_hours_midnight_crossing(), test_fire_time_computation(), test_idempotency_key_deterministic() (+1 more)

### Community 32 - "components.json"
Cohesion: 0.21
Nodes (6): Department, DepartmentRepository, DepartmentModel, department_to_domain(), DepartmentRepositoryImpl, Stage 02: Domain model and persistence (OOAD core)

### Community 33 - "Condition-Based Waiting"
Cohesion: 0.14
Nodes (3): TimetableUploadModel, timetable_upload_to_domain(), TimetableUploadRepositoryImpl

### Community 34 - "dependencies"
Cohesion: 0.11
Nodes (17): 1. Problem and users, 3. Architecture, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine, 4.4 ScheduledNotification State Machine, 4.5 Entity-Relationship (ER) Diagram, 4.6 Authentication & Token Rotation Sequence (+9 more)

### Community 35 - "InvariantViolation"
Cohesion: 0.12
Nodes (3): InvariantViolation, 1.2 Half-Open Interval Invariant and Overlap Arithmetic, 1. Time and Recurrence

### Community 37 - "Root Cause Tracing"
Cohesion: 0.12
Nodes (15): 1. Observe the Symptom, 2. Find Immediate Cause, 3. Ask: What Called This?, 4. Keep Tracing Up, 5. Find Original Trigger, Adding Stack Traces, Finding Which Test Causes Pollution, Key Principle (+7 more)

### Community 38 - "Systematic Debugging"
Cohesion: 0.12
Nodes (15): Common Rationalizations, Overview, Phase 1: Root Cause Investigation, Phase 2: Pattern Analysis, Phase 3: Hypothesis and Testing, Phase 4: Implementation, Quick Reference, Red Flags - STOP and Follow Process (+7 more)

### Community 39 - "Course"
Cohesion: 0.12
Nodes (15): aliases, components, hooks, lib, ui, utils, rsc, $schema (+7 more)

### Community 40 - "Room"
Cohesion: 0.15
Nodes (12): Common Mistakes, Condition-Based Waiting, Core Pattern, waitForEvent(), waitForEventCount(), waitForEventMatch(), Implementation, Overview (+4 more)

### Community 41 - "domain/__init__.py"
Cohesion: 0.42
Nodes (8): AttendeeResponse, CircularStatus, EventKind, EventSource, NotificationStatus, TaskStatus, TimetableUploadStatus, event_to_domain()

### Community 42 - "RefreshToken"
Cohesion: 0.18
Nodes (4): RefreshToken, RefreshTokenModel, refresh_token_to_domain(), RefreshTokenRepositoryImpl

### Community 43 - "Defense-in-Depth Validation"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 44 - "Writing Plans"
Cohesion: 0.18
Nodes (7): confirm_timetable(), ConfirmTimetableResponse, get_faculty_slots(), get_timetable_upload(), TimetableSlotResponse, TimetableUploadDetailResponse, UploadTimetableResponse

### Community 45 - "devDependencies"
Cohesion: 0.22
Nodes (4): Course, CourseModel, course_to_domain(), CourseRepositoryImpl

### Community 46 - "Brainstorming"
Cohesion: 0.26
Nodes (5): Task, TaskRepository, TaskModel, task_to_domain(), TaskRepositoryImpl

### Community 47 - "Department"
Cohesion: 0.26
Nodes (3): get_storage_service(), process_timetable_upload(), _run_parse()

### Community 48 - "Room"
Cohesion: 0.29
Nodes (5): Room, RoomRepository, RoomModel, room_to_domain(), RoomRepositoryImpl

### Community 49 - "Section"
Cohesion: 0.29
Nodes (5): Section, SectionRepository, SectionModel, section_to_domain(), SectionRepositoryImpl

### Community 50 - "Defense-in-Depth Validation"
Cohesion: 0.17
Nodes (11): Applying the Pattern, Defense-in-Depth Validation, Example from Session, Key Insight, Layer 1: Entry Point Validation, Layer 2: Business Logic Validation, Layer 3: Environment Guards, Layer 4: Debug Instrumentation (+3 more)

### Community 51 - "FacultyDesk Agent Contract"
Cohesion: 0.17
Nodes (11): Execution Handoff, File Structure, Overview, Plan Document Header, Scope Check, Self-Review, Step Granularity, Task Right-Sizing (+3 more)

### Community 52 - "Verification Before Completion"
Cohesion: 0.23
Nodes (6): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_settings(), Settings

### Community 53 - "bulk_import.py"
Cohesion: 0.27
Nodes (4): BulkImportFacultyUseCase, BulkImportReport, RowImportResult, test_bulk_import_from_sample_csv()

### Community 54 - "scripts"
Cohesion: 0.27
Nodes (4): materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation(), ping()

### Community 55 - "helper.js"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, eslint-config-next, openapi-typescript, prettier, prettier-plugin-tailwindcss, tailwindcss, @tailwindcss/turbopack (+4 more)

### Community 56 - "Brainstorming"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 57 - "PushSubscription"
Cohesion: 0.25
Nodes (4): PushSubscriptionResponse, register_push_subscription(), RegisterPushSubscriptionUseCase, PushSubscription

### Community 58 - "layout.tsx"
Cohesion: 0.47
Nodes (10): DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged, TimetableConfirmed, Domain (backend/app/domain) (+2 more)

### Community 59 - "Web Application Testing"
Cohesion: 0.20
Nodes (9): Architecture law, Communication style, Definition of done for every stage, FacultyDesk Agent Contract, Fixed tech stack (do not substitute), How work is organised, Non-negotiables, Product in one paragraph (+1 more)

### Community 60 - "bulk_import.py"
Cohesion: 0.20
Nodes (9): Common Failures, Key Patterns, Overview, Rationalization Prevention, Red Flags - STOP, The Gate Function, The Iron Law, Verification Before Completion (+1 more)

### Community 62 - "page.tsx"
Cohesion: 0.20
Nodes (10): scripts, build, dev, fmt, format:check, generate:api, lint, start (+2 more)

### Community 63 - "Stage 02: Domain model and persistence (OOAD core)"
Cohesion: 0.42
Nodes (7): connect(), nextReconnectDelay(), reloadAfterRecovery(), sessionKey(), setStatus(), showTombstone(), websocketUrl()

### Community 65 - "Graphify Protocol"
Cohesion: 0.33
Nodes (3): ReminderRuleModel, reminder_rule_to_domain(), ReminderRuleRepositoryImpl

### Community 66 - "Trusted External Skills"
Cohesion: 0.22
Nodes (5): nextConfig, geistMono, geistSans, metadata, next

### Community 67 - "stop-server.sh"
Cohesion: 0.25
Nodes (7): Best Practices, Common Pitfall, Decision Tree: Choosing Your Approach, Example: Using with_server.py, Reconnaissance-Then-Action Pattern, Reference Files, Web Application Testing

### Community 68 - "Frontend Design"
Cohesion: 0.39
Nodes (3): PushSubscriptionModel, push_subscription_to_domain(), PushSubscriptionRepositoryImpl

### Community 70 - "page.tsx"
Cohesion: 0.39
Nodes (5): fetchInitialReadiness(), Home(), ReadinessData, ReadinessView(), react

### Community 71 - "Stage 02: Domain model and persistence (OOAD core)"
Cohesion: 0.25
Nodes (7): Acceptance criteria, Diagrams, Goal, Maths to specify first (MATHS.md), Persistence, Stage 02: Domain model and persistence (OOAD core), Tests

### Community 72 - "Graphify Protocol"
Cohesion: 0.29
Nodes (6): During the stage, End of every stage, Graphify Protocol, Install (stage 01 only, verify in every later stage), Start of every stage, Version control

### Community 73 - "Stage 03: Authentication, roles and faculty directory"
Cohesion: 0.29
Nodes (6): 1. obra/superpowers (Jesse Vincent, MIT), 2. anthropics/skills (Anthropic, official), 3. safishamsi/graphify (Graphify), Local project skills (already in `.agents/skills/`), Trusted External Skills, Vetting rule for anything else

### Community 74 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.52
Nodes (6): command_has_server_id(), command_line_for_pid(), is_brainstorm_server(), mark_stopped(), read_expected_server_id(), stop-server.sh script

### Community 75 - "Stage 08: Documentation tasks, priority scoring and alerts"
Cohesion: 0.29
Nodes (6): Design principles, Frontend Design, Ground your designs in the subject matter, More on writing in design, Process: plan, review against the brief, build, critique, Restraint and self-critique

### Community 77 - "Documentation Rule"
Cohesion: 0.48
Nodes (3): UserModel, user_to_domain(), UserRepositoryImpl

### Community 78 - "Build Loop"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Maths to specify first, Stage 03: Authentication, roles and faculty directory, Tasks, Tests

### Community 79 - "Math First"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Maths to specify first, Stage 08: Documentation tasks, priority scoring and alerts, Tasks, Tests

### Community 80 - "playwright_sync_api"
Cohesion: 0.33
Nodes (5): Code Quality Bar, Forbidden patterns (slop detector), Python, Review before you finish, TypeScript

### Community 81 - "._transition"
Cohesion: 0.33
Nodes (5): docs/DECISIONS.md (what was done and why), docs/MATHS.md (how the logic is proven), docs/PROJECT.md (what the system is), Documentation Rule, Writing style for all three

### Community 82 - "Stage 05: Calendar core, recurrence, clash detection, ICS feed"
Cohesion: 0.33
Nodes (5): Build Loop, Finish, Loop, progress.json shape, Stop conditions

### Community 83 - "Stage 06: Reminder engine with exactly-once delivery"
Cohesion: 0.33
Nodes (5): Math First, Step 1: Specify, Step 2: Test, Step 3: Implement, Step 4: Prove

### Community 85 - "Start here"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 05: Calendar core, recurrence, clash detection, ICS feed, Tests

### Community 86 - "Architect"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 06: Reminder engine with exactly-once delivery, Tests

### Community 87 - "Backend Engineer"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 10: Security, reliability and observability hardening, Tasks

### Community 88 - "Frontend Engineer"
Cohesion: 0.33
Nodes (5): Before you start (one time, about 10 minutes), Run, Start here, What this folder is, What to show your guide

### Community 89 - "Math Verifier"
Cohesion: 0.40
Nodes (4): Architect, Design checks, Output for every design task, Responsibilities

### Community 90 - "Orchestrator"
Cohesion: 0.40
Nodes (4): Backend Engineer, Responsibilities, Standards you are held to, Working method

### Community 91 - "Reviewer"
Cohesion: 0.40
Nodes (4): Design bar, Frontend Engineer, Responsibilities, Rules

### Community 92 - "Graphify Protocol"
Cohesion: 0.40
Nodes (4): After implementation, Before implementation, Core specifications this project needs (owner of each section), Math Verifier

### Community 93 - "Slop Review"
Cohesion: 0.40
Nodes (4): Orchestrator, Ownership table, Responsibilities, You never

### Community 94 - "Pressure Test 1: Emergency Production Fix"
Cohesion: 0.40
Nodes (4): Output, Procedure, Reviewer, Things you always look for

### Community 95 - "Pressure Test 2: Sunk Cost + Exhaustion"
Cohesion: 0.40
Nodes (4): Before writing a helper or new class, End of stage, Graphify Protocol, Start of stage

### Community 96 - "Pressure Test 3: Authority + Social Pressure"
Cohesion: 0.40
Nodes (4): Judgement checks, Mechanical checks (run them, paste results), Output, Slop Review

### Community 97 - "Stage 09: Frontend installable web app"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 1: Emergency Production Fix, Scenario, Your Options

### Community 98 - "Stage 11: Production deployment, CI and end-to-end smoke test"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 2: Sunk Cost + Exhaustion, Scenario, Your Options

### Community 99 - "Stage 12: OOAD diagram pack and final audit"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 3: Authority + Social Pressure, Scenario, Your Options

### Community 101 - "Docs Writer"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 09: Frontend installable web app, Tasks

### Community 102 - "OOAD Diagrammer"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 11: Production deployment, CI and end-to-end smoke test, Tasks

### Community 103 - "Security and Safety"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 12: OOAD diagram pack and final audit, Tasks

### Community 104 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): DevOps Engineer, Responsibilities, Rules

### Community 105 - "frontend/README.md"
Cohesion: 0.50
Nodes (3): Docs Writer, Responsibilities, Style

### Community 106 - "Kickoff prompt (paste this into the Antigravity agent)"
Cohesion: 0.50
Nodes (3): Diagram set (kept in docs/PROJECT.md, exported to docs/diagrams/), OOAD Diagrammer, Rules

### Community 107 - "start-server.sh"
Cohesion: 0.50
Nodes (3): Agent safety while building, Application security, Security and Safety

### Community 108 - "eslint.config.mjs"
Cohesion: 0.50
Nodes (3): eslintConfig, eslint, eslint-config-next

### Community 109 - "builder-check-prompt.md"
Cohesion: 0.50
Nodes (3): Deploy on Vercel, Getting Started, Learn More

### Community 110 - "task-done"
Cohesion: 0.50
Nodes (3): Kickoff prompt (paste this into the Antigravity agent), Resuming in a new conversation, Running a single stage manually

### Community 111 - "task-start"
Cohesion: 0.50
Nodes (3): Acceptance criteria, Goal, Stage 01: Foundation, environment, Graphify, trusted skills

## Knowledge Gaps
- **23 isolated node(s):** `facultydesk-backend`, `clsx`, `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 733 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `parsers/__init__.py`, `server.cjs`, `datetime`, `bulk_import_faculty`, `db/repositories.py`, `get_settings`, `Test-Driven Development (TDD)`, `UnitOfWork`, `reminders.py`, `Executing Plans`, `reminders/use_cases.py`, `compilerOptions`, `timetable.py`, `RefreshToken`, `components.json`, `ScheduledNotification`, `domain/__init__.py`, `Writing Plans`, `bulk_import.py`, `PushSubscription`, `layout.tsx`, `web_push.py`, `Stage 02: Domain model and persistence (OOAD core)`, `Code Quality Bar`, `DevOps Engineer`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 41 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 41 INFERRED edges - model-reasoned connections that need verification._
- **What connects `facultydesk-backend`, `clsx`, `@fullcalendar/core` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `parsers/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05948399426660296 - nodes in this community are weakly interconnected._
- **Why does `Clock` connect `UnitOfWork` to `parsers/__init__.py`, `server.cjs`, `User`, `bulk_import_faculty`, `get_settings`, `Test-Driven Development (TDD)`, `Writing Plans`, `UnitOfWork`, `Executing Plans`, `bulk_import.py`, `compilerOptions`, `Orchestrator`, `Web Application Testing`, `RefreshToken`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `Principal` (e.g. with `require_admin()` and `require_hod_or_admin()`) actually correct?**
  _`Principal` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.07205452775073028 - nodes in this community are weakly interconnected._