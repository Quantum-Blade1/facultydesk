# Graph Report - facultydesk  (2026-10-28)

## Corpus Check
- 242 files · ~218,516 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: (none) 11, .csv 2, .example 1)

## Summary
- 2302 nodes · 6659 edges · 141 communities (112 shown, 29 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 992 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e92172fd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- server.cjs
- Department
- Event
- get_settings
- UUID
- FacultyProfileRepositoryImpl
- SqlAlchemyUnitOfWork
- db/repositories.py
- main.py
- UnitOfWork
- Principal
- calendar.py
- auth.py
- @playwright/test
- Task
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- auth.py
- UUID
- Test-Driven Development (TDD)
- reminders.py
- InvariantViolation
- deps.py
- Visual Companion Guide
- Circular
- AcademicTermRepositoryImpl
- demo_setup.py
- create_task
- circulars/use_cases.py
- assign_task
- Systematic Debugging
- RefreshToken
- components.json
- Domain (backend/app/domain)
- InvariantViolation
- AsyncSession
- ScheduledNotification
- reminders/maths.py
- compute_priority_score
- ReminderRuleRepositoryImpl
- calendar/__init__.py
- Root Cause Tracing
- Defense-in-Depth Validation
- manifest.json
- devDependencies
- Brainstorming
- SqlAlchemyUnitOfWork
- FacultyProfile
- Section
- upload_timetable
- Section
- tasks/use_cases.py
- metrics.py
- Room
- helper.js
- Brainstorming
- Course
- EntityNotFound
- Web Application Testing
- 10. Security Limits
- NotificationRepositoryImpl
- reminders/use_cases.py
- Circular
- celery_app.py
- FacultyDesk Agent Contract
- Trusted External Skills
- stop-server.sh
- helper.js
- Stage 03: Authentication, authorization, and faculty directory
- FacultyDesk Maths
- directory/page.tsx
- Graphify Protocol
- Stage 07: Meeting circular scanning, extraction and review queue
- Stage 08: Documentation tasks, priority scoring and alerts
- Code Quality Bar
- stop-server.sh
- Build Loop
- test_initials_matching.py
- TaskTemplate
- ._transition
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- Stage 06: Reminder engine with exactly-once delivery
- Stage 10: Security, reliability and observability hardening
- Build Loop
- Math First
- Frontend Engineer
- Math Verifier
- Orchestrator
- MinioStorageService
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
- builder-check-prompt.md
- task-done
- Kickoff prompt (paste this into the Antigravity agent)
- ooad-diagrams/SKILL.md
- test-academic.md
- api/__init__.py
- application/__init__.py
- find-polluter.sh
- infrastructure/__init__.py
- seed/__init__.py
- NotificationRepositoryImpl
- bulk_import.py
- facultydesk-backend
- QuietHours
- test_parsers.py
- delete_task
- CircularRepositoryImpl
- tasks.py
- Stage 06: Reminder engine with exactly-once delivery
- Clock
- 5. Initials and Name Matching
- OCR and Parsing Engineer

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 182 edges
2. `Clock` - 111 edges
3. `Principal` - 95 edges
4. `FacultyProfile` - 79 edges
5. `ScheduledNotification` - 77 edges
6. `Event` - 69 edges
7. `User` - 64 edges
8. `NotFoundError` - 58 edges
9. `InvariantViolation` - 49 edges
10. `Initials` - 49 edges

## Surprising Connections (you probably didn't know these)
- `10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix` --references--> `AuthorisationPolicy`  [INFERRED]
  docs/MATHS.md → backend/app/application/security/policy.py
- `Non-negotiables` --references--> `Clock`  [INFERRED]
  AGENTS.md → backend/app/core/clock.py
- `5.4 Merged-Cell Period Expansion` --references--> `TimetableSlot`  [INFERRED]
  docs/MATHS.md → backend/app/domain/entities.py
- `5.1 Initials Value Object Invariant` --references--> `InvariantViolation`  [INFERRED]
  docs/MATHS.md → backend/app/domain/errors.py
- `Persistence` --references--> `UnitOfWork`  [INFERRED]
  prompts/02-domain-model.md → backend/app/domain/repositories.py

## Import Cycles
- None detected.

## Communities (141 total, 29 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.20
Nodes (15): split_co_teachers(), tokenize_cell(), CsvTimetableParser, _get_col(), _parse_clock_time(), _adjust_hour(), normalize_weekday(), parse_time_range() (+7 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 3 - "Event"
Cohesion: 0.14
Nodes (21): generate_vcalendar_ics(), CheckClashesUseCase, CreateEventUseCase, GetCalendarEventsUseCase, UpdateEventUseCase, ReminderPlanner, Event, EventAttendee (+13 more)

### Community 4 - "get_settings"
Cohesion: 0.14
Nodes (6): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_settings(), Settings

### Community 5 - "UUID"
Cohesion: 0.04
Nodes (16): Holiday, PushSubscription, AcademicTermRepository, AuditLogRepository, CircularRepository, DepartmentRepository, EventRepository, FacultyProfileRepository (+8 more)

### Community 7 - "SqlAlchemyUnitOfWork"
Cohesion: 0.18
Nodes (11): MaterialiseTimetableEventsUseCase, materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation(), process_circular_upload(), _run_process_circular(), dispatch_due_notifications(), recover_stale_sending_notifications() (+3 more)

### Community 8 - "db/repositories.py"
Cohesion: 0.23
Nodes (15): Base, AuditLogModel, DepartmentModel, EventAttendeeModel, EventModel, FacultyProfileModel, HolidayModel, PushSubscriptionModel (+7 more)

### Community 9 - "main.py"
Cohesion: 0.06
Nodes (12): upgrade(), upgrade(), upgrade(), upgrade(), upgrade(), configure_logging(), RequestIdMiddleware, domain_exception_handler() (+4 more)

### Community 10 - "UnitOfWork"
Cohesion: 0.07
Nodes (5): rotate_ics_token(), RotateIcsTokenUseCase, ConfirmCircularUseCase, DeletePushSubscriptionUseCase, UnitOfWork

### Community 11 - "Principal"
Cohesion: 0.13
Nodes (16): update_faculty(), get_timetable_upload(), CreateFacultyUseCase, DeactivateFacultyUseCase, ManageTermsUseCase, UpdateFacultyUseCase, AuthorisationPolicy, Principal (+8 more)

### Community 12 - "calendar.py"
Cohesion: 0.08
Nodes (24): get_clock(), get_current_principal(), get_rate_limiter(), get_redis(), get_uow(), require_admin(), require_hod_or_admin(), CalendarEventResponse (+16 more)

### Community 13 - "auth.py"
Cohesion: 0.10
Nodes (24): AcademicTermResponse, add_holiday(), bulk_import_faculty(), bulk_import_holidays(), BulkImportResponse, create_faculty(), create_term(), CreateAcademicTermRequest (+16 more)

### Community 15 - "Task"
Cohesion: 0.15
Nodes (4): Task, TaskRepository, task_to_domain(), TaskRepositoryImpl

### Community 16 - "Stage 05: Calendar core, recurrence, clash detection, ICS feed"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 05: Calendar core, recurrence, clash detection, ICS feed, Tests

### Community 17 - "auth.py"
Cohesion: 0.05
Nodes (38): change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest, LoginResponse (+30 more)

### Community 18 - "UUID"
Cohesion: 0.11
Nodes (6): TimetableSlotModel, EventRepositoryImpl, push_subscription_to_domain(), PushSubscriptionRepositoryImpl, timetable_slot_to_domain(), TimetableSlotRepositoryImpl

### Community 19 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 20 - "reminders.py"
Cohesion: 0.11
Nodes (17): delete_push_subscription(), DeletePushSubscriptionRequest, get_quiet_hours(), get_reminder_rules(), get_upcoming_notifications(), get_vapid_public_key(), PushSubscriptionRequest, PushSubscriptionResponse (+9 more)

### Community 21 - "InvariantViolation"
Cohesion: 0.17
Nodes (10): expand_slot_recurrence(), AcademicTerm, TimetableSlot, TimeSlot, test_timeslot_half_open_overlap(), test_recurrence_expansion_matching_weekday(), test_recurrence_expansion_skips_holidays(), test_recurrence_expansion_utc_roundtrip() (+2 more)

### Community 22 - "deps.py"
Cohesion: 0.08
Nodes (24): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+16 more)

### Community 23 - "Visual Companion Guide"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 24 - "Circular"
Cohesion: 0.12
Nodes (13): CircularDetailResponse, CircularUploadResponse, confirm_circular(), ConfirmCircularRequest, ConfirmCircularResponse, get_circular(), list_review_queue(), reject_circular() (+5 more)

### Community 25 - "AcademicTermRepositoryImpl"
Cohesion: 0.31
Nodes (4): AcademicTermModel, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 26 - "demo_setup.py"
Cohesion: 0.12
Nodes (8): is_server_ready(), main(), main(), http_get_json(), http_post_json(), http_post_multipart(), run_demo_setup(), main()

### Community 28 - "circulars/use_cases.py"
Cohesion: 0.05
Nodes (53): compute_lateness_percentiles(), ProcessCircularUseCase, UploadCircularUseCase, ValidationError, detect_mime_and_extension(), validate_upload_content(), detect_probable_duplicate(), normalize_title() (+45 more)

### Community 29 - "assign_task"
Cohesion: 0.17
Nodes (8): assign_task(), AssignTaskRequest, complete_task(), get_task(), list_tasks(), reopen_task(), TaskResponse, ReopenTaskUseCase

### Community 30 - "Systematic Debugging"
Cohesion: 0.10
Nodes (19): Browser Events Format, Cards (visual designs), Cleaning Up, CSS Classes Available, Design Tips, File Naming, How It Works, Mock elements (wireframe building blocks) (+11 more)

### Community 31 - "RefreshToken"
Cohesion: 0.10
Nodes (19): Bulletproofing Elements, Creation Log: Systematic Debugging Skill, Enhancement 1: TDD Reference, Extraction Decisions, Final Outcome, Initial Version, Iterations, Key Insight (+11 more)

### Community 32 - "components.json"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 33 - "Domain (backend/app/domain)"
Cohesion: 0.41
Nodes (10): DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged, TimetableConfirmed, Domain (backend/app/domain) (+2 more)

### Community 34 - "InvariantViolation"
Cohesion: 0.12
Nodes (8): InvariantViolation, Initials, test_event_invariants(), test_initials_invalid_property(), test_initials_valid_property(), test_notification_state_machine_exhaustive(), test_task_invariants(), test_timeslot_invariants()

### Community 36 - "ScheduledNotification"
Cohesion: 0.09
Nodes (22): 1. Problem and users, 3. Architecture, 4.10 Reminder Dispatch and Exactly-Once Delivery Sequence, 4.11 Meeting Circular Scanning, Extraction, and Review Sequence, 4.11 Task Assignment, Alert Lifecycle and Escalation Sequence, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine (+14 more)

### Community 37 - "reminders/maths.py"
Cohesion: 0.28
Nodes (6): compute_backoff_delay(), compute_fire_time(), compute_idempotency_key(), test_backoff_bounds(), test_fire_time_computation(), test_idempotency_key_deterministic()

### Community 38 - "compute_priority_score"
Cohesion: 0.19
Nodes (13): compute_lead_alert_times(), compute_overdue_alert_times(), compute_priority_score(), test_completed_task_priority(), test_completion_rate(), test_lead_alert_times(), test_overdue_alert_times(), test_priority_bounds_property_active() (+5 more)

### Community 40 - "ReminderRuleRepositoryImpl"
Cohesion: 0.31
Nodes (4): ReminderRule, ReminderRuleModel, reminder_rule_to_domain(), ReminderRuleRepositoryImpl

### Community 41 - "calendar/__init__.py"
Cohesion: 0.12
Nodes (17): Interval, intervals_overlap(), pairwise_clashes(), SweepLineClashDetector, BusyInterval, FreeSlotFinder, merge_busy_intervals(), FindFreeSlotsUseCase (+9 more)

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

### Community 47 - "SqlAlchemyUnitOfWork"
Cohesion: 0.08
Nodes (19): FrozenClock, SystemClock, get_db(), Department, SqlAlchemyUnitOfWork, _run_schedule_daily_overdue_alerts(), _run_schedule_hod_escalations(), InMemoryStorageService (+11 more)

### Community 48 - "FacultyProfile"
Cohesion: 0.08
Nodes (20): ReminderDispatcher, FacultyProfile, ScheduledNotification, User, NotificationChannel, Role, NotificationPayload, Notifier (+12 more)

### Community 49 - "Section"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 50 - "upload_timetable"
Cohesion: 0.16
Nodes (7): confirm_timetable(), ConfirmTimetableResponse, get_faculty_slots(), TimetableSlotResponse, TimetableUploadDetailResponse, upload_timetable(), UploadTimetableResponse

### Community 51 - "Section"
Cohesion: 0.26
Nodes (5): Section, SectionRepository, SectionModel, section_to_domain(), SectionRepositoryImpl

### Community 52 - "tasks/use_cases.py"
Cohesion: 0.24
Nodes (9): compute_completion_rate(), AssignmentProgress, CompleteTaskUseCase, FacultyOverdueSummary, GetHodDashboardUseCase, HodDashboardData, ListTasksUseCase, TaskWithScore (+1 more)

### Community 53 - "metrics.py"
Cohesion: 0.19
Nodes (6): AdminMetricsResponse, DeadLetterResponse, get_system_metrics(), LatenessPercentilesResponse, QueueDepthResponse, retry_failed_notification()

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
Cohesion: 0.24
Nodes (5): Course, CourseRepository, CourseModel, course_to_domain(), CourseRepositoryImpl

### Community 58 - "EntityNotFound"
Cohesion: 0.11
Nodes (4): get_ics_feed(), GenerateIcsFeedUseCase, DomainError, EntityNotFound

### Community 59 - "Web Application Testing"
Cohesion: 0.15
Nodes (13): devDependencies, eslint, eslint-config-next, openapi-typescript, @playwright/test, prettier, prettier-plugin-tailwindcss, tailwindcss (+5 more)

### Community 60 - "10. Security Limits"
Cohesion: 0.50
Nodes (4): 10.1 Token Lifetimes, Rotation, and Family Reuse Detection, 10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix, 10.3 Sliding Window Log Rate Limiting, 10. Security Limits

### Community 61 - "NotificationRepositoryImpl"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 62 - "reminders/use_cases.py"
Cohesion: 0.14
Nodes (6): GetUpcomingNotificationsUseCase, GetUserQuietHoursUseCase, GetUserReminderRulesUseCase, RegisterPushSubscriptionUseCase, UpdateReminderRuleUseCase, UpdateUserQuietHoursUseCase

### Community 63 - "Circular"
Cohesion: 0.05
Nodes (23): Circular, TimetableUpload, InvalidTransition, TimetableUploadRepository, timetable_upload_to_domain(), TimetableUploadRepositoryImpl, test_circular_state_machine_exhaustive(), 1.3 State Machine Transition Algebras (+15 more)

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

### Community 69 - "Stage 03: Authentication, authorization, and faculty directory"
Cohesion: 0.29
Nodes (4): BackupService, backup_database_to_minio(), test_backup_prune_expired(), test_backup_prune_preserves_single_expired_backup()

### Community 70 - "FacultyDesk Maths"
Cohesion: 0.10
Nodes (19): 11.1 Dispatch Lateness Percentile Computation, 11.2 Backup Retention Arithmetic & Bounded Pruning, 11.3 Upload Decompression Bomb and Page Count Limits, 11. Hardening, Observability and Reliability, 1.2 Half-Open Interval Invariant and Overlap Arithmetic, 1. Time and Recurrence, 4.1 Deterministic Idempotency Key Derivation, 4.2 Distributed Dispatch via Skip-Locked Batch Claiming (+11 more)

### Community 71 - "directory/page.tsx"
Cohesion: 0.09
Nodes (36): nextConfig, CalendarPage(), CircularsPage(), DirectoryPage(), metadata, RootLayout(), viewport, LoginPage() (+28 more)

### Community 72 - "Graphify Protocol"
Cohesion: 0.25
Nodes (7): Best Practices, Common Pitfall, Decision Tree: Choosing Your Approach, Example: Using with_server.py, Reconnaissance-Then-Action Pattern, Reference Files, Web Application Testing

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

### Community 79 - "test_initials_matching.py"
Cohesion: 0.25
Nodes (8): InitialsResolver, normalized_similarity(), ResolutionOutcome, test_ambiguity_threshold_rejection(), test_cell_tokenization_topologies(), test_exact_and_alias_resolution(), test_normalized_similarity_properties(), 5.3 Initials Resolution via Normalized Levenshtein Distance

### Community 80 - "TaskTemplate"
Cohesion: 0.18
Nodes (8): TaskTemplate, TaskTemplateRepository, TaskCategory, TaskTemplateModel, task_template_to_domain(), TaskTemplateRepositoryImpl, main(), seed_database()

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

### Community 91 - "MinioStorageService"
Cohesion: 0.17
Nodes (6): get_storage(), ParseTimetableUseCase, get_storage_service(), MinioStorageService, process_timetable_upload(), _run_parse()

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

### Community 135 - "bulk_import.py"
Cohesion: 0.29
Nodes (3): BulkImportFacultyUseCase, BulkImportReport, RowImportResult

### Community 139 - "QuietHours"
Cohesion: 0.29
Nodes (7): adjust_for_quiet_hours(), QuietHours, test_quiet_hours_midnight_crossing(), test_quiet_hours_table(), 3.1 Fire Time and Lead-Time Computation, 3.2 Quiet Hours Shift with Midnight-Crossing Window, 3. Reminder Scheduling

### Community 140 - "test_parsers.py"
Cohesion: 0.61
Nodes (6): TimetableParserFactory, test_csv_timetable_parsing(), test_pdf_text_timetable_parsing(), test_xlsx_co_teachers_parsing(), test_xlsx_merged_cell_period_expansion(), test_xlsx_standard_timetable_parsing()

### Community 144 - "CircularRepositoryImpl"
Cohesion: 0.48
Nodes (3): CircularModel, circular_to_domain(), CircularRepositoryImpl

### Community 146 - "tasks.py"
Cohesion: 0.15
Nodes (13): AssignmentProgressResponse, CreateTaskRequest, ensure_utc(), FacultyOverdueSummaryResponse, get_hod_dashboard(), HodDashboardResponse, list_templates(), TaskTemplateResponse (+5 more)

### Community 148 - "Stage 06: Reminder engine with exactly-once delivery"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 06: Reminder engine with exactly-once delivery, Tests

### Community 149 - "Clock"
Cohesion: 0.09
Nodes (14): Backend Engineer, Responsibilities, Standards you are held to, Working method, CancelEventUseCase, AssignTaskUseCase, Clock, FacultyDesk Decisions (+6 more)

### Community 154 - "5. Initials and Name Matching"
Cohesion: 0.40
Nodes (5): 5.1 Initials Value Object Invariant, 5.2 Timetable Cell Tokenization Grammar, 5.4 Merged-Cell Period Expansion, 5.5 Header Day and Time Normalization, 5. Initials and Name Matching

### Community 155 - "OCR and Parsing Engineer"
Cohesion: 0.50
Nodes (3): OCR and Parsing Engineer, Responsibilities, Rules

## Knowledge Gaps
- **22 isolated node(s):** `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 847 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `Event`, `get_settings`, `UUID`, `SqlAlchemyUnitOfWork`, `bulk_import.py`, `Principal`, `calendar.py`, `auth.py`, `delete_task`, `auth.py`, `tasks.py`, `reminders.py`, `Clock`, `InvariantViolation`, `Circular`, `create_task`, `circulars/use_cases.py`, `assign_task`, `Domain (backend/app/domain)`, `calendar/__init__.py`, `SqlAlchemyUnitOfWork`, `FacultyProfile`, `upload_timetable`, `tasks/use_cases.py`, `metrics.py`, `EntityNotFound`, `reminders/use_cases.py`, `Stage 07: Meeting circular scanning, extraction and review queue`, `MinioStorageService`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 52 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._
- **Why does `Event` connect `Event` to `Domain (backend/app/domain)`, `InvariantViolation`, `UUID`, `SqlAlchemyUnitOfWork`, `datetime`, `UnitOfWork`, `calendar.py`, `SqlAlchemyUnitOfWork`, `FacultyProfile`, `UUID`, `tasks/use_cases.py`, `InvariantViolation`, `EntityNotFound`, `create_task`, `circulars/use_cases.py`, `NotificationRepositoryImpl`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Clock` (e.g. with `Standards you are held to` and `Non-negotiables`) actually correct?**
  _`Clock` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Should `Event` be split into smaller, more focused modules?**
  _Cohesion score 0.1388235294117647 - nodes in this community are weakly interconnected._