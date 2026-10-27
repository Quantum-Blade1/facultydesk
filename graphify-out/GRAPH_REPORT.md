# Graph Report - facultydesk  (2026-10-28)

## Corpus Check
- 225 files · ~196,919 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: (none) 10, .csv 2, .example 1)

## Summary
- 2223 nodes · 6276 edges · 162 communities (115 shown, 47 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 874 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a209b577`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- server.cjs
- Department
- test_calendar_full_pipeline
- get_settings
- User
- SqlAlchemyUnitOfWork
- db/repositories.py
- sqlalchemy
- UnitOfWork
- Principal
- calendar.py
- auth.py
- main.py
- clash_detector.py
- Principal
- auth.py
- reminders.py
- Test-Driven Development (TDD)
- reminders.py
- AcademicTerm
- deps.py
- Visual Companion Guide
- Circular
- Holiday
- with_server.py
- Event
- extractor.py
- tasks.py
- Systematic Debugging
- RefreshToken
- components.json
- Domain (backend/app/domain)
- tasks/use_cases.py
- AsyncSession
- ScheduledNotification
- Root Cause Tracing
- FacultyDesk Decisions
- NotificationRepository
- ReminderRule
- domain/__init__.py
- Root Cause Tracing
- Defense-in-Depth Validation
- manifest.json
- devDependencies
- Brainstorming
- FrozenClock
- Role
- Section
- zoneinfo
- Section
- entities.py
- Course
- Room
- helper.js
- Brainstorming
- domain/__init__.py
- TimetableUpload
- Web Application Testing
- Stage 05: Calendar core, recurrence, clash detection, ICS feed
- NotificationRepositoryImpl
- reminders/use_cases.py
- compute_priority_score
- timetable_tasks.py
- FacultyDesk Agent Contract
- Trusted External Skills
- stop-server.sh
- helper.js
- EventRepository
- FacultyProfile
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
- Frontend Engineer
- Math Verifier
- Orchestrator
- deps.py
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
- ScheduledNotification
- engine.py
- test-academic.md
- api/__init__.py
- application/__init__.py
- find-polluter.sh
- infrastructure/__init__.py
- seed/__init__.py
- .__aenter__
- NotificationRepositoryImpl
- test_ocr_maths.py
- QuietHours
- facultydesk-backend
- RefreshToken
- generate_sample_circulars.py
- FacultyProfileRepositoryImpl
- delete_push_subscription
- duplicate_detector.py
- delete_task
- CircularRepositoryImpl
- Stage 07: Meeting circular scanning, extraction and review queue
- timetable_upload_to_domain
- UserRepositoryImpl
- Stage 06: Reminder engine with exactly-once delivery
- Backend Engineer
- test_clock.py
- get_ics_feed
- test_reschedule_and_cancel_lifecycle

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 177 edges
2. `Clock` - 108 edges
3. `Principal` - 92 edges
4. `FacultyProfile` - 77 edges
5. `ScheduledNotification` - 72 edges
6. `Event` - 67 edges
7. `User` - 62 edges
8. `NotFoundError` - 54 edges
9. `InvariantViolation` - 51 edges
10. `SqlAlchemyUnitOfWork` - 49 edges

## Surprising Connections (you probably didn't know these)
- `Persistence` --references--> `UnitOfWork`  [INFERRED]
  prompts/02-domain-model.md → backend/app/domain/repositories.py
- `Standards you are held to` --references--> `Clock`  [INFERRED]
  .agents/agents/backend-engineer.md → backend/app/core/clock.py
- `Non-negotiables` --references--> `Clock`  [INFERRED]
  AGENTS.md → backend/app/core/clock.py
- `10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix` --references--> `AuthorisationPolicy`  [INFERRED]
  docs/MATHS.md → backend/app/application/security/policy.py
- `5.4 Merged-Cell Period Expansion` --references--> `TimetableSlot`  [INFERRED]
  docs/MATHS.md → backend/app/domain/entities.py

## Import Cycles
- None detected.

## Communities (162 total, 47 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.13
Nodes (26): OCR and Parsing Engineer, Responsibilities, Rules, split_co_teachers(), tokenize_cell(), CsvTimetableParser, _get_col(), _parse_clock_time() (+18 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 2 - "Department"
Cohesion: 0.42
Nodes (4): Department, department_to_domain(), DepartmentRepositoryImpl, test_round_trip_all_aggregates()

### Community 3 - "test_calendar_full_pipeline"
Cohesion: 0.17
Nodes (10): CheckClashesUseCase, GenerateIcsFeedUseCase, GetCalendarEventsUseCase, RotateIcsTokenUseCase, UpdateEventUseCase, ClashDetectedError, ConflictError, DomainError (+2 more)

### Community 4 - "get_settings"
Cohesion: 0.16
Nodes (7): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_settings(), Settings, get_db()

### Community 6 - "User"
Cohesion: 0.12
Nodes (10): ReminderDispatcher, User, NotificationPayload, Notifier, EmailNotifier, CompositeNotifier, WebPushNotifier, _build_dispatcher() (+2 more)

### Community 7 - "SqlAlchemyUnitOfWork"
Cohesion: 0.17
Nodes (15): SystemClock, SqlAlchemyUnitOfWork, materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation(), process_circular_upload(), _run_process_circular(), dispatch_due_notifications() (+7 more)

### Community 8 - "db/repositories.py"
Cohesion: 0.24
Nodes (20): Base, AcademicTermModel, AuditLogModel, CircularModel, CourseModel, DepartmentModel, EventAttendeeModel, EventModel (+12 more)

### Community 9 - "sqlalchemy"
Cohesion: 0.14
Nodes (6): upgrade(), upgrade(), upgrade(), upgrade(), upgrade(), cleanup_db_connections()

### Community 11 - "Principal"
Cohesion: 0.13
Nodes (20): get_faculty_slots(), get_timetable_upload(), BulkImportFacultyUseCase, BulkImportReport, RowImportResult, CreateFacultyUseCase, DeactivateFacultyUseCase, ManageTermsUseCase (+12 more)

### Community 12 - "calendar.py"
Cohesion: 0.13
Nodes (14): CalendarEventResponse, cancel_calendar_event(), check_event_clashes(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots() (+6 more)

### Community 13 - "auth.py"
Cohesion: 0.07
Nodes (30): get_clock(), get_current_principal(), get_uow(), require_admin(), require_hod_or_admin(), AcademicTermResponse, add_holiday(), bulk_import_faculty() (+22 more)

### Community 14 - "main.py"
Cohesion: 0.09
Nodes (6): configure_logging(), RequestIdMiddleware, domain_exception_handler(), healthz(), lifespan(), readyz()

### Community 15 - "clash_detector.py"
Cohesion: 0.33
Nodes (8): Interval, intervals_overlap(), pairwise_clashes(), SweepLineClashDetector, test_adjacent_intervals_no_clash(), test_sweep_line_clash_detection_matches_pairwise_property(), test_worked_example_from_maths_md(), 2.2 Sweep-Line Interval Clash Detection Algorithm

### Community 16 - "Principal"
Cohesion: 0.08
Nodes (24): test_meeting_time_grammar_table(), 10.1 Token Lifetimes, Rotation, and Family Reuse Detection, 10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix, 10.3 Sliding Window Log Rate Limiting, 10. Security Limits, 4.1 Deterministic Idempotency Key Derivation, 4.2 Distributed Dispatch via Skip-Locked Batch Claiming, 4.3 Stale SENDING Recovery and Failure Window Bound (+16 more)

### Community 17 - "auth.py"
Cohesion: 0.07
Nodes (37): get_rate_limiter(), change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest (+29 more)

### Community 18 - "reminders.py"
Cohesion: 0.16
Nodes (4): event_to_domain(), EventRepositoryImpl, timetable_slot_to_domain(), TimetableSlotRepositoryImpl

### Community 19 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 20 - "reminders.py"
Cohesion: 0.13
Nodes (16): DeletePushSubscriptionRequest, get_quiet_hours(), get_reminder_rules(), get_upcoming_notifications(), get_vapid_public_key(), PushSubscriptionRequest, PushSubscriptionResponse, QuietHoursResponse (+8 more)

### Community 21 - "AcademicTerm"
Cohesion: 0.14
Nodes (13): expand_slot_recurrence(), AcademicTerm, TimetableSlot, TimeSlot, test_timeslot_half_open_overlap(), test_recurrence_expansion_matching_weekday(), test_recurrence_expansion_skips_holidays(), test_recurrence_expansion_utc_roundtrip() (+5 more)

### Community 22 - "deps.py"
Cohesion: 0.08
Nodes (24): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+16 more)

### Community 23 - "Visual Companion Guide"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 24 - "Circular"
Cohesion: 0.09
Nodes (17): CircularDetailResponse, CircularUploadResponse, confirm_circular(), ConfirmCircularRequest, ConfirmCircularResponse, get_circular(), list_review_queue(), reject_circular() (+9 more)

### Community 25 - "Holiday"
Cohesion: 0.12
Nodes (5): Holiday, AcademicTermRepository, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 27 - "Event"
Cohesion: 0.22
Nodes (13): generate_vcalendar_ics(), CreateEventUseCase, MaterialiseTimetableEventsUseCase, ConfirmCircularUseCase, ReminderPlanner, Event, EventKind, EventSource (+5 more)

### Community 28 - "extractor.py"
Cohesion: 0.20
Nodes (13): CircularExtractor, ExtractedAttendee, ExtractedTime, ExtractionResult, parse_meeting_date(), parse_meeting_time(), parse_military_time(), parse_title_and_agenda() (+5 more)

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

### Community 33 - "Domain (backend/app/domain)"
Cohesion: 0.41
Nodes (10): DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged, TimetableConfirmed, Domain (backend/app/domain) (+2 more)

### Community 34 - "tasks/use_cases.py"
Cohesion: 0.19
Nodes (16): compute_completion_rate(), AssignmentProgress, AssignTaskUseCase, CompleteTaskUseCase, CreateTaskUseCase, FacultyOverdueSummary, GetHodDashboardUseCase, HodDashboardData (+8 more)

### Community 36 - "ScheduledNotification"
Cohesion: 0.10
Nodes (20): 1. Problem and users, 3. Architecture, 4.10 Reminder Dispatch and Exactly-Once Delivery Sequence, 4.11 Meeting Circular Scanning, Extraction, and Review Sequence, 4.11 Task Assignment, Alert Lifecycle and Escalation Sequence, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine (+12 more)

### Community 37 - "Root Cause Tracing"
Cohesion: 0.26
Nodes (7): compute_backoff_delay(), compute_fire_time(), compute_idempotency_key(), NotificationChannel, test_backoff_bounds(), test_fire_time_computation(), test_idempotency_key_deterministic()

### Community 38 - "FacultyDesk Decisions"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 01: Foundation, environment, Graphify, trusted skills, Tasks

### Community 40 - "ReminderRule"
Cohesion: 0.17
Nodes (7): GetUserReminderRulesUseCase, ReminderRule, reminder_rule_to_domain(), ReminderRuleRepositoryImpl, 3.1 Fire Time and Lead-Time Computation, 3.2 Quiet Hours Shift with Midnight-Crossing Window, 3. Reminder Scheduling

### Community 41 - "domain/__init__.py"
Cohesion: 0.19
Nodes (10): Initials, test_bulk_import_from_sample_csv(), test_circular_state_machine_exhaustive(), test_event_invariants(), test_initials_invalid_property(), test_initials_valid_property(), test_notification_state_machine_exhaustive(), test_task_invariants() (+2 more)

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
Cohesion: 0.29
Nodes (3): FrozenClock, test_frozen_clock_advance_property(), 2. Features that exist now

### Community 48 - "Role"
Cohesion: 0.25
Nodes (4): Role, InMemoryStorageService, sample_dir(), test_circular_full_pipeline_with_samples()

### Community 49 - "Section"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 50 - "zoneinfo"
Cohesion: 0.18
Nodes (9): BusyInterval, FreeSlotFinder, merge_busy_intervals(), FindFreeSlotsUseCase, test_free_slots_never_intersect_busy_property(), test_free_slots_worked_example(), 2.1 Half-Open Overlap Predicate, 2.3 Multi-Attendee Common Free-Slot Finder (+1 more)

### Community 51 - "Section"
Cohesion: 0.43
Nodes (3): Section, section_to_domain(), SectionRepositoryImpl

### Community 52 - "entities.py"
Cohesion: 0.15
Nodes (11): EventAttendee, Task, AttendeeResponse, CircularStatus, NotificationStatus, TaskCategory, TaskRecurrence, TaskStatus (+3 more)

### Community 53 - "Course"
Cohesion: 0.43
Nodes (3): Course, course_to_domain(), CourseRepositoryImpl

### Community 54 - "Room"
Cohesion: 0.43
Nodes (3): Room, room_to_domain(), RoomRepositoryImpl

### Community 55 - "helper.js"
Cohesion: 0.17
Nodes (11): Applying the Pattern, Defense-in-Depth Validation, Example from Session, Key Insight, Layer 1: Entry Point Validation, Layer 2: Business Logic Validation, Layer 3: Environment Guards, Layer 4: Debug Instrumentation (+3 more)

### Community 56 - "Brainstorming"
Cohesion: 0.17
Nodes (11): Execution Handoff, File Structure, Overview, Plan Document Header, Scope Check, Self-Review, Step Granularity, Task Right-Sizing (+3 more)

### Community 57 - "domain/__init__.py"
Cohesion: 0.06
Nodes (15): AuditLogRepository, CircularRepository, CourseRepository, DepartmentRepository, FacultyProfileRepository, PushSubscriptionRepository, RefreshTokenRepository, ReminderRuleRepository (+7 more)

### Community 58 - "TimetableUpload"
Cohesion: 0.12
Nodes (9): TimetableUpload, InvalidTransition, Acceptance criteria, Goal, Input formats to support, Maths to specify first, Pipeline, Stage 04: Timetable upload, parsing and initials resolution (+1 more)

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
Cohesion: 0.17
Nodes (4): GetUpcomingNotificationsUseCase, RegisterPushSubscriptionUseCase, UpdateReminderRuleUseCase, UpdateUserQuietHoursUseCase

### Community 63 - "compute_priority_score"
Cohesion: 0.21
Nodes (13): compute_lead_alert_times(), compute_overdue_alert_times(), compute_priority_score(), test_completed_task_priority(), test_completion_rate(), test_lead_alert_times(), test_overdue_alert_times(), test_priority_bounds_property_active() (+5 more)

### Community 64 - "timetable_tasks.py"
Cohesion: 0.24
Nodes (3): ping(), process_timetable_upload(), _run_parse()

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

### Community 70 - "FacultyProfile"
Cohesion: 0.26
Nodes (8): FacultyProfile, InitialsResolver, normalized_similarity(), ResolutionOutcome, test_ambiguity_threshold_rejection(), test_exact_and_alias_resolution(), test_normalized_similarity_properties(), 5.3 Initials Resolution via Normalized Levenshtein Distance

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

### Community 79 - "InvariantViolation"
Cohesion: 0.14
Nodes (5): InvariantViolation, 1.2 Half-Open Interval Invariant and Overlap Arithmetic, 1.3 State Machine Transition Algebras, 1. Time and Recurrence, Circular State Machine

### Community 80 - "TaskTemplateRepositoryImpl"
Cohesion: 0.67
Nodes (3): TaskTemplate, task_template_to_domain(), TaskTemplateRepositoryImpl

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

### Community 91 - "deps.py"
Cohesion: 0.12
Nodes (13): get_storage(), confirm_timetable(), ConfirmTimetableResponse, TimetableSlotResponse, TimetableUploadDetailResponse, upload_timetable(), UploadTimetableResponse, ConfirmTimetableUseCase (+5 more)

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
Cohesion: 0.38
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

### Community 113 - "ScheduledNotification"
Cohesion: 0.24
Nodes (3): ScheduledNotification, ConcurrentMockNotifier, test_concurrency_dispatcher_skip_locked()

### Community 114 - "engine.py"
Cohesion: 0.24
Nodes (3): OcrEngine, OcrResult, WordBox

### Community 124 - ".__aenter__"
Cohesion: 0.27
Nodes (3): PushSubscription, push_subscription_to_domain(), PushSubscriptionRepositoryImpl

### Community 131 - "test_ocr_maths.py"
Cohesion: 0.24
Nodes (10): compute_length_weighted_confidence(), test_confidence_bounds_property(), test_confidence_empty_tokens(), test_deskew_skip_sub_threshold(), test_length_weighted_document_confidence(), 6.1 Document Confidence: Length-Weighted Mean, 6.2 Image Deskewing via Minimum-Area Bounding Rectangle, 6.3 Field Confidence Rules and Review Queue Gate Predicate (+2 more)

### Community 135 - "QuietHours"
Cohesion: 0.31
Nodes (5): adjust_for_quiet_hours(), GetUserQuietHoursUseCase, QuietHours, test_quiet_hours_midnight_crossing(), test_quiet_hours_table()

### Community 138 - "RefreshToken"
Cohesion: 0.25
Nodes (4): RefreshToken, RefreshTokenModel, refresh_token_to_domain(), RefreshTokenRepositoryImpl

### Community 139 - "generate_sample_circulars.py"
Cohesion: 0.29
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

### Community 150 - "test_clock.py"
Cohesion: 0.50
Nodes (3): test_clock_always_returns_utc_property(), test_frozen_clock_rejects_naive_datetime(), 1.1 Canonical Time Representation and Clock Invariant

## Knowledge Gaps
- **22 isolated node(s):** `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react`, `@fullcalendar/timegrid`, `@hookform/resolvers` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 833 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **47 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `test_calendar_full_pipeline`, `User`, `QuietHours`, `SqlAlchemyUnitOfWork`, `Principal`, `calendar.py`, `auth.py`, `delete_push_subscription`, `delete_task`, `auth.py`, `reminders.py`, `AcademicTerm`, `get_ics_feed`, `test_reschedule_and_cancel_lifecycle`, `Circular`, `Event`, `tasks.py`, `Domain (backend/app/domain)`, `tasks/use_cases.py`, `Root Cause Tracing`, `ReminderRule`, `zoneinfo`, `domain/__init__.py`, `reminders/use_cases.py`, `Stage 07: Meeting circular scanning, extraction and review queue`, `deps.py`, `ocr/__init__.py`, `ScheduledNotification`, `engine.py`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 52 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `datetime` be split into smaller, more focused modules?**
  _Cohesion score 0.13350340136054423 - nodes in this community are weakly interconnected._
- **Why does `Clock` connect `UnitOfWork` to `test_calendar_full_pipeline`, `User`, `Principal`, `calendar.py`, `auth.py`, `auth.py`, `Backend Engineer`, `test_clock.py`, `get_ics_feed`, `test_reschedule_and_cancel_lifecycle`, `Circular`, `AcademicTerm`, `Event`, `tasks.py`, `tasks/use_cases.py`, `Root Cause Tracing`, `FacultyDesk Decisions`, `ReminderRule`, `FrozenClock`, `FacultyDesk Agent Contract`, `deps.py`, `ocr/__init__.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 50 inferred relationships involving `Clock` (e.g. with `Standards you are held to` and `Non-negotiables`) actually correct?**
  _`Clock` has 50 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._