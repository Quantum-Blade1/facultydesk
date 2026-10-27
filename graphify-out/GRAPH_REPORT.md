# Graph Report - facultydesk  (2026-10-28)

## Corpus Check
- 233 files · ~206,395 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: (none) 10, .csv 2, .example 1)

## Summary
- 2282 nodes · 6616 edges · 145 communities (116 shown, 29 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 992 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `71a5873f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- server.cjs
- Department
- Event
- get_settings
- UUID
- User
- SqlAlchemyUnitOfWork
- db/repositories.py
- calendar/__init__.py
- UnitOfWork
- Principal
- calendar.py
- auth.py
- core/errors.py
- Task
- Principal
- auth.py
- reminders.py
- Test-Driven Development (TDD)
- reminders.py
- AcademicTerm
- deps.py
- Visual Companion Guide
- Circular
- AcademicTermRepositoryImpl
- logging.py
- directory.py
- extractor.py
- tasks.py
- Systematic Debugging
- RefreshToken
- components.json
- Domain (backend/app/domain)
- test_hardening.py
- AsyncSession
- ScheduledNotification
- Root Cause Tracing
- FacultyDesk Decisions
- ScheduledNotification
- ReminderRuleRepositoryImpl
- domain/__init__.py
- Root Cause Tracing
- Defense-in-Depth Validation
- manifest.json
- devDependencies
- Brainstorming
- FrozenClock
- FacultyProfile
- Section
- upload_timetable
- Section
- entities.py
- metrics.py
- Room
- helper.js
- Brainstorming
- domain/__init__.py
- TimetableUpload
- Web Application Testing
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- NotificationRepositoryImpl
- reminders/use_cases.py
- Circular
- celery_app.py
- FacultyDesk Agent Contract
- Trusted External Skills
- stop-server.sh
- helper.js
- circular_tasks.py
- 10. Security Limits
- directory/page.tsx
- Graphify Protocol
- Stage 07: Meeting circular scanning, extraction and review queue
- Stage 08: Documentation tasks, priority scoring and alerts
- Code Quality Bar
- stop-server.sh
- Build Loop
- InvariantViolation
- TaskTemplateRepositoryImpl
- ._transition
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- Stage 06: Reminder engine with exactly-once delivery
- Stage 10: Security, reliability and observability hardening
- Build Loop
- Math First
- 11. Hardening, Observability and Reliability
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
- ocr/__init__.py
- builder-check-prompt.md
- task-done
- Kickoff prompt (paste this into the Antigravity agent)
- ooad-diagrams/SKILL.md
- 1.3 State Machine Transition Algebras
- engine.py
- test-academic.md
- api/__init__.py
- application/__init__.py
- find-polluter.sh
- infrastructure/__init__.py
- seed/__init__.py
- PushSubscription
- NotificationRepositoryImpl
- test_ocr_maths.py
- facultydesk-backend
- RefreshToken
- generate_sample_circulars.py
- duplicate_detector.py
- CircularRepositoryImpl
- Stage 07: Meeting circular scanning, extraction and review queue
- Stage 06: Reminder engine with exactly-once delivery
- Backend Engineer

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

## Communities (145 total, 29 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.06
Nodes (42): OCR and Parsing Engineer, Responsibilities, Rules, split_co_teachers(), tokenize_cell(), CsvTimetableParser, _get_col(), _parse_clock_time() (+34 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 3 - "Event"
Cohesion: 0.12
Nodes (27): generate_vcalendar_ics(), CancelEventUseCase, CheckClashesUseCase, CreateEventUseCase, GenerateIcsFeedUseCase, GetCalendarEventsUseCase, MaterialiseTimetableEventsUseCase, RotateIcsTokenUseCase (+19 more)

### Community 4 - "get_settings"
Cohesion: 0.15
Nodes (6): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_settings(), Settings

### Community 6 - "User"
Cohesion: 0.10
Nodes (10): ReminderDispatcher, NotificationPayload, Notifier, EmailNotifier, CompositeNotifier, WebPushNotifier, _build_dispatcher(), _run_dispatch() (+2 more)

### Community 7 - "SqlAlchemyUnitOfWork"
Cohesion: 0.25
Nodes (10): SystemClock, materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation(), dispatch_due_notifications(), recover_stale_sending_notifications(), _run_schedule_daily_overdue_alerts(), _run_schedule_hod_escalations() (+2 more)

### Community 8 - "db/repositories.py"
Cohesion: 0.27
Nodes (15): Base, CircularModel, CourseModel, DepartmentModel, EventAttendeeModel, EventModel, FacultyProfileModel, HolidayModel (+7 more)

### Community 9 - "calendar/__init__.py"
Cohesion: 0.07
Nodes (23): upgrade(), upgrade(), upgrade(), upgrade(), upgrade(), Interval, intervals_overlap(), pairwise_clashes() (+15 more)

### Community 10 - "UnitOfWork"
Cohesion: 0.08
Nodes (3): delete_push_subscription(), DeletePushSubscriptionUseCase, UnitOfWork

### Community 11 - "Principal"
Cohesion: 0.11
Nodes (16): BulkImportFacultyUseCase, BulkImportReport, RowImportResult, CreateFacultyUseCase, ManageTermsUseCase, UpdateFacultyUseCase, AuthorisationPolicy, Principal (+8 more)

### Community 12 - "calendar.py"
Cohesion: 0.11
Nodes (16): CalendarEventResponse, cancel_calendar_event(), check_event_clashes(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots() (+8 more)

### Community 13 - "auth.py"
Cohesion: 0.08
Nodes (21): AcademicTermResponse, add_holiday(), bulk_import_faculty(), bulk_import_holidays(), BulkImportResponse, create_faculty(), create_term(), CreateAcademicTermRequest (+13 more)

### Community 14 - "core/errors.py"
Cohesion: 0.08
Nodes (10): FacultyDeskError, InvalidTransition, RateLimitExceededError, get_redis_client(), RedisSlidingWindowRateLimiter, domain_exception_handler(), healthz(), lifespan() (+2 more)

### Community 15 - "Task"
Cohesion: 0.14
Nodes (4): Task, TaskRepository, task_to_domain(), TaskRepositoryImpl

### Community 16 - "Principal"
Cohesion: 0.13
Nodes (14): 4.1 Deterministic Idempotency Key Derivation, 4.2 Distributed Dispatch via Skip-Locked Batch Claiming, 4.3 Stale SENDING Recovery and Failure Window Bound, 4.4 Maximum Lateness Bound, 4. Exactly-Once Delivery, 7.1 Formal Time Grammar and Assumed Duration Invariant, 7.2 Date Extraction with Cue Words and Timezone Anchoring, 7. Date and Time Extraction (+6 more)

### Community 17 - "auth.py"
Cohesion: 0.08
Nodes (30): change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest, LoginResponse (+22 more)

### Community 18 - "reminders.py"
Cohesion: 0.14
Nodes (4): EventRepositoryImpl, faculty_profile_to_domain(), FacultyProfileRepositoryImpl, TimetableSlotRepositoryImpl

### Community 19 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 20 - "reminders.py"
Cohesion: 0.13
Nodes (16): DeletePushSubscriptionRequest, get_quiet_hours(), get_reminder_rules(), get_upcoming_notifications(), get_vapid_public_key(), PushSubscriptionRequest, PushSubscriptionResponse, QuietHoursResponse (+8 more)

### Community 21 - "AcademicTerm"
Cohesion: 0.13
Nodes (16): expand_slot_recurrence(), TimetableSlot, TimeSlot, timetable_slot_to_domain(), test_timeslot_half_open_overlap(), test_recurrence_expansion_matching_weekday(), test_recurrence_expansion_skips_holidays(), test_recurrence_expansion_utc_roundtrip() (+8 more)

### Community 22 - "deps.py"
Cohesion: 0.08
Nodes (24): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+16 more)

### Community 23 - "Visual Companion Guide"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 24 - "Circular"
Cohesion: 0.08
Nodes (17): CircularDetailResponse, CircularUploadResponse, confirm_circular(), ConfirmCircularRequest, ConfirmCircularResponse, get_circular(), list_review_queue(), reject_circular() (+9 more)

### Community 25 - "AcademicTermRepositoryImpl"
Cohesion: 0.31
Nodes (4): AcademicTermModel, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 26 - "logging.py"
Cohesion: 0.12
Nodes (6): is_server_ready(), main(), configure_logging(), RequestIdMiddleware, main(), main()

### Community 27 - "directory.py"
Cohesion: 0.25
Nodes (9): get_clock(), get_current_principal(), get_rate_limiter(), get_storage(), get_uow(), require_admin(), require_hod_or_admin(), DepartmentResponse (+1 more)

### Community 28 - "extractor.py"
Cohesion: 0.24
Nodes (11): ExtractedAttendee, ExtractedTime, ExtractionResult, parse_meeting_date(), parse_meeting_time(), parse_military_time(), parse_title_and_agenda(), parse_venue() (+3 more)

### Community 29 - "tasks.py"
Cohesion: 0.05
Nodes (45): assign_task(), AssignmentProgressResponse, AssignTaskRequest, complete_task(), create_task(), CreateTaskRequest, delete_task(), ensure_utc() (+37 more)

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
Cohesion: 0.24
Nodes (11): DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged, TimetableConfirmed, test_event_reschedule() (+3 more)

### Community 34 - "test_hardening.py"
Cohesion: 0.26
Nodes (12): compute_lateness_percentiles(), ValidationError, detect_mime_and_extension(), validate_upload_content(), test_compute_lateness_percentiles_100_elements(), test_compute_lateness_percentiles_empty(), test_compute_lateness_percentiles_single(), test_detect_mime_and_extension_invalid() (+4 more)

### Community 35 - "AsyncSession"
Cohesion: 0.14
Nodes (3): AuditLogModel, audit_log_to_domain(), AuditLogRepositoryImpl

### Community 36 - "ScheduledNotification"
Cohesion: 0.10
Nodes (20): 1. Problem and users, 3. Architecture, 4.10 Reminder Dispatch and Exactly-Once Delivery Sequence, 4.11 Meeting Circular Scanning, Extraction, and Review Sequence, 4.11 Task Assignment, Alert Lifecycle and Escalation Sequence, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine (+12 more)

### Community 37 - "Root Cause Tracing"
Cohesion: 0.20
Nodes (10): adjust_for_quiet_hours(), compute_backoff_delay(), compute_fire_time(), compute_idempotency_key(), QuietHours, test_quiet_hours_midnight_crossing(), test_backoff_bounds(), test_fire_time_computation() (+2 more)

### Community 38 - "FacultyDesk Decisions"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 01: Foundation, environment, Graphify, trusted skills, Tasks

### Community 39 - "ScheduledNotification"
Cohesion: 0.10
Nodes (5): GetUpcomingNotificationsUseCase, ScheduledNotification, 3.1 Fire Time and Lead-Time Computation, 3.2 Quiet Hours Shift with Midnight-Crossing Window, 3. Reminder Scheduling

### Community 40 - "ReminderRuleRepositoryImpl"
Cohesion: 0.39
Nodes (3): ReminderRuleModel, reminder_rule_to_domain(), ReminderRuleRepositoryImpl

### Community 41 - "domain/__init__.py"
Cohesion: 0.28
Nodes (8): test_circular_state_machine_exhaustive(), test_event_invariants(), test_initials_invalid_property(), test_initials_valid_property(), test_notification_state_machine_exhaustive(), test_task_invariants(), test_timeslot_invariants(), ScheduledNotification State Machine

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

### Community 47 - "FrozenClock"
Cohesion: 0.20
Nodes (8): FrozenClock, test_clock_always_returns_utc_property(), test_frozen_clock_advance_property(), test_frozen_clock_rejects_naive_datetime(), FacultyDesk Decisions, Stage 00: Agent setup, Stage 01: Foundation, environment, Graphify, trusted skills, 1.1 Canonical Time Representation and Clock Invariant

### Community 48 - "FacultyProfile"
Cohesion: 0.13
Nodes (22): AssignTaskUseCase, get_db(), AcademicTerm, Department, FacultyProfile, User, Initials, Role (+14 more)

### Community 49 - "Section"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 50 - "upload_timetable"
Cohesion: 0.15
Nodes (8): confirm_timetable(), ConfirmTimetableResponse, get_faculty_slots(), get_timetable_upload(), TimetableSlotResponse, TimetableUploadDetailResponse, upload_timetable(), UploadTimetableResponse

### Community 51 - "Section"
Cohesion: 0.48
Nodes (3): SectionModel, section_to_domain(), SectionRepositoryImpl

### Community 52 - "entities.py"
Cohesion: 0.25
Nodes (10): EventAttendee, AttendeeResponse, CircularStatus, NotificationChannel, NotificationStatus, TaskCategory, TaskRecurrence, TaskStatus (+2 more)

### Community 53 - "metrics.py"
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

### Community 57 - "domain/__init__.py"
Cohesion: 0.06
Nodes (19): Course, RefreshToken, Section, AuditLogRepository, CircularRepository, CourseRepository, DepartmentRepository, EventRepository (+11 more)

### Community 58 - "TimetableUpload"
Cohesion: 0.12
Nodes (4): TimetableUpload, InvalidTransition, timetable_upload_to_domain(), TimetableUploadRepositoryImpl

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
Cohesion: 0.14
Nodes (6): GetUserQuietHoursUseCase, GetUserReminderRulesUseCase, RegisterPushSubscriptionUseCase, UpdateReminderRuleUseCase, UpdateUserQuietHoursUseCase, ReminderRule

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
Cohesion: 0.18
Nodes (11): scripts, build, dev, fmt, format:check, gen:api, generate:api, lint (+3 more)

### Community 68 - "helper.js"
Cohesion: 0.42
Nodes (7): connect(), nextReconnectDelay(), reloadAfterRecovery(), sessionKey(), setStatus(), showTombstone(), websocketUrl()

### Community 69 - "circular_tasks.py"
Cohesion: 0.39
Nodes (3): ProcessCircularUseCase, process_circular_upload(), _run_process_circular()

### Community 70 - "10. Security Limits"
Cohesion: 0.50
Nodes (4): 10.1 Token Lifetimes, Rotation, and Family Reuse Detection, 10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix, 10.3 Sliding Window Log Rate Limiting, 10. Security Limits

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

### Community 80 - "TaskTemplateRepositoryImpl"
Cohesion: 0.39
Nodes (3): TaskTemplateModel, task_template_to_domain(), TaskTemplateRepositoryImpl

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

### Community 87 - "11. Hardening, Observability and Reliability"
Cohesion: 0.50
Nodes (4): 11.1 Dispatch Lateness Percentile Computation, 11.2 Backup Retention Arithmetic & Bounded Pruning, 11.3 Upload Decompression Bomb and Page Count Limits, 11. Hardening, Observability and Reliability

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
Cohesion: 0.19
Nodes (5): ParseTimetableUseCase, get_storage_service(), MinioStorageService, process_timetable_upload(), _run_parse()

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

### Community 108 - "ocr/__init__.py"
Cohesion: 0.47
Nodes (5): compute_deskew_angle(), deskew_image(), has_pdf_text_layer(), preprocess_image_for_ocr(), rasterise_pdf_page()

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

### Community 114 - "engine.py"
Cohesion: 0.22
Nodes (3): OcrEngine, OcrResult, WordBox

### Community 124 - "PushSubscription"
Cohesion: 0.15
Nodes (4): PushSubscription, PushSubscriptionRepository, push_subscription_to_domain(), PushSubscriptionRepositoryImpl

### Community 131 - "test_ocr_maths.py"
Cohesion: 0.18
Nodes (13): compute_length_weighted_confidence(), CircularExtractor, test_confidence_bounds_property(), test_confidence_empty_tokens(), test_deskew_skip_sub_threshold(), test_length_weighted_document_confidence(), test_meeting_time_grammar_table(), test_review_gate_decision_matrix() (+5 more)

### Community 138 - "RefreshToken"
Cohesion: 0.18
Nodes (5): RefreshTokenModel, refresh_token_to_domain(), RefreshTokenRepositoryImpl, user_to_domain(), UserRepositoryImpl

### Community 139 - "generate_sample_circulars.py"
Cohesion: 0.39
Nodes (4): _get_font(), main(), _make_pdf_with_text(), _render_text_to_image()

### Community 145 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Corpus and tests, Goal, Maths to specify first, Pipeline, Stage 07: Meeting circular scanning, extraction and review queue

### Community 148 - "Stage 06: Reminder engine with exactly-once delivery"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 06: Reminder engine with exactly-once delivery, Tests

### Community 149 - "Backend Engineer"
Cohesion: 0.40
Nodes (4): Backend Engineer, Responsibilities, Standards you are held to, Working method

## Knowledge Gaps
- **22 isolated node(s):** `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 841 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `Event`, `get_settings`, `User`, `calendar/__init__.py`, `Principal`, `calendar.py`, `auth.py`, `auth.py`, `reminders.py`, `Circular`, `directory.py`, `tasks.py`, `Domain (backend/app/domain)`, `Root Cause Tracing`, `ScheduledNotification`, `FacultyProfile`, `upload_timetable`, `entities.py`, `metrics.py`, `domain/__init__.py`, `reminders/use_cases.py`, `Circular`, `circular_tasks.py`, `Stage 07: Meeting circular scanning, extraction and review queue`, `MinioStorageService`, `ocr/__init__.py`, `engine.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 52 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `datetime` be split into smaller, more focused modules?**
  _Cohesion score 0.05934242181234964 - nodes in this community are weakly interconnected._
- **Why does `Event` connect `Event` to `Domain (backend/app/domain)`, `test_ocr_maths.py`, `UUID`, `domain/__init__.py`, `ocr/__init__.py`, `calendar.py`, `duplicate_detector.py`, `InvariantViolation`, `FacultyProfile`, `reminders.py`, `entities.py`, `domain/__init__.py`, `tasks.py`, `NotificationRepositoryImpl`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Clock` (e.g. with `Standards you are held to` and `Non-negotiables`) actually correct?**
  _`Clock` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._