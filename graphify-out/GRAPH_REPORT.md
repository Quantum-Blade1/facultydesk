# Graph Report - facultydesk  (2026-10-28)

## Corpus Check
- 209 files · ~173,781 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: (none) 10, .csv 2, .example 1)

## Summary
- 2121 nodes · 6026 edges · 136 communities (106 shown, 30 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 969 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ffbe20b6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- server.cjs
- Department
- test_calendar_full_pipeline
- SqlAlchemyUnitOfWork
- UUID
- FacultyProfile
- Initials
- db/repositories.py
- sqlalchemy
- timetable.py
- Test-Driven Development (TDD)
- calendar.py
- auth.py
- logging.py
- UnitOfWork
- Principal
- package.json
- reminders.py
- Test-Driven Development (TDD)
- reminders.py
- Executing Plans
- deps.py
- Visual Companion Guide
- Circular
- TimetableSlot
- ReminderRule
- calendar/use_cases.py
- extractor.py
- tasks.py
- Systematic Debugging
- RefreshToken
- components.json
- domain/__init__.py
- ScheduledNotification
- AsyncSession
- ScheduledNotification
- Root Cause Tracing
- reminder_tasks.py
- tasks/use_cases.py
- InvariantViolation
- domain/__init__.py
- Root Cause Tracing
- Defense-in-Depth Validation
- PushSubscription
- devDependencies
- Brainstorming
- Department
- circulars/use_cases.py
- Section
- zoneinfo
- FacultyDesk Agent Contract
- Task
- Course
- scripts
- helper.js
- Brainstorming
- Section
- Circular
- Web Application Testing
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- NotificationRepositoryImpl
- reminders/use_cases.py
- RedisSlidingWindowRateLimiter
- with_server.py
- FacultyDesk Agent Contract
- Trusted External Skills
- stop-server.sh
- helper.js
- compute_priority_score
- Stage 02: Domain model and persistence (OOAD core)
- Graphify Protocol
- Stage 03: Authentication, roles and faculty directory
- Stage 07: Meeting circular scanning, extraction and review queue
- Stage 08: Documentation tasks, priority scoring and alerts
- Code Quality Bar
- stop-server.sh
- Build Loop
- Stage 06: Reminder engine with exactly-once delivery
- TaskTemplateRepository
- ._transition
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- Stage 06: Reminder engine with exactly-once delivery
- Stage 10: Security, reliability and observability hardening
- Build Loop
- Math First
- Frontend Engineer
- Math Verifier
- Orchestrator
- confirm_timetable
- Graphify Protocol
- Slop Review
- Pressure Test 1: Emergency Production Fix
- Pressure Test 2: Sunk Cost + Exhaustion
- Pressure Test 3: Authority + Social Pressure
- Stage 09: Frontend installable web app
- Stage 11: Production deployment, CI and end-to-end smoke test
- Stage 12: OOAD diagram pack and final audit
- Pressure Test 3: Authority + Social Pressure
- Docs Writer
- OOAD Diagrammer
- Security and Safety
- eslint.config.mjs
- frontend/README.md
- Kickoff prompt (paste this into the Antigravity agent)
- start-server.sh
- delete_task
- builder-check-prompt.md
- task-done
- Kickoff prompt (paste this into the Antigravity agent)
- ooad-diagrams/SKILL.md
- AuditLogRepository
- test-academic.md
- api/__init__.py
- application/__init__.py
- find-polluter.sh
- infrastructure/__init__.py
- seed/__init__.py
- DomainError
- main.py
- facultydesk-backend
- FacultyProfileRepository

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 177 edges
2. `Clock` - 108 edges
3. `Principal` - 92 edges
4. `FacultyProfile` - 77 edges
5. `ScheduledNotification` - 75 edges
6. `Event` - 69 edges
7. `User` - 64 edges
8. `NotFoundError` - 56 edges
9. `InvariantViolation` - 51 edges
10. `Initials` - 49 edges

## Surprising Connections (you probably didn't know these)
- `10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix` --references--> `AuthorisationPolicy`  [INFERRED]
  docs/MATHS.md → backend/app/application/security/policy.py
- `Standards you are held to` --references--> `Clock`  [INFERRED]
  .agents/agents/backend-engineer.md → backend/app/core/clock.py
- `Non-negotiables` --references--> `Clock`  [INFERRED]
  AGENTS.md → backend/app/core/clock.py
- `5.4 Merged-Cell Period Expansion` --references--> `TimetableSlot`  [INFERRED]
  docs/MATHS.md → backend/app/domain/entities.py
- `5.1 Initials Value Object Invariant` --references--> `InvariantViolation`  [INFERRED]
  docs/MATHS.md → backend/app/domain/errors.py

## Import Cycles
- None detected.

## Communities (136 total, 30 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.10
Nodes (32): OCR and Parsing Engineer, Responsibilities, Rules, split_co_teachers(), tokenize_cell(), CsvTimetableParser, _get_col(), _parse_clock_time() (+24 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 2 - "Department"
Cohesion: 0.20
Nodes (3): Department, department_to_domain(), DepartmentRepositoryImpl

### Community 3 - "test_calendar_full_pipeline"
Cohesion: 0.17
Nodes (12): cancel_calendar_event(), CancelEventUseCase, CheckClashesUseCase, MaterialiseTimetableEventsUseCase, RotateIcsTokenUseCase, UpdateEventUseCase, ReminderPlanner, ClashDetectedError (+4 more)

### Community 4 - "SqlAlchemyUnitOfWork"
Cohesion: 0.09
Nodes (21): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), SystemClock, get_settings(), Settings, SqlAlchemyUnitOfWork (+13 more)

### Community 6 - "FacultyProfile"
Cohesion: 0.10
Nodes (17): ReminderDispatcher, FacultyProfile, User, CircularRepository, DepartmentRepository, UserRepository, NotificationChannel, NotificationPayload (+9 more)

### Community 7 - "Initials"
Cohesion: 0.28
Nodes (5): BulkImportFacultyUseCase, BulkImportReport, RowImportResult, Initials, test_bulk_import_from_sample_csv()

### Community 8 - "db/repositories.py"
Cohesion: 0.14
Nodes (25): Base, get_db(), AcademicTermModel, AuditLogModel, CircularModel, CourseModel, DepartmentModel, EventAttendeeModel (+17 more)

### Community 9 - "sqlalchemy"
Cohesion: 0.10
Nodes (14): upgrade(), upgrade(), upgrade(), upgrade(), upgrade(), Interval, intervals_overlap(), pairwise_clashes() (+6 more)

### Community 10 - "timetable.py"
Cohesion: 0.15
Nodes (8): get_storage(), upload_timetable(), ConfirmTimetableUseCase, ParseTimetableUseCase, UploadTimetableUseCase, get_storage_service(), MinioStorageService, test_timetable_upload_parse_and_confirm_pipeline()

### Community 11 - "Test-Driven Development (TDD)"
Cohesion: 0.19
Nodes (16): CreateFacultyUseCase, DeactivateFacultyUseCase, ManageTermsUseCase, UpdateFacultyUseCase, AuthorisationPolicy, Principal, ConflictError, FacultyDeskError (+8 more)

### Community 12 - "calendar.py"
Cohesion: 0.11
Nodes (15): CalendarEventResponse, check_event_clashes(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots(), FindFreeSlotsRequest (+7 more)

### Community 13 - "auth.py"
Cohesion: 0.08
Nodes (28): get_clock(), get_current_principal(), get_uow(), require_admin(), require_hod_or_admin(), AcademicTermResponse, add_holiday(), bulk_import_faculty() (+20 more)

### Community 14 - "logging.py"
Cohesion: 0.16
Nodes (3): configure_logging(), RequestIdMiddleware, lifespan()

### Community 16 - "Principal"
Cohesion: 0.06
Nodes (31): 10.1 Token Lifetimes, Rotation, and Family Reuse Detection, 10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix, 10.3 Sliding Window Log Rate Limiting, 10. Security Limits, 1.2 Half-Open Interval Invariant and Overlap Arithmetic, 1. Time and Recurrence, 2.1 Half-Open Overlap Predicate, 2.3 Multi-Attendee Common Free-Slot Finder (+23 more)

### Community 17 - "package.json"
Cohesion: 0.15
Nodes (16): ChangePasswordUseCase, LoginResult, LoginUseCase, LogoutUseCase, RefreshResult, RefreshTokenUseCase, UnauthorizedError, create_access_token() (+8 more)

### Community 18 - "reminders.py"
Cohesion: 0.13
Nodes (5): EventRepositoryImpl, faculty_profile_to_domain(), FacultyProfileRepositoryImpl, timetable_slot_to_domain(), TimetableSlotRepositoryImpl

### Community 19 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 20 - "reminders.py"
Cohesion: 0.11
Nodes (15): delete_push_subscription(), DeletePushSubscriptionRequest, get_quiet_hours(), get_reminder_rules(), get_upcoming_notifications(), PushSubscriptionRequest, PushSubscriptionResponse, QuietHoursResponse (+7 more)

### Community 21 - "Executing Plans"
Cohesion: 0.18
Nodes (14): change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest, LoginResponse (+6 more)

### Community 22 - "deps.py"
Cohesion: 0.08
Nodes (25): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+17 more)

### Community 23 - "Visual Companion Guide"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 24 - "Circular"
Cohesion: 0.11
Nodes (14): CircularDetailResponse, CircularUploadResponse, confirm_circular(), ConfirmCircularRequest, ConfirmCircularResponse, get_circular(), list_review_queue(), reject_circular() (+6 more)

### Community 25 - "TimetableSlot"
Cohesion: 0.28
Nodes (8): expand_slot_recurrence(), TimetableSlot, TimeSlot, test_timeslot_half_open_overlap(), test_recurrence_expansion_matching_weekday(), test_recurrence_expansion_skips_holidays(), test_recurrence_expansion_utc_roundtrip(), 1.4 Recurrence Expansion and Rolling 21-Day Materialisation Window

### Community 26 - "ReminderRule"
Cohesion: 0.20
Nodes (4): ReminderRule, ReminderRuleRepository, reminder_rule_to_domain(), ReminderRuleRepositoryImpl

### Community 27 - "calendar/use_cases.py"
Cohesion: 0.32
Nodes (7): generate_vcalendar_ics(), EventKind, EventSource, test_ics_export_stable_uids(), test_ics_export_valid_rfc5545(), test_duplicate_predicate_worked_example(), 2.4 RFC 5545 ICS Feed Specification

### Community 28 - "extractor.py"
Cohesion: 0.06
Nodes (38): detect_probable_duplicate(), normalize_title(), compute_length_weighted_confidence(), OcrEngine, OcrResult, WordBox, CircularExtractor, ExtractedAttendee (+30 more)

### Community 29 - "tasks.py"
Cohesion: 0.12
Nodes (18): assign_task(), AssignmentProgressResponse, AssignTaskRequest, complete_task(), create_task(), CreateTaskRequest, ensure_utc(), FacultyOverdueSummaryResponse (+10 more)

### Community 30 - "Systematic Debugging"
Cohesion: 0.10
Nodes (19): Browser Events Format, Cards (visual designs), Cleaning Up, CSS Classes Available, Design Tips, File Naming, How It Works, Mock elements (wireframe building blocks) (+11 more)

### Community 31 - "RefreshToken"
Cohesion: 0.10
Nodes (19): Bulletproofing Elements, Creation Log: Systematic Debugging Skill, Enhancement 1: TDD Reference, Extraction Decisions, Final Outcome, Initial Version, Iterations, Key Insight (+11 more)

### Community 32 - "components.json"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 33 - "domain/__init__.py"
Cohesion: 0.19
Nodes (18): Event, EventAttendee, DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged (+10 more)

### Community 34 - "ScheduledNotification"
Cohesion: 0.11
Nodes (5): ScheduledNotification, NotificationRepository, NotificationStatus, notification_to_domain(), NotificationRepositoryImpl

### Community 36 - "ScheduledNotification"
Cohesion: 0.10
Nodes (20): 1. Problem and users, 3. Architecture, 4.10 Reminder Dispatch and Exactly-Once Delivery Sequence, 4.11 Meeting Circular Scanning, Extraction, and Review Sequence, 4.11 Task Assignment, Alert Lifecycle and Escalation Sequence, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine (+12 more)

### Community 37 - "Root Cause Tracing"
Cohesion: 0.18
Nodes (11): adjust_for_quiet_hours(), compute_backoff_delay(), compute_fire_time(), compute_idempotency_key(), GetUserQuietHoursUseCase, QuietHours, test_quiet_hours_midnight_crossing(), test_backoff_bounds() (+3 more)

### Community 38 - "reminder_tasks.py"
Cohesion: 0.19
Nodes (9): _build_dispatcher(), dispatch_due_notifications(), recover_stale_sending_notifications(), _run_dispatch(), _run_recover(), FacultyDesk Decisions, Stage 00: Agent setup, Stage 01: Foundation, environment, Graphify, trusted skills (+1 more)

### Community 39 - "tasks/use_cases.py"
Cohesion: 0.13
Nodes (22): compute_completion_rate(), AssignmentProgress, AssignTaskUseCase, CompleteTaskUseCase, CreateTaskUseCase, FacultyOverdueSummary, GetHodDashboardUseCase, HodDashboardData (+14 more)

### Community 40 - "InvariantViolation"
Cohesion: 0.09
Nodes (7): AcademicTerm, Holiday, InvariantViolation, AcademicTermRepository, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 41 - "domain/__init__.py"
Cohesion: 0.31
Nodes (6): test_event_invariants(), test_initials_invalid_property(), test_initials_valid_property(), test_notification_state_machine_exhaustive(), test_task_invariants(), test_timeslot_invariants()

### Community 42 - "Root Cause Tracing"
Cohesion: 0.12
Nodes (15): 1. Observe the Symptom, 2. Find Immediate Cause, 3. Ask: What Called This?, 4. Keep Tracing Up, 5. Find Original Trigger, Adding Stack Traces, Finding Which Test Causes Pollution, Key Principle (+7 more)

### Community 43 - "Defense-in-Depth Validation"
Cohesion: 0.12
Nodes (15): Common Rationalizations, Overview, Phase 1: Root Cause Investigation, Phase 2: Pattern Analysis, Phase 3: Hypothesis and Testing, Phase 4: Implementation, Quick Reference, Red Flags - STOP and Follow Process (+7 more)

### Community 44 - "PushSubscription"
Cohesion: 0.13
Nodes (4): PushSubscription, PushSubscriptionRepository, push_subscription_to_domain(), PushSubscriptionRepositoryImpl

### Community 45 - "devDependencies"
Cohesion: 0.12
Nodes (15): aliases, components, hooks, lib, ui, utils, rsc, $schema (+7 more)

### Community 46 - "Brainstorming"
Cohesion: 0.15
Nodes (12): Common Mistakes, Condition-Based Waiting, Core Pattern, waitForEvent(), waitForEventCount(), waitForEventMatch(), Implementation, Overview (+4 more)

### Community 47 - "Department"
Cohesion: 0.18
Nodes (9): FrozenClock, test_clock_always_returns_utc_property(), test_frozen_clock_advance_property(), test_frozen_clock_rejects_naive_datetime(), 1.1 Canonical Time Representation and Clock Invariant, Acceptance criteria, Goal, Stage 01: Foundation, environment, Graphify, trusted skills (+1 more)

### Community 48 - "circulars/use_cases.py"
Cohesion: 0.17
Nodes (7): CreateEventUseCase, GetCalendarEventsUseCase, ConfirmCircularUseCase, ProcessCircularUseCase, InMemoryStorageService, sample_dir(), test_circular_full_pipeline_with_samples()

### Community 49 - "Section"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 50 - "zoneinfo"
Cohesion: 0.24
Nodes (6): BusyInterval, FreeSlotFinder, merge_busy_intervals(), FindFreeSlotsUseCase, test_free_slots_never_intersect_busy_property(), test_free_slots_worked_example()

### Community 51 - "FacultyDesk Agent Contract"
Cohesion: 0.14
Nodes (4): RefreshToken, RefreshTokenRepository, refresh_token_to_domain(), RefreshTokenRepositoryImpl

### Community 52 - "Task"
Cohesion: 0.16
Nodes (5): Task, TaskRepository, TaskStatus, task_to_domain(), TaskRepositoryImpl

### Community 53 - "Course"
Cohesion: 0.30
Nodes (4): Course, CourseRepository, course_to_domain(), CourseRepositoryImpl

### Community 54 - "scripts"
Cohesion: 0.30
Nodes (4): Room, RoomRepository, room_to_domain(), RoomRepositoryImpl

### Community 55 - "helper.js"
Cohesion: 0.17
Nodes (11): Applying the Pattern, Defense-in-Depth Validation, Example from Session, Key Insight, Layer 1: Entry Point Validation, Layer 2: Business Logic Validation, Layer 3: Environment Guards, Layer 4: Debug Instrumentation (+3 more)

### Community 56 - "Brainstorming"
Cohesion: 0.17
Nodes (11): Execution Handoff, File Structure, Overview, Plan Document Header, Scope Check, Self-Review, Step Granularity, Task Right-Sizing (+3 more)

### Community 57 - "Section"
Cohesion: 0.30
Nodes (4): Section, SectionRepository, section_to_domain(), SectionRepositoryImpl

### Community 58 - "Circular"
Cohesion: 0.06
Nodes (24): Circular, TimetableUpload, InvalidTransition, TimetableUploadRepository, timetable_upload_to_domain(), TimetableUploadRepositoryImpl, test_round_trip_all_aggregates(), test_circular_state_machine_exhaustive() (+16 more)

### Community 59 - "Web Application Testing"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, eslint-config-next, openapi-typescript, prettier, prettier-plugin-tailwindcss, tailwindcss, @tailwindcss/turbopack (+4 more)

### Community 60 - "Stage 05: Calendar core, recurrence, clash detection, ICS feed"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 05: Calendar core, recurrence, clash detection, ICS feed, Tests

### Community 61 - "NotificationRepositoryImpl"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 62 - "reminders/use_cases.py"
Cohesion: 0.12
Nodes (6): DeletePushSubscriptionUseCase, GetUpcomingNotificationsUseCase, GetUserReminderRulesUseCase, RegisterPushSubscriptionUseCase, UpdateReminderRuleUseCase, UpdateUserQuietHoursUseCase

### Community 63 - "RedisSlidingWindowRateLimiter"
Cohesion: 0.29
Nodes (5): get_rate_limiter(), RateLimitExceededError, get_redis_client(), RedisSlidingWindowRateLimiter, test_sliding_window_rate_limiter()

### Community 65 - "FacultyDesk Agent Contract"
Cohesion: 0.20
Nodes (9): Architecture law, Communication style, Definition of done for every stage, FacultyDesk Agent Contract, Fixed tech stack (do not substitute), How work is organised, Non-negotiables, Product in one paragraph (+1 more)

### Community 66 - "Trusted External Skills"
Cohesion: 0.20
Nodes (9): Common Failures, Key Patterns, Overview, Rationalization Prevention, Red Flags - STOP, The Gate Function, The Iron Law, Verification Before Completion (+1 more)

### Community 67 - "stop-server.sh"
Cohesion: 0.20
Nodes (10): scripts, build, dev, fmt, format:check, generate:api, lint, start (+2 more)

### Community 68 - "helper.js"
Cohesion: 0.42
Nodes (7): connect(), nextReconnectDelay(), reloadAfterRecovery(), sessionKey(), setStatus(), showTombstone(), websocketUrl()

### Community 70 - "compute_priority_score"
Cohesion: 0.21
Nodes (12): compute_lead_alert_times(), compute_overdue_alert_times(), compute_priority_score(), test_completed_task_priority(), test_lead_alert_times(), test_overdue_alert_times(), test_priority_bounds_property_active(), test_priority_bounds_property_overdue() (+4 more)

### Community 71 - "Stage 02: Domain model and persistence (OOAD core)"
Cohesion: 0.22
Nodes (5): nextConfig, geistMono, geistSans, metadata, next

### Community 72 - "Graphify Protocol"
Cohesion: 0.25
Nodes (7): Best Practices, Common Pitfall, Decision Tree: Choosing Your Approach, Example: Using with_server.py, Reconnaissance-Then-Action Pattern, Reference Files, Web Application Testing

### Community 73 - "Stage 03: Authentication, roles and faculty directory"
Cohesion: 0.39
Nodes (5): fetchInitialReadiness(), Home(), ReadinessData, ReadinessView(), react

### Community 74 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.14
Nodes (11): Backend Engineer, Responsibilities, Standards you are held to, Working method, Acceptance criteria, Diagrams, Goal, Maths to specify first (MATHS.md) (+3 more)

### Community 75 - "Stage 08: Documentation tasks, priority scoring and alerts"
Cohesion: 0.29
Nodes (6): During the stage, End of every stage, Graphify Protocol, Install (stage 01 only, verify in every later stage), Start of every stage, Version control

### Community 76 - "Code Quality Bar"
Cohesion: 0.29
Nodes (6): 1. obra/superpowers (Jesse Vincent, MIT), 2. anthropics/skills (Anthropic, official), 3. safishamsi/graphify (Graphify), Local project skills (already in `.agents/skills/`), Trusted External Skills, Vetting rule for anything else

### Community 77 - "stop-server.sh"
Cohesion: 0.52
Nodes (6): command_has_server_id(), command_line_for_pid(), is_brainstorm_server(), mark_stopped(), read_expected_server_id(), stop-server.sh script

### Community 78 - "Build Loop"
Cohesion: 0.29
Nodes (6): Design principles, Frontend Design, Ground your designs in the subject matter, More on writing in design, Process: plan, review against the brief, build, critique, Restraint and self-critique

### Community 79 - "Stage 06: Reminder engine with exactly-once delivery"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 06: Reminder engine with exactly-once delivery, Tests

### Community 80 - "TaskTemplateRepository"
Cohesion: 0.15
Nodes (4): TaskTemplateRepository, TaskTemplateModel, task_template_to_domain(), TaskTemplateRepositoryImpl

### Community 81 - "._transition"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Maths to specify first, Stage 03: Authentication, roles and faculty directory, Tasks, Tests

### Community 82 - "Stage 05: Calendar core, recurrence, clash detection, ICS feed"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Maths to specify first, Stage 08: Documentation tasks, priority scoring and alerts, Tasks, Tests

### Community 83 - "Stage 06: Reminder engine with exactly-once delivery"
Cohesion: 0.33
Nodes (5): Code Quality Bar, Forbidden patterns (slop detector), Python, Review before you finish, TypeScript

### Community 84 - "Stage 10: Security, reliability and observability hardening"
Cohesion: 0.33
Nodes (5): docs/DECISIONS.md (what was done and why), docs/MATHS.md (how the logic is proven), docs/PROJECT.md (what the system is), Documentation Rule, Writing style for all three

### Community 85 - "Build Loop"
Cohesion: 0.33
Nodes (5): Build Loop, Finish, Loop, progress.json shape, Stop conditions

### Community 86 - "Math First"
Cohesion: 0.33
Nodes (5): Math First, Step 1: Specify, Step 2: Test, Step 3: Implement, Step 4: Prove

### Community 88 - "Frontend Engineer"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 10: Security, reliability and observability hardening, Tasks

### Community 89 - "Math Verifier"
Cohesion: 0.33
Nodes (5): Before you start (one time, about 10 minutes), Run, Start here, What this folder is, What to show your guide

### Community 90 - "Orchestrator"
Cohesion: 0.40
Nodes (4): Architect, Design checks, Output for every design task, Responsibilities

### Community 91 - "confirm_timetable"
Cohesion: 0.18
Nodes (7): confirm_timetable(), ConfirmTimetableResponse, get_faculty_slots(), get_timetable_upload(), TimetableSlotResponse, TimetableUploadDetailResponse, UploadTimetableResponse

### Community 92 - "Graphify Protocol"
Cohesion: 0.40
Nodes (4): Design bar, Frontend Engineer, Responsibilities, Rules

### Community 93 - "Slop Review"
Cohesion: 0.40
Nodes (4): After implementation, Before implementation, Core specifications this project needs (owner of each section), Math Verifier

### Community 94 - "Pressure Test 1: Emergency Production Fix"
Cohesion: 0.40
Nodes (4): Orchestrator, Ownership table, Responsibilities, You never

### Community 95 - "Pressure Test 2: Sunk Cost + Exhaustion"
Cohesion: 0.40
Nodes (4): Output, Procedure, Reviewer, Things you always look for

### Community 96 - "Pressure Test 3: Authority + Social Pressure"
Cohesion: 0.40
Nodes (4): Before writing a helper or new class, End of stage, Graphify Protocol, Start of stage

### Community 97 - "Stage 09: Frontend installable web app"
Cohesion: 0.40
Nodes (4): Judgement checks, Mechanical checks (run them, paste results), Output, Slop Review

### Community 98 - "Stage 11: Production deployment, CI and end-to-end smoke test"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 1: Emergency Production Fix, Scenario, Your Options

### Community 99 - "Stage 12: OOAD diagram pack and final audit"
Cohesion: 0.40
Nodes (4): Choose A, B, or C, Pressure Test 2: Sunk Cost + Exhaustion, Scenario, Your Options

### Community 100 - "Pressure Test 3: Authority + Social Pressure"
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

### Community 109 - "builder-check-prompt.md"
Cohesion: 0.50
Nodes (3): eslintConfig, eslint, eslint-config-next

### Community 110 - "task-done"
Cohesion: 0.50
Nodes (3): Deploy on Vercel, Getting Started, Learn More

### Community 111 - "Kickoff prompt (paste this into the Antigravity agent)"
Cohesion: 0.50
Nodes (3): Kickoff prompt (paste this into the Antigravity agent), Resuming in a new conversation, Running a single stage manually

### Community 131 - "main.py"
Cohesion: 0.15
Nodes (3): domain_exception_handler(), healthz(), readyz()

## Knowledge Gaps
- **23 isolated node(s):** `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 782 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `test_calendar_full_pipeline`, `SqlAlchemyUnitOfWork`, `FacultyProfile`, `Initials`, `db/repositories.py`, `timetable.py`, `Test-Driven Development (TDD)`, `calendar.py`, `auth.py`, `package.json`, `reminders.py`, `Executing Plans`, `Circular`, `calendar/use_cases.py`, `extractor.py`, `tasks.py`, `domain/__init__.py`, `Root Cause Tracing`, `tasks/use_cases.py`, `circulars/use_cases.py`, `zoneinfo`, `reminders/use_cases.py`, `Stage 07: Meeting circular scanning, extraction and review queue`, `confirm_timetable`, `delete_task`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Are the 52 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `datetime` be split into smaller, more focused modules?**
  _Cohesion score 0.10056497175141244 - nodes in this community are weakly interconnected._
- **Why does `Clock` connect `UnitOfWork` to `test_calendar_full_pipeline`, `SqlAlchemyUnitOfWork`, `FacultyProfile`, `Initials`, `timetable.py`, `Test-Driven Development (TDD)`, `calendar.py`, `auth.py`, `Principal`, `package.json`, `Executing Plans`, `Circular`, `calendar/use_cases.py`, `tasks.py`, `reminder_tasks.py`, `tasks/use_cases.py`, `Department`, `circulars/use_cases.py`, `FacultyDesk Agent Contract`, `Stage 07: Meeting circular scanning, extraction and review queue`, `confirm_timetable`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `Clock` (e.g. with `Standards you are held to` and `Non-negotiables`) actually correct?**
  _`Clock` has 58 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._