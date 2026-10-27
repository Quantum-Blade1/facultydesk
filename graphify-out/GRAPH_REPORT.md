# Graph Report - facultydesk  (2026-10-27)

## Corpus Check
- 201 files · ~160,672 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: (none) 10, .csv 2, .example 1)

## Summary
- 1968 nodes · 5234 edges · 140 communities (105 shown, 35 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 611 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ce2af82a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- server.cjs
- Department
- main.py
- circular_tasks.py
- domain/__init__.py
- directory.py
- User
- db/repositories.py
- sqlalchemy
- timetable.py
- Test-Driven Development (TDD)
- calendar.py
- auth.py
- main.py
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
- Event
- extractor.py
- get_settings
- Systematic Debugging
- RefreshToken
- components.json
- Condition-Based Waiting
- ScheduledNotification
- AsyncSession
- ScheduledNotification
- Root Cause Tracing
- reminder_tasks.py
- Course
- Room
- domain/__init__.py
- Root Cause Tracing
- Defense-in-Depth Validation
- PushSubscription
- devDependencies
- Brainstorming
- Department
- entities.py
- Section
- zoneinfo
- FacultyDesk Agent Contract
- Verification Before Completion
- Course
- scripts
- helper.js
- Brainstorming
- Section
- TimetableUpload
- Web Application Testing
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- NotificationRepositoryImpl
- Stage 01: Foundation, environment, Graphify, trusted skills
- RedisSlidingWindowRateLimiter
- with_server.py
- FacultyDesk Agent Contract
- Trusted External Skills
- stop-server.sh
- helper.js
- timetable_tasks.py
- Stage 02: Domain model and persistence (OOAD core)
- Graphify Protocol
- Stage 03: Authentication, roles and faculty directory
- Stage 07: Meeting circular scanning, extraction and review queue
- Stage 08: Documentation tasks, priority scoring and alerts
- Code Quality Bar
- stop-server.sh
- Build Loop
- Stage 06: Reminder engine with exactly-once delivery
- test_circular_full_pipeline_with_samples
- ._transition
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- Stage 06: Reminder engine with exactly-once delivery
- Stage 10: Security, reliability and observability hardening
- Build Loop
- Math First
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
- Pressure Test 3: Authority + Social Pressure
- Docs Writer
- OOAD Diagrammer
- Security and Safety
- eslint.config.mjs
- frontend/README.md
- Kickoff prompt (paste this into the Antigravity agent)
- start-server.sh
- TimeSlot
- builder-check-prompt.md
- task-done
- Kickoff prompt (paste this into the Antigravity agent)
- ooad-diagrams/SKILL.md
- 1.3 State Machine Transition Algebras
- test-academic.md
- api/__init__.py
- application/__init__.py
- find-polluter.sh
- infrastructure/__init__.py
- seed/__init__.py
- facultydesk-backend

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 148 edges
2. `Principal` - 79 edges
3. `Clock` - 76 edges
4. `FacultyProfile` - 70 edges
5. `ScheduledNotification` - 61 edges
6. `User` - 56 edges
7. `Event` - 55 edges
8. `Initials` - 44 edges
9. `SqlAlchemyUnitOfWork` - 42 edges
10. `NotFoundError` - 39 edges

## Surprising Connections (you probably didn't know these)
- `2.3 Multi-Attendee Common Free-Slot Finder` --references--> `test_free_slots_never_intersect_busy_property()`  [INFERRED]
  docs/MATHS.md → backend/tests/unit/test_free_slots.py
- `5.1 Initials Value Object Invariant` --references--> `InvariantViolation`  [INFERRED]
  docs/MATHS.md → backend/app/domain/errors.py
- `5.4 Merged-Cell Period Expansion` --references--> `TimetableSlot`  [INFERRED]
  docs/MATHS.md → backend/app/domain/entities.py
- `10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix` --references--> `AuthorisationPolicy`  [INFERRED]
  docs/MATHS.md → backend/app/application/security/policy.py
- `10.3 Sliding Window Log Rate Limiting` --references--> `test_sliding_window_rate_limiter()`  [INFERRED]
  docs/MATHS.md → backend/tests/integration/test_rate_limiter.py

## Import Cycles
- None detected.

## Communities (140 total, 35 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.09
Nodes (37): OCR and Parsing Engineer, Responsibilities, Rules, split_co_teachers(), tokenize_cell(), CsvTimetableParser, _get_col(), _parse_clock_time() (+29 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 2 - "Department"
Cohesion: 0.21
Nodes (5): Department, DepartmentRepository, department_to_domain(), DepartmentRepositoryImpl, Stage 02: Domain model and persistence (OOAD core)

### Community 3 - "main.py"
Cohesion: 0.11
Nodes (14): CancelEventUseCase, CheckClashesUseCase, CreateEventUseCase, FindFreeSlotsUseCase, GenerateIcsFeedUseCase, GetCalendarEventsUseCase, RotateIcsTokenUseCase, UpdateEventUseCase (+6 more)

### Community 4 - "circular_tasks.py"
Cohesion: 0.18
Nodes (7): ProcessCircularUseCase, materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation(), ping(), process_circular_upload(), _run_process_circular()

### Community 5 - "domain/__init__.py"
Cohesion: 0.04
Nodes (12): AcademicTermRepository, AuditLogRepository, CircularRepository, EventRepository, FacultyProfileRepository, NotificationRepository, PushSubscriptionRepository, RefreshTokenRepository (+4 more)

### Community 6 - "directory.py"
Cohesion: 0.13
Nodes (6): ReminderDispatcher, FacultyProfile, NotificationPayload, Notifier, CompositeNotifier, WebPushNotifier

### Community 7 - "User"
Cohesion: 0.13
Nodes (11): User, Initials, SqlAlchemyUnitOfWork, main(), seed_database(), ConcurrentMockNotifier, test_concurrency_dispatcher_skip_locked(), test_planning_idempotency_property() (+3 more)

### Community 8 - "db/repositories.py"
Cohesion: 0.14
Nodes (25): Base, AcademicTermModel, AuditLogModel, CircularModel, CourseModel, DepartmentModel, EventAttendeeModel, EventModel (+17 more)

### Community 9 - "sqlalchemy"
Cohesion: 0.14
Nodes (6): upgrade(), upgrade(), upgrade(), upgrade(), cleanup_db_connections(), sample_dir()

### Community 10 - "timetable.py"
Cohesion: 0.10
Nodes (18): get_storage(), confirm_timetable(), ConfirmTimetableResponse, get_faculty_slots(), get_timetable_upload(), TimetableSlotResponse, TimetableUploadDetailResponse, upload_timetable() (+10 more)

### Community 11 - "Test-Driven Development (TDD)"
Cohesion: 0.15
Nodes (18): BulkImportFacultyUseCase, BulkImportReport, RowImportResult, CreateFacultyUseCase, DeactivateFacultyUseCase, ManageTermsUseCase, UpdateFacultyUseCase, AuthorisationPolicy (+10 more)

### Community 12 - "calendar.py"
Cohesion: 0.09
Nodes (14): CalendarEventResponse, cancel_calendar_event(), check_event_clashes(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots() (+6 more)

### Community 13 - "auth.py"
Cohesion: 0.08
Nodes (30): get_clock(), get_current_principal(), get_uow(), require_admin(), require_hod_or_admin(), AcademicTermResponse, add_holiday(), bulk_import_faculty() (+22 more)

### Community 14 - "main.py"
Cohesion: 0.09
Nodes (6): configure_logging(), RequestIdMiddleware, domain_exception_handler(), healthz(), lifespan(), readyz()

### Community 15 - "UnitOfWork"
Cohesion: 0.11
Nodes (3): get_ics_feed(), Clock, UnitOfWork

### Community 16 - "Principal"
Cohesion: 0.08
Nodes (31): Interval, intervals_overlap(), pairwise_clashes(), SweepLineClashDetector, test_adjacent_intervals_no_clash(), test_sweep_line_clash_detection_matches_pairwise_property(), test_worked_example_from_maths_md(), test_meeting_time_grammar_table() (+23 more)

### Community 17 - "package.json"
Cohesion: 0.18
Nodes (16): ChangePasswordUseCase, LoginResult, LoginUseCase, LogoutUseCase, RefreshResult, RefreshTokenUseCase, UnauthorizedError, create_access_token() (+8 more)

### Community 18 - "reminders.py"
Cohesion: 0.13
Nodes (6): faculty_profile_to_domain(), FacultyProfileRepositoryImpl, notification_to_domain(), NotificationRepositoryImpl, timetable_slot_to_domain(), TimetableSlotRepositoryImpl

### Community 19 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 20 - "reminders.py"
Cohesion: 0.07
Nodes (22): delete_push_subscription(), DeletePushSubscriptionRequest, get_quiet_hours(), get_reminder_rules(), get_upcoming_notifications(), PushSubscriptionRequest, PushSubscriptionResponse, QuietHoursResponse (+14 more)

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
Cohesion: 0.05
Nodes (21): CircularDetailResponse, CircularUploadResponse, confirm_circular(), ConfirmCircularRequest, ConfirmCircularResponse, get_circular(), list_review_queue(), reject_circular() (+13 more)

### Community 25 - "TimetableSlot"
Cohesion: 0.24
Nodes (7): expand_slot_recurrence(), AcademicTerm, TimetableSlot, test_recurrence_expansion_matching_weekday(), test_recurrence_expansion_skips_holidays(), test_recurrence_expansion_utc_roundtrip(), 1.4 Recurrence Expansion and Rolling 21-Day Materialisation Window

### Community 26 - "ReminderRule"
Cohesion: 0.36
Nodes (3): ReminderRule, reminder_rule_to_domain(), ReminderRuleRepositoryImpl

### Community 27 - "Event"
Cohesion: 0.17
Nodes (8): generate_vcalendar_ics(), MaterialiseTimetableEventsUseCase, ReminderPlanner, Event, event_to_domain(), test_ics_export_stable_uids(), test_ics_export_valid_rfc5545(), 2.4 RFC 5545 ICS Feed Specification

### Community 28 - "extractor.py"
Cohesion: 0.06
Nodes (35): compute_length_weighted_confidence(), OcrEngine, OcrResult, WordBox, CircularExtractor, ExtractedAttendee, ExtractedTime, ExtractionResult (+27 more)

### Community 29 - "get_settings"
Cohesion: 0.16
Nodes (7): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_settings(), Settings, get_db()

### Community 30 - "Systematic Debugging"
Cohesion: 0.10
Nodes (19): Browser Events Format, Cards (visual designs), Cleaning Up, CSS Classes Available, Design Tips, File Naming, How It Works, Mock elements (wireframe building blocks) (+11 more)

### Community 31 - "RefreshToken"
Cohesion: 0.10
Nodes (19): Bulletproofing Elements, Creation Log: Systematic Debugging Skill, Enhancement 1: TDD Reference, Extraction Decisions, Final Outcome, Initial Version, Iterations, Key Insight (+11 more)

### Community 32 - "components.json"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 33 - "Condition-Based Waiting"
Cohesion: 0.41
Nodes (10): DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged, TimetableConfirmed, Domain (backend/app/domain) (+2 more)

### Community 34 - "ScheduledNotification"
Cohesion: 0.20
Nodes (3): ScheduledNotification, EmailNotifier, test_mailpit_real_delivery()

### Community 36 - "ScheduledNotification"
Cohesion: 0.10
Nodes (19): 1. Problem and users, 3. Architecture, 4.10 Reminder Dispatch and Exactly-Once Delivery Sequence, 4.11 Meeting Circular Scanning, Extraction, and Review Sequence, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine, 4.4 ScheduledNotification State Machine (+11 more)

### Community 37 - "Root Cause Tracing"
Cohesion: 0.21
Nodes (10): adjust_for_quiet_hours(), compute_backoff_delay(), compute_fire_time(), compute_idempotency_key(), QuietHours, test_quiet_hours_midnight_crossing(), test_backoff_bounds(), test_fire_time_computation() (+2 more)

### Community 38 - "reminder_tasks.py"
Cohesion: 0.21
Nodes (8): _build_dispatcher(), dispatch_due_notifications(), recover_stale_sending_notifications(), _run_dispatch(), _run_recover(), FacultyDesk Decisions, Stage 00: Agent setup, Stage 03: Authentication, authorization, and faculty directory

### Community 39 - "Course"
Cohesion: 0.20
Nodes (4): Holiday, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 41 - "domain/__init__.py"
Cohesion: 0.28
Nodes (8): test_circular_state_machine_exhaustive(), test_event_invariants(), test_initials_invalid_property(), test_initials_valid_property(), test_notification_state_machine_exhaustive(), test_task_invariants(), test_timeslot_invariants(), ScheduledNotification State Machine

### Community 42 - "Root Cause Tracing"
Cohesion: 0.12
Nodes (15): 1. Observe the Symptom, 2. Find Immediate Cause, 3. Ask: What Called This?, 4. Keep Tracing Up, 5. Find Original Trigger, Adding Stack Traces, Finding Which Test Causes Pollution, Key Principle (+7 more)

### Community 43 - "Defense-in-Depth Validation"
Cohesion: 0.12
Nodes (15): Common Rationalizations, Overview, Phase 1: Root Cause Investigation, Phase 2: Pattern Analysis, Phase 3: Hypothesis and Testing, Phase 4: Implementation, Quick Reference, Red Flags - STOP and Follow Process (+7 more)

### Community 44 - "PushSubscription"
Cohesion: 0.22
Nodes (3): PushSubscription, push_subscription_to_domain(), PushSubscriptionRepositoryImpl

### Community 45 - "devDependencies"
Cohesion: 0.12
Nodes (15): aliases, components, hooks, lib, ui, utils, rsc, $schema (+7 more)

### Community 46 - "Brainstorming"
Cohesion: 0.15
Nodes (12): Common Mistakes, Condition-Based Waiting, Core Pattern, waitForEvent(), waitForEventCount(), waitForEventMatch(), Implementation, Overview (+4 more)

### Community 47 - "Department"
Cohesion: 0.25
Nodes (5): FrozenClock, test_clock_always_returns_utc_property(), test_frozen_clock_advance_property(), test_frozen_clock_rejects_naive_datetime(), 1.1 Canonical Time Representation and Clock Invariant

### Community 48 - "entities.py"
Cohesion: 0.18
Nodes (12): ConfirmCircularUseCase, UploadCircularUseCase, AttendeeResponse, CircularStatus, EventKind, EventSource, NotificationChannel, NotificationStatus (+4 more)

### Community 49 - "Section"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 50 - "zoneinfo"
Cohesion: 0.29
Nodes (5): BusyInterval, FreeSlotFinder, merge_busy_intervals(), test_free_slots_never_intersect_busy_property(), test_free_slots_worked_example()

### Community 51 - "FacultyDesk Agent Contract"
Cohesion: 0.18
Nodes (3): RefreshToken, refresh_token_to_domain(), RefreshTokenRepositoryImpl

### Community 52 - "Verification Before Completion"
Cohesion: 0.25
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

### Community 58 - "TimetableUpload"
Cohesion: 0.13
Nodes (11): TimetableUpload, InvalidTransition, timetable_upload_to_domain(), TimetableUploadRepositoryImpl, Acceptance criteria, Goal, Input formats to support, Maths to specify first (+3 more)

### Community 59 - "Web Application Testing"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, eslint-config-next, openapi-typescript, prettier, prettier-plugin-tailwindcss, tailwindcss, @tailwindcss/turbopack (+4 more)

### Community 60 - "Stage 05: Calendar core, recurrence, clash detection, ICS feed"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 05: Calendar core, recurrence, clash detection, ICS feed, Tests

### Community 61 - "NotificationRepositoryImpl"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 62 - "Stage 01: Foundation, environment, Graphify, trusted skills"
Cohesion: 0.50
Nodes (3): Acceptance criteria, Goal, Stage 01: Foundation, environment, Graphify, trusted skills

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
Cohesion: 0.25
Nodes (7): Acceptance criteria, Diagrams, Goal, Maths to specify first (MATHS.md), Persistence, Stage 02: Domain model and persistence (OOAD core), Tests

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

### Community 91 - "Reviewer"
Cohesion: 0.40
Nodes (4): Backend Engineer, Responsibilities, Standards you are held to, Working method

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

### Community 113 - "1.3 State Machine Transition Algebras"
Cohesion: 0.50
Nodes (4): 1.2 Half-Open Interval Invariant and Overlap Arithmetic, 1.3 State Machine Transition Algebras, 1. Time and Recurrence, Circular State Machine

## Knowledge Gaps
- **23 isolated node(s):** `facultydesk-backend`, `RFC-6455`, `clsx`, `@fullcalendar/core`, `@fullcalendar/daygrid` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 755 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `Department`, `main.py`, `domain/__init__.py`, `directory.py`, `User`, `db/repositories.py`, `timetable.py`, `Test-Driven Development (TDD)`, `calendar.py`, `auth.py`, `package.json`, `reminders.py`, `Executing Plans`, `Circular`, `Event`, `extractor.py`, `Condition-Based Waiting`, `ScheduledNotification`, `entities.py`, `Stage 07: Meeting circular scanning, extraction and review queue`, `.__aexit__`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 39 INFERRED edges - model-reasoned connections that need verification._
- **What connects `facultydesk-backend`, `RFC-6455`, `clsx` to the rest of the system?**
  _23 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `datetime` be split into smaller, more focused modules?**
  _Cohesion score 0.08701923076923077 - nodes in this community are weakly interconnected._
- **Why does `2. Features that exist now` connect `User` to `Department`, `main.py`, `directory.py`, `timetable.py`, `Test-Driven Development (TDD)`, `UnitOfWork`, `Circular`, `TimetableSlot`, `ReminderRule`, `Event`, `Condition-Based Waiting`, `ScheduledNotification`, `ScheduledNotification`, `Course`, `PushSubscription`, `Department`, `FacultyDesk Agent Contract`, `Verification Before Completion`, `Course`, `scripts`, `Section`, `TimetableUpload`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `Principal` (e.g. with `require_admin()` and `require_hod_or_admin()`) actually correct?**
  _`Principal` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._