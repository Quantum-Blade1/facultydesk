# Graph Report - facultydesk  (2026-10-28)

## Corpus Check
- 240 files · ~345,224 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: (none) 11, .csv 2, .example 1)

## Summary
- 2309 nodes · 6728 edges · 148 communities (115 shown, 33 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 1056 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `75f9b5f2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- server.cjs
- AsyncSession
- entities.py
- get_settings
- UUID
- SqlAlchemyUnitOfWork
- db/repositories.py
- main.py
- Clock
- sqlalchemy
- calendar.py
- directory.py
- @playwright/test
- Task
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- uuid
- ABC
- Test-Driven Development (TDD)
- reminders.py
- Holiday
- deps.py
- Visual Companion Guide
- Circular
- AcademicTermRepositoryImpl
- Principal
- FacultyProfile
- clash_detector.py
- tasks.py
- Systematic Debugging
- RefreshToken
- components.json
- domain/__init__.py
- InvariantViolation
- CircularRepository
- 5. How to run, test and deploy
- reminders/maths.py
- compute_priority_score
- RedisSlidingWindowRateLimiter
- ReminderRuleRepository
- calendar/__init__.py
- Root Cause Tracing
- Defense-in-Depth Validation
- manifest.json
- devDependencies
- Brainstorming
- test_clock.py
- FacultyProfile
- Section
- pytest
- Section
- tasks/use_cases.py
- deps.py
- Room
- helper.js
- Brainstorming
- Course
- RefreshToken
- Web Application Testing
- User
- NotificationRepositoryImpl
- 4.3 Standard OOAD Diagram Pack
- TimetableUpload
- celery_app.py
- FacultyDesk Agent Contract
- Trusted External Skills
- stop-server.sh
- helper.js
- TimetableSlotRepository
- FacultyDesk Maths
- directory/page.tsx
- Graphify Protocol
- Stage 07: Meeting circular scanning, extraction and review queue
- Stage 08: Documentation tasks, priority scoring and alerts
- Code Quality Bar
- stop-server.sh
- Build Loop
- test_ocr_maths.py
- TaskTemplate
- ._transition
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- Stage 06: Reminder engine with exactly-once delivery
- Stage 10: Security, reliability and observability hardening
- Build Loop
- Math First
- PushSubscription
- Frontend Engineer
- Math Verifier
- Orchestrator
- timetable.py
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
- Backend Engineer
- builder-check-prompt.md
- task-done
- Kickoff prompt (paste this into the Antigravity agent)
- ooad-diagrams/SKILL.md
- 5. Initials and Name Matching
- Stage 01: Foundation, environment, Graphify, trusted skills
- test-academic.md
- api/__init__.py
- application/__init__.py
- find-polluter.sh
- infrastructure/__init__.py
- seed/__init__.py
- Department
- NotificationRepositoryImpl
- AuditLogRepository
- FacultyDesk Decisions
- facultydesk-backend
- test_circular_full_pipeline_with_samples
- 11. Hardening, Observability and Reliability
- TimetableSlot
- get_db
- delete_task
- Circular
- Stage 07: Meeting circular scanning, extraction and review queue
- auth.py

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 182 edges
2. `Clock` - 111 edges
3. `Principal` - 95 edges
4. `FacultyProfile` - 81 edges
5. `ScheduledNotification` - 80 edges
6. `Event` - 72 edges
7. `User` - 64 edges
8. `NotFoundError` - 58 edges
9. `Initials` - 52 edges
10. `SqlAlchemyUnitOfWork` - 50 edges

## Surprising Connections (you probably didn't know these)
- `10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix` --references--> `AuthorisationPolicy`  [INFERRED]
  docs/MATHS.md → backend/app/application/security/policy.py
- `Standards you are held to` --references--> `Clock`  [INFERRED]
  .agents/agents/backend-engineer.md → backend/app/core/clock.py
- `Non-negotiables` --references--> `Clock`  [INFERRED]
  AGENTS.md → backend/app/core/clock.py
- `5.4 Merged-Cell Period Expansion` --references--> `TimetableSlot`  [INFERRED]
  docs/MATHS.md → backend/app/domain/entities.py
- `Pipeline` --references--> `Circular`  [INFERRED]
  prompts/07-circular-ocr.md → backend/app/domain/entities.py

## Import Cycles
- None detected.

## Communities (148 total, 33 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.07
Nodes (40): OCR and Parsing Engineer, Responsibilities, Rules, get_storage(), ParseTimetableUseCase, split_co_teachers(), tokenize_cell(), CsvTimetableParser (+32 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 3 - "entities.py"
Cohesion: 0.11
Nodes (24): check_event_clashes(), generate_vcalendar_ics(), CheckClashesUseCase, CreateEventUseCase, GenerateIcsFeedUseCase, GetCalendarEventsUseCase, MaterialiseTimetableEventsUseCase, RotateIcsTokenUseCase (+16 more)

### Community 4 - "get_settings"
Cohesion: 0.14
Nodes (6): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_settings(), Settings

### Community 6 - "UUID"
Cohesion: 0.11
Nodes (6): ReminderRuleModel, EventRepositoryImpl, faculty_profile_to_domain(), FacultyProfileRepositoryImpl, reminder_rule_to_domain(), ReminderRuleRepositoryImpl

### Community 7 - "SqlAlchemyUnitOfWork"
Cohesion: 0.14
Nodes (16): ProcessCircularUseCase, SystemClock, materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation(), process_circular_upload(), _run_process_circular(), _build_dispatcher() (+8 more)

### Community 8 - "db/repositories.py"
Cohesion: 0.27
Nodes (12): Base, DepartmentModel, EventAttendeeModel, EventModel, FacultyProfileModel, HolidayModel, ScheduledNotificationModel, TaskModel (+4 more)

### Community 9 - "main.py"
Cohesion: 0.07
Nodes (10): is_server_ready(), main(), configure_logging(), RequestIdMiddleware, domain_exception_handler(), healthz(), lifespan(), readyz() (+2 more)

### Community 10 - "Clock"
Cohesion: 0.12
Nodes (7): deactivate_faculty(), StatusResponse, BulkImportFacultyUseCase, BulkImportReport, RowImportResult, DeactivateFacultyUseCase, Clock

### Community 11 - "sqlalchemy"
Cohesion: 0.17
Nodes (5): upgrade(), upgrade(), upgrade(), upgrade(), upgrade()

### Community 12 - "calendar.py"
Cohesion: 0.10
Nodes (15): CalendarEventResponse, cancel_calendar_event(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots(), FindFreeSlotsRequest (+7 more)

### Community 13 - "directory.py"
Cohesion: 0.08
Nodes (28): get_clock(), get_current_principal(), get_uow(), require_admin(), require_hod_or_admin(), AcademicTermResponse, add_holiday(), bulk_import_faculty() (+20 more)

### Community 15 - "Task"
Cohesion: 0.10
Nodes (14): AssignTaskUseCase, EventAttendee, Task, TaskRepository, TaskCategory, TaskRecurrence, TaskStatus, task_to_domain() (+6 more)

### Community 16 - "Stage 05: Calendar core, recurrence, clash detection, ICS feed"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 05: Calendar core, recurrence, clash detection, ICS feed, Tests

### Community 17 - "uuid"
Cohesion: 0.16
Nodes (16): ChangePasswordUseCase, LoginResult, LoginUseCase, LogoutUseCase, RefreshResult, RefreshTokenUseCase, UnauthorizedError, create_access_token() (+8 more)

### Community 18 - "ABC"
Cohesion: 0.12
Nodes (6): EventRepository, TaskTemplateRepository, UserRepository, TaskTemplateRepositoryImpl, user_to_domain(), UserRepositoryImpl

### Community 19 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 20 - "reminders.py"
Cohesion: 0.06
Nodes (27): delete_push_subscription(), DeletePushSubscriptionRequest, get_quiet_hours(), get_reminder_rules(), get_upcoming_notifications(), get_vapid_public_key(), PushSubscriptionRequest, PushSubscriptionResponse (+19 more)

### Community 21 - "Holiday"
Cohesion: 0.15
Nodes (3): Holiday, AcademicTermRepository, holiday_to_domain()

### Community 22 - "deps.py"
Cohesion: 0.08
Nodes (24): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+16 more)

### Community 23 - "Visual Companion Guide"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 24 - "Circular"
Cohesion: 0.11
Nodes (16): CircularDetailResponse, CircularUploadResponse, confirm_circular(), ConfirmCircularRequest, ConfirmCircularResponse, get_circular(), list_review_queue(), reject_circular() (+8 more)

### Community 25 - "AcademicTermRepositoryImpl"
Cohesion: 0.43
Nodes (3): AcademicTermModel, academic_term_to_domain(), AcademicTermRepositoryImpl

### Community 26 - "Principal"
Cohesion: 0.17
Nodes (14): CreateFacultyUseCase, ManageTermsUseCase, UpdateFacultyUseCase, AuthorisationPolicy, Principal, UploadTimetableUseCase, ConflictError, FacultyDeskError (+6 more)

### Community 28 - "clash_detector.py"
Cohesion: 0.33
Nodes (8): Interval, intervals_overlap(), pairwise_clashes(), SweepLineClashDetector, test_adjacent_intervals_no_clash(), test_sweep_line_clash_detection_matches_pairwise_property(), test_worked_example_from_maths_md(), 2.2 Sweep-Line Interval Clash Detection Algorithm

### Community 29 - "tasks.py"
Cohesion: 0.13
Nodes (17): assign_task(), AssignmentProgressResponse, AssignTaskRequest, complete_task(), create_task(), CreateTaskRequest, ensure_utc(), FacultyOverdueSummaryResponse (+9 more)

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
Cohesion: 0.29
Nodes (11): DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged, TimetableConfirmed, test_event_reschedule() (+3 more)

### Community 35 - "CircularRepository"
Cohesion: 0.23
Nodes (4): CircularRepository, CircularModel, circular_to_domain(), CircularRepositoryImpl

### Community 36 - "5. How to run, test and deploy"
Cohesion: 0.20
Nodes (9): 1. Problem and users, 3. Architecture, 5. How to run, test and deploy, College-LAN mode (Department Server deployment), Development commands, FacultyDesk, Prerequisites, Production deployment (+1 more)

### Community 37 - "reminders/maths.py"
Cohesion: 0.19
Nodes (13): adjust_for_quiet_hours(), compute_backoff_delay(), compute_fire_time(), compute_idempotency_key(), QuietHours, test_quiet_hours_midnight_crossing(), test_backoff_bounds(), test_fire_time_computation() (+5 more)

### Community 38 - "compute_priority_score"
Cohesion: 0.21
Nodes (14): compute_completion_rate(), compute_lead_alert_times(), compute_overdue_alert_times(), compute_priority_score(), test_completed_task_priority(), test_completion_rate(), test_lead_alert_times(), test_overdue_alert_times() (+6 more)

### Community 39 - "RedisSlidingWindowRateLimiter"
Cohesion: 0.29
Nodes (5): get_rate_limiter(), RateLimitExceededError, get_redis_client(), RedisSlidingWindowRateLimiter, test_sliding_window_rate_limiter()

### Community 41 - "calendar/__init__.py"
Cohesion: 0.20
Nodes (6): BusyInterval, FreeSlotFinder, merge_busy_intervals(), FindFreeSlotsUseCase, test_free_slots_never_intersect_busy_property(), test_free_slots_worked_example()

### Community 42 - "Root Cause Tracing"
Cohesion: 0.12
Nodes (15): 1. Observe the Symptom, 2. Find Immediate Cause, 3. Ask: What Called This?, 4. Keep Tracing Up, 5. Find Original Trigger, Adding Stack Traces, Finding Which Test Causes Pollution, Key Principle (+7 more)

### Community 43 - "Defense-in-Depth Validation"
Cohesion: 0.12
Nodes (15): Common Rationalizations, Overview, Phase 1: Root Cause Investigation, Phase 2: Pattern Analysis, Phase 3: Hypothesis and Testing, Phase 4: Implementation, Quick Reference, Red Flags - STOP and Follow Process (+7 more)

### Community 44 - "manifest.json"
Cohesion: 0.22
Nodes (8): background_color, description, display, icons, name, short_name, start_url, theme_color

### Community 45 - "devDependencies"
Cohesion: 0.12
Nodes (15): aliases, components, hooks, lib, ui, utils, rsc, $schema (+7 more)

### Community 46 - "Brainstorming"
Cohesion: 0.15
Nodes (12): Common Mistakes, Condition-Based Waiting, Core Pattern, waitForEvent(), waitForEventCount(), waitForEventMatch(), Implementation, Overview (+4 more)

### Community 47 - "test_clock.py"
Cohesion: 0.18
Nodes (8): test_clock_always_returns_utc_property(), test_frozen_clock_advance_property(), test_frozen_clock_rejects_naive_datetime(), 1.1 Canonical Time Representation and Clock Invariant, 1.2 Half-Open Interval Invariant and Overlap Arithmetic, 1.3 State Machine Transition Algebras, 1. Time and Recurrence, Circular State Machine

### Community 48 - "FacultyProfile"
Cohesion: 0.06
Nodes (11): ReminderDispatcher, ScheduledNotification, NotificationRepository, NotificationStatus, NotificationPayload, Notifier, EmailNotifier, CompositeNotifier (+3 more)

### Community 49 - "Section"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 50 - "pytest"
Cohesion: 0.05
Nodes (30): compute_lateness_percentiles(), ValidationError, detect_mime_and_extension(), validate_upload_content(), rasterise_pdf_page(), BackupService, backup_database_to_minio(), cleanup_db_connections() (+22 more)

### Community 51 - "Section"
Cohesion: 0.26
Nodes (5): Section, SectionRepository, SectionModel, section_to_domain(), SectionRepositoryImpl

### Community 52 - "tasks/use_cases.py"
Cohesion: 0.18
Nodes (10): AssignmentProgress, CompleteTaskUseCase, CreateTaskUseCase, FacultyOverdueSummary, GetHodDashboardUseCase, HodDashboardData, ListTasksUseCase, ReopenTaskUseCase (+2 more)

### Community 53 - "deps.py"
Cohesion: 0.20
Nodes (7): get_redis(), AdminMetricsResponse, DeadLetterResponse, get_system_metrics(), LatenessPercentilesResponse, QueueDepthResponse, retry_failed_notification()

### Community 54 - "Room"
Cohesion: 0.26
Nodes (5): Room, RoomRepository, RoomModel, room_to_domain(), RoomRepositoryImpl

### Community 55 - "helper.js"
Cohesion: 0.17
Nodes (11): Applying the Pattern, Defense-in-Depth Validation, Example from Session, Key Insight, Layer 1: Entry Point Validation, Layer 2: Business Logic Validation, Layer 3: Environment Guards, Layer 4: Debug Instrumentation (+3 more)

### Community 56 - "Brainstorming"
Cohesion: 0.17
Nodes (11): Execution Handoff, File Structure, Overview, Plan Document Header, Scope Check, Self-Review, Step Granularity, Task Right-Sizing (+3 more)

### Community 57 - "Course"
Cohesion: 0.26
Nodes (5): Course, CourseRepository, CourseModel, course_to_domain(), CourseRepositoryImpl

### Community 58 - "RefreshToken"
Cohesion: 0.26
Nodes (5): RefreshToken, RefreshTokenRepository, RefreshTokenModel, refresh_token_to_domain(), RefreshTokenRepositoryImpl

### Community 59 - "Web Application Testing"
Cohesion: 0.15
Nodes (13): devDependencies, eslint, eslint-config-next, openapi-typescript, @playwright/test, prettier, prettier-plugin-tailwindcss, tailwindcss (+5 more)

### Community 60 - "User"
Cohesion: 0.21
Nodes (18): FrozenClock, AcademicTerm, Department, User, Initials, Role, SqlAlchemyUnitOfWork, main() (+10 more)

### Community 61 - "NotificationRepositoryImpl"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 62 - "4.3 Standard OOAD Diagram Pack"
Cohesion: 0.17
Nodes (12): 4.3.10 Deployment Diagram: Production & College-LAN Topology, 4.3.11 Entity-Relationship (ER) Diagram, 4.3.1 Use Case Diagram, 4.3.2 Domain Class Diagram, 4.3.3 Sequence Diagram: Timetable Upload and Class Materialisation, 4.3.4 Sequence Diagram: Circular OCR Scan & Review Queue, 4.3.5 Sequence Diagram: Periodic Reminder Dispatch (Atomic SKIP LOCKED), 4.3.6 State Diagram: Circular Lifecycle (+4 more)

### Community 63 - "TimetableUpload"
Cohesion: 0.10
Nodes (10): TimetableUpload, InvalidTransition, TimetableUploadRepository, Acceptance criteria, Goal, Input formats to support, Maths to specify first, Pipeline (+2 more)

### Community 64 - "celery_app.py"
Cohesion: 0.25
Nodes (4): on_before_task_publish(), on_task_postrun(), on_task_prerun(), ping()

### Community 65 - "FacultyDesk Agent Contract"
Cohesion: 0.20
Nodes (9): Architecture law, Communication style, Definition of done for every stage, FacultyDesk Agent Contract, Fixed tech stack (do not substitute), How work is organised, Non-negotiables, Product in one paragraph (+1 more)

### Community 66 - "Trusted External Skills"
Cohesion: 0.20
Nodes (9): Common Failures, Key Patterns, Overview, Rationalization Prevention, Red Flags - STOP, The Gate Function, The Iron Law, Verification Before Completion (+1 more)

### Community 67 - "stop-server.sh"
Cohesion: 0.17
Nodes (12): scripts, build, dev, fmt, format:check, gen:api, generate:api, lint (+4 more)

### Community 68 - "helper.js"
Cohesion: 0.42
Nodes (7): connect(), nextReconnectDelay(), reloadAfterRecovery(), sessionKey(), setStatus(), showTombstone(), websocketUrl()

### Community 70 - "FacultyDesk Maths"
Cohesion: 0.09
Nodes (21): 10.1 Token Lifetimes, Rotation, and Family Reuse Detection, 10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix, 10.3 Sliding Window Log Rate Limiting, 10. Security Limits, 2.1 Half-Open Overlap Predicate, 2.3 Multi-Attendee Common Free-Slot Finder, 2. Clash Detection and Calendar Operations, 4.1 Deterministic Idempotency Key Derivation (+13 more)

### Community 71 - "directory/page.tsx"
Cohesion: 0.09
Nodes (36): nextConfig, CalendarPage(), CircularsPage(), DirectoryPage(), metadata, RootLayout(), viewport, LoginPage() (+28 more)

### Community 72 - "Graphify Protocol"
Cohesion: 0.25
Nodes (7): Best Practices, Common Pitfall, Decision Tree: Choosing Your Approach, Example: Using with_server.py, Reconnaissance-Then-Action Pattern, Reference Files, Web Application Testing

### Community 74 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.13
Nodes (12): Acceptance criteria, Diagrams, Goal, Maths to specify first (MATHS.md), Persistence, Stage 02: Domain model and persistence (OOAD core), Tests, Acceptance criteria (+4 more)

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

### Community 79 - "test_ocr_maths.py"
Cohesion: 0.06
Nodes (37): detect_probable_duplicate(), normalize_title(), compute_length_weighted_confidence(), OcrEngine, OcrResult, WordBox, CircularExtractor, ExtractedAttendee (+29 more)

### Community 80 - "TaskTemplate"
Cohesion: 0.15
Nodes (5): list_templates(), TaskTemplateResponse, ListTaskTemplatesUseCase, TaskTemplate, task_template_to_domain()

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

### Community 87 - "PushSubscription"
Cohesion: 0.18
Nodes (5): PushSubscription, PushSubscriptionRepository, PushSubscriptionModel, push_subscription_to_domain(), PushSubscriptionRepositoryImpl

### Community 88 - "Frontend Engineer"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 10: Security, reliability and observability hardening, Tasks

### Community 89 - "Math Verifier"
Cohesion: 0.33
Nodes (5): Before you start (one time, about 10 minutes), Run, Start here, What this folder is, What to show your guide

### Community 90 - "Orchestrator"
Cohesion: 0.40
Nodes (4): Architect, Design checks, Output for every design task, Responsibilities

### Community 91 - "timetable.py"
Cohesion: 0.13
Nodes (9): confirm_timetable(), ConfirmTimetableResponse, get_faculty_slots(), get_timetable_upload(), TimetableSlotResponse, TimetableUploadDetailResponse, upload_timetable(), UploadTimetableResponse (+1 more)

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

### Community 108 - "Backend Engineer"
Cohesion: 0.40
Nodes (4): Backend Engineer, Responsibilities, Standards you are held to, Working method

### Community 109 - "builder-check-prompt.md"
Cohesion: 0.50
Nodes (3): eslintConfig, eslint, eslint-config-next

### Community 110 - "task-done"
Cohesion: 0.50
Nodes (3): Deploy on Vercel, Getting Started, Learn More

### Community 111 - "Kickoff prompt (paste this into the Antigravity agent)"
Cohesion: 0.50
Nodes (3): Kickoff prompt (paste this into the Antigravity agent), Resuming in a new conversation, Running a single stage manually

### Community 113 - "5. Initials and Name Matching"
Cohesion: 0.40
Nodes (5): 5.1 Initials Value Object Invariant, 5.2 Timetable Cell Tokenization Grammar, 5.4 Merged-Cell Period Expansion, 5.5 Header Day and Time Normalization, 5. Initials and Name Matching

### Community 114 - "Stage 01: Foundation, environment, Graphify, trusted skills"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 01: Foundation, environment, Graphify, trusted skills, Tasks

### Community 131 - "AuditLogRepository"
Cohesion: 0.18
Nodes (7): AuditLogRepository, AuditLogModel, TimetableUploadModel, audit_log_to_domain(), AuditLogRepositoryImpl, timetable_upload_to_domain(), TimetableUploadRepositoryImpl

### Community 135 - "FacultyDesk Decisions"
Cohesion: 0.50
Nodes (3): FacultyDesk Decisions, Stage 00: Agent setup, Stage 01: Foundation, environment, Graphify, trusted skills

### Community 138 - "test_circular_full_pipeline_with_samples"
Cohesion: 0.25
Nodes (3): InMemoryStorageService, sample_dir(), test_circular_full_pipeline_with_samples()

### Community 139 - "11. Hardening, Observability and Reliability"
Cohesion: 0.50
Nodes (4): 11.1 Dispatch Lateness Percentile Computation, 11.2 Backup Retention Arithmetic & Bounded Pruning, 11.3 Upload Decompression Bomb and Page Count Limits, 11. Hardening, Observability and Reliability

### Community 140 - "TimetableSlot"
Cohesion: 0.22
Nodes (10): expand_slot_recurrence(), TimetableSlot, TimeSlot, timetable_slot_to_domain(), TimetableSlotRepositoryImpl, test_timeslot_half_open_overlap(), test_recurrence_expansion_matching_weekday(), test_recurrence_expansion_skips_holidays() (+2 more)

### Community 143 - "delete_task"
Cohesion: 0.25
Nodes (3): delete_task(), DeleteTaskUseCase, DomainError

### Community 144 - "Circular"
Cohesion: 0.20
Nodes (4): Circular, CircularStatus, test_round_trip_all_aggregates(), 4.1.3 Core Domain Classes and Rationales

### Community 145 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Corpus and tests, Goal, Maths to specify first, Pipeline, Stage 07: Meeting circular scanning, extraction and review queue

### Community 147 - "auth.py"
Cohesion: 0.18
Nodes (14): change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest, LoginResponse (+6 more)

## Knowledge Gaps
- **22 isolated node(s):** `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 848 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **33 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `reminders.py` to `datetime`, `entities.py`, `get_settings`, `AuditLogRepository`, `SqlAlchemyUnitOfWork`, `Clock`, `calendar.py`, `directory.py`, `delete_task`, `Task`, `uuid`, `ABC`, `auth.py`, `Circular`, `Principal`, `tasks.py`, `domain/__init__.py`, `reminders/maths.py`, `calendar/__init__.py`, `FacultyProfile`, `tasks/use_cases.py`, `deps.py`, `User`, `Stage 07: Meeting circular scanning, extraction and review queue`, `test_ocr_maths.py`, `TaskTemplate`, `timetable.py`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 52 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `datetime` be split into smaller, more focused modules?**
  _Cohesion score 0.0680672268907563 - nodes in this community are weakly interconnected._
- **Why does `Event` connect `entities.py` to `domain/__init__.py`, `InvariantViolation`, `AuditLogRepository`, `reminders/maths.py`, `UUID`, `db/repositories.py`, `calendar.py`, `Task`, `FacultyProfile`, `test_ocr_maths.py`, `ABC`, `Circular`, `tasks/use_cases.py`, `pytest`, `Circular`, `User`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Clock` (e.g. with `Standards you are held to` and `Non-negotiables`) actually correct?**
  _`Clock` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._