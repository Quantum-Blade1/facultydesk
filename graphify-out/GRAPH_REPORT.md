# Graph Report - facultydesk  (2026-10-28)

## Corpus Check
- 233 files · ~206,395 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 19 file(s) not represented in the graph (top: (none) 10, .csv 2, .example 1)

## Summary
- 2293 nodes · 6463 edges · 167 communities (127 shown, 40 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 979 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6f61e20c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- server.cjs
- Department
- Event
- NotFoundError
- UUID
- auth.py
- SqlAlchemyUnitOfWork
- db/repositories.py
- sqlalchemy
- UnitOfWork
- Principal
- calendar.py
- auth.py
- deps.py
- Task
- 4. Exactly-Once Delivery
- auth.py
- reminders.py
- Test-Driven Development (TDD)
- reminders.py
- InvariantViolation
- deps.py
- Visual Companion Guide
- Circular
- AcademicTermRepositoryImpl
- logging.py
- main.py
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
- compute_priority_score
- ScheduledNotification
- ReminderRuleRepositoryImpl
- FindFreeSlotsUseCase
- Root Cause Tracing
- Defense-in-Depth Validation
- manifest.json
- devDependencies
- Brainstorming
- FrozenClock
- FacultyProfile
- Section
- timetable.py
- Section
- tasks/use_cases.py
- metrics.py
- RoomRepositoryImpl
- helper.js
- Brainstorming
- Course
- TimetableUpload
- Web Application Testing
- clash_detector.py
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
- .execute
- builder-check-prompt.md
- task-done
- Kickoff prompt (paste this into the Antigravity agent)
- ooad-diagrams/SKILL.md
- logging.py
- test-academic.md
- api/__init__.py
- application/__init__.py
- find-polluter.sh
- infrastructure/__init__.py
- seed/__init__.py
- PushSubscription
- NotificationRepositoryImpl
- test_ocr_maths.py
- bulk_import.py
- facultydesk-backend
- RefreshToken
- QuietHours
- test_parsers.py
- delete_push_subscription
- Stage 04: Timetable upload, parsing and initials resolution
- delete_task
- CircularRepositoryImpl
- Stage 07: Meeting circular scanning, extraction and review queue
- list_templates
- TimetableSlotRepositoryImpl
- Stage 06: Reminder engine with exactly-once delivery
- Backend Engineer
- TimetableUploadRepositoryImpl
- update_quiet_hours
- register_push_subscription
- 5. Initials and Name Matching
- OCR and Parsing Engineer
- test_meeting_time_grammar_table

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 173 edges
2. `Clock` - 111 edges
3. `Principal` - 89 edges
4. `ScheduledNotification` - 75 edges
5. `FacultyProfile` - 73 edges
6. `Event` - 68 edges
7. `User` - 59 edges
8. `NotFoundError` - 58 edges
9. `SqlAlchemyUnitOfWork` - 49 edges
10. `InvariantViolation` - 47 edges

## Surprising Connections (you probably didn't know these)
- `Standards you are held to` --references--> `Clock`  [INFERRED]
  .agents/agents/backend-engineer.md → backend/app/core/clock.py
- `Non-negotiables` --references--> `Clock`  [INFERRED]
  AGENTS.md → backend/app/core/clock.py
- `5.4 Merged-Cell Period Expansion` --references--> `TimetableSlot`  [INFERRED]
  docs/MATHS.md → backend/app/domain/entities.py
- `Pipeline` --references--> `Circular`  [INFERRED]
  prompts/07-circular-ocr.md → backend/app/domain/entities.py
- `5.1 Initials Value Object Invariant` --references--> `InvariantViolation`  [INFERRED]
  docs/MATHS.md → backend/app/domain/errors.py

## Import Cycles
- None detected.

## Communities (167 total, 40 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.21
Nodes (13): split_co_teachers(), tokenize_cell(), CsvTimetableParser, _get_col(), _parse_clock_time(), _adjust_hour(), normalize_weekday(), parse_time_range() (+5 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 3 - "Event"
Cohesion: 0.12
Nodes (29): generate_vcalendar_ics(), CancelEventUseCase, CheckClashesUseCase, CreateEventUseCase, GetCalendarEventsUseCase, MaterialiseTimetableEventsUseCase, RotateIcsTokenUseCase, UpdateEventUseCase (+21 more)

### Community 4 - "NotFoundError"
Cohesion: 0.12
Nodes (8): update_faculty(), CreateFacultyUseCase, UpdateFacultyUseCase, ConflictError, FacultyDeskError, InvalidTransition, NotFoundError, ValidationError

### Community 5 - "UUID"
Cohesion: 0.03
Nodes (15): Room, TaskTemplate, AcademicTermRepository, AuditLogRepository, CircularRepository, DepartmentRepository, EventRepository, FacultyProfileRepository (+7 more)

### Community 6 - "auth.py"
Cohesion: 0.18
Nodes (14): change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest, LoginResponse (+6 more)

### Community 7 - "SqlAlchemyUnitOfWork"
Cohesion: 0.14
Nodes (16): get_clock(), SystemClock, materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation(), process_circular_upload(), _run_process_circular(), _build_dispatcher() (+8 more)

### Community 8 - "db/repositories.py"
Cohesion: 0.18
Nodes (18): Base, get_db(), AuditLogModel, CourseModel, DepartmentModel, EventAttendeeModel, EventModel, FacultyProfileModel (+10 more)

### Community 9 - "sqlalchemy"
Cohesion: 0.10
Nodes (9): do_run_migrations(), run_async_migrations(), run_migrations_online(), upgrade(), upgrade(), upgrade(), upgrade(), upgrade() (+1 more)

### Community 10 - "UnitOfWork"
Cohesion: 0.07
Nodes (5): get_ics_feed(), GenerateIcsFeedUseCase, UpdateTaskUseCase, Clock, UnitOfWork

### Community 11 - "Principal"
Cohesion: 0.22
Nodes (10): require_hod_or_admin(), retry_failed_notification(), DeactivateFacultyUseCase, ManageTermsUseCase, AuthorisationPolicy, Principal, ForbiddenError, test_admin_policy_allows_all() (+2 more)

### Community 12 - "calendar.py"
Cohesion: 0.13
Nodes (14): CalendarEventResponse, cancel_calendar_event(), check_event_clashes(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots() (+6 more)

### Community 13 - "auth.py"
Cohesion: 0.10
Nodes (24): AcademicTermResponse, add_holiday(), bulk_import_faculty(), bulk_import_holidays(), BulkImportResponse, create_faculty(), create_term(), CreateAcademicTermRequest (+16 more)

### Community 14 - "deps.py"
Cohesion: 0.20
Nodes (7): get_rate_limiter(), get_redis(), require_admin(), RateLimitExceededError, get_redis_client(), RedisSlidingWindowRateLimiter, test_sliding_window_rate_limiter()

### Community 15 - "Task"
Cohesion: 0.14
Nodes (5): Task, TaskRepository, TaskStatus, task_to_domain(), TaskRepositoryImpl

### Community 16 - "4. Exactly-Once Delivery"
Cohesion: 0.40
Nodes (5): 4.1 Deterministic Idempotency Key Derivation, 4.2 Distributed Dispatch via Skip-Locked Batch Claiming, 4.3 Stale SENDING Recovery and Failure Window Bound, 4.4 Maximum Lateness Bound, 4. Exactly-Once Delivery

### Community 17 - "auth.py"
Cohesion: 0.16
Nodes (17): get_current_principal(), ChangePasswordUseCase, LoginResult, LoginUseCase, LogoutUseCase, RefreshResult, RefreshTokenUseCase, UnauthorizedError (+9 more)

### Community 18 - "reminders.py"
Cohesion: 0.14
Nodes (5): event_to_domain(), EventRepositoryImpl, faculty_profile_to_domain(), FacultyProfileRepositoryImpl, RefreshTokenRepositoryImpl

### Community 19 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 20 - "reminders.py"
Cohesion: 0.20
Nodes (9): get_reminder_rules(), get_upcoming_notifications(), get_vapid_public_key(), ReminderRuleResponse, ScheduledNotificationResponse, update_reminder_rule(), UpdateQuietHoursRequest, UpdateReminderRuleRequest (+1 more)

### Community 21 - "InvariantViolation"
Cohesion: 0.09
Nodes (13): expand_slot_recurrence(), AcademicTerm, TimetableSlot, InvariantViolation, TimeSlot, test_event_invariants(), test_initials_invalid_property(), test_initials_valid_property() (+5 more)

### Community 22 - "deps.py"
Cohesion: 0.08
Nodes (24): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+16 more)

### Community 23 - "Visual Companion Guide"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 24 - "Circular"
Cohesion: 0.13
Nodes (15): CircularDetailResponse, CircularUploadResponse, confirm_circular(), ConfirmCircularRequest, ConfirmCircularResponse, get_circular(), list_review_queue(), reject_circular() (+7 more)

### Community 25 - "AcademicTermRepositoryImpl"
Cohesion: 0.31
Nodes (4): AcademicTermModel, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 26 - "logging.py"
Cohesion: 0.27
Nodes (4): is_server_ready(), main(), main(), main()

### Community 27 - "main.py"
Cohesion: 0.14
Nodes (4): domain_exception_handler(), healthz(), lifespan(), readyz()

### Community 28 - "extractor.py"
Cohesion: 0.18
Nodes (13): detect_probable_duplicate(), normalize_title(), ExtractedAttendee, ExtractedTime, ExtractionResult, parse_meeting_date(), parse_meeting_time(), parse_military_time() (+5 more)

### Community 29 - "tasks.py"
Cohesion: 0.14
Nodes (16): assign_task(), AssignmentProgressResponse, AssignTaskRequest, complete_task(), create_task(), CreateTaskRequest, ensure_utc(), FacultyOverdueSummaryResponse (+8 more)

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
Cohesion: 0.16
Nodes (16): DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged, TimetableConfirmed, test_event_reschedule() (+8 more)

### Community 34 - "test_hardening.py"
Cohesion: 0.22
Nodes (13): compute_lateness_percentiles(), detect_mime_and_extension(), validate_upload_content(), test_task_invariants(), test_timeslot_invariants(), test_compute_lateness_percentiles_100_elements(), test_compute_lateness_percentiles_empty(), test_compute_lateness_percentiles_single() (+5 more)

### Community 36 - "ScheduledNotification"
Cohesion: 0.10
Nodes (20): 1. Problem and users, 3. Architecture, 4.10 Reminder Dispatch and Exactly-Once Delivery Sequence, 4.11 Meeting Circular Scanning, Extraction, and Review Sequence, 4.11 Task Assignment, Alert Lifecycle and Escalation Sequence, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine (+12 more)

### Community 37 - "Root Cause Tracing"
Cohesion: 0.15
Nodes (13): ReminderDispatcher, adjust_for_quiet_hours(), compute_backoff_delay(), compute_fire_time(), compute_idempotency_key(), UpdateReminderRuleUseCase, ReminderRule, NotificationChannel (+5 more)

### Community 38 - "compute_priority_score"
Cohesion: 0.17
Nodes (17): compute_completion_rate(), compute_lead_alert_times(), compute_overdue_alert_times(), compute_priority_score(), test_completed_task_priority(), test_completion_rate(), test_lead_alert_times(), test_overdue_alert_times() (+9 more)

### Community 39 - "ScheduledNotification"
Cohesion: 0.09
Nodes (3): ScheduledNotification, NotificationRepository, NotificationStatus

### Community 40 - "ReminderRuleRepositoryImpl"
Cohesion: 0.39
Nodes (3): ReminderRuleModel, reminder_rule_to_domain(), ReminderRuleRepositoryImpl

### Community 41 - "FindFreeSlotsUseCase"
Cohesion: 0.22
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

### Community 47 - "FrozenClock"
Cohesion: 0.13
Nodes (12): FrozenClock, test_clock_always_returns_utc_property(), test_frozen_clock_advance_property(), test_frozen_clock_rejects_naive_datetime(), FacultyDesk Decisions, Stage 00: Agent setup, Stage 01: Foundation, environment, Graphify, trusted skills, 1.1 Canonical Time Representation and Clock Invariant (+4 more)

### Community 48 - "FacultyProfile"
Cohesion: 0.08
Nodes (28): Department, FacultyProfile, Holiday, User, Initials, Role, SqlAlchemyUnitOfWork, NotificationPayload (+20 more)

### Community 49 - "Section"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 50 - "timetable.py"
Cohesion: 0.11
Nodes (13): confirm_timetable(), ConfirmTimetableResponse, get_faculty_slots(), get_timetable_upload(), TimetableSlotResponse, TimetableUploadDetailResponse, upload_timetable(), UploadTimetableResponse (+5 more)

### Community 51 - "Section"
Cohesion: 0.27
Nodes (4): Section, SectionRepository, section_to_domain(), SectionRepositoryImpl

### Community 52 - "tasks/use_cases.py"
Cohesion: 0.24
Nodes (12): AssignmentProgress, AssignTaskUseCase, CompleteTaskUseCase, CreateTaskUseCase, FacultyOverdueSummary, GetHodDashboardUseCase, HodDashboardData, ListTasksUseCase (+4 more)

### Community 53 - "metrics.py"
Cohesion: 0.24
Nodes (6): get_uow(), AdminMetricsResponse, DeadLetterResponse, get_system_metrics(), LatenessPercentilesResponse, QueueDepthResponse

### Community 54 - "RoomRepositoryImpl"
Cohesion: 0.48
Nodes (3): RoomModel, room_to_domain(), RoomRepositoryImpl

### Community 55 - "helper.js"
Cohesion: 0.17
Nodes (11): Applying the Pattern, Defense-in-Depth Validation, Example from Session, Key Insight, Layer 1: Entry Point Validation, Layer 2: Business Logic Validation, Layer 3: Environment Guards, Layer 4: Debug Instrumentation (+3 more)

### Community 56 - "Brainstorming"
Cohesion: 0.17
Nodes (11): Execution Handoff, File Structure, Overview, Plan Document Header, Scope Check, Self-Review, Step Granularity, Task Right-Sizing (+3 more)

### Community 57 - "Course"
Cohesion: 0.27
Nodes (4): Course, CourseRepository, course_to_domain(), CourseRepositoryImpl

### Community 59 - "Web Application Testing"
Cohesion: 0.17
Nodes (12): devDependencies, eslint, eslint-config-next, openapi-typescript, prettier, prettier-plugin-tailwindcss, tailwindcss, @tailwindcss/turbopack (+4 more)

### Community 60 - "clash_detector.py"
Cohesion: 0.33
Nodes (8): Interval, intervals_overlap(), pairwise_clashes(), SweepLineClashDetector, test_adjacent_intervals_no_clash(), test_sweep_line_clash_detection_matches_pairwise_property(), test_worked_example_from_maths_md(), 2.2 Sweep-Line Interval Clash Detection Algorithm

### Community 61 - "NotificationRepositoryImpl"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 62 - "reminders/use_cases.py"
Cohesion: 0.19
Nodes (4): GetUpcomingNotificationsUseCase, GetUserQuietHoursUseCase, GetUserReminderRulesUseCase, RegisterPushSubscriptionUseCase

### Community 63 - "Circular"
Cohesion: 0.16
Nodes (6): Circular, test_circular_state_machine_exhaustive(), test_notification_state_machine_exhaustive(), 1.3 State Machine Transition Algebras, Circular State Machine, ScheduledNotification State Machine

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

### Community 69 - "Stage 03: Authentication, authorization, and faculty directory"
Cohesion: 0.22
Nodes (5): BackupService, backup_database_to_minio(), test_backup_prune_expired(), test_backup_prune_preserves_single_expired_backup(), Stage 03: Authentication, authorization, and faculty directory

### Community 70 - "FacultyDesk Maths"
Cohesion: 0.13
Nodes (14): 10.1 Token Lifetimes, Rotation, and Family Reuse Detection, 10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix, 10.3 Sliding Window Log Rate Limiting, 10. Security Limits, 1.2 Half-Open Interval Invariant and Overlap Arithmetic, 1. Time and Recurrence, 2.1 Half-Open Overlap Predicate, 2.3 Multi-Attendee Common Free-Slot Finder (+6 more)

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
Cohesion: 0.13
Nodes (8): run_migrations_offline(), get_storage(), get_settings(), Settings, get_storage_service(), MinioStorageService, process_timetable_upload(), _run_parse()

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

### Community 108 - ".execute"
Cohesion: 0.19
Nodes (10): compute_deskew_angle(), deskew_image(), has_pdf_text_layer(), preprocess_image_for_ocr(), rasterise_pdf_page(), _get_font(), main(), _make_pdf_with_text() (+2 more)

### Community 109 - "builder-check-prompt.md"
Cohesion: 0.50
Nodes (3): eslintConfig, eslint, eslint-config-next

### Community 110 - "task-done"
Cohesion: 0.50
Nodes (3): Deploy on Vercel, Getting Started, Learn More

### Community 111 - "Kickoff prompt (paste this into the Antigravity agent)"
Cohesion: 0.50
Nodes (3): Kickoff prompt (paste this into the Antigravity agent), Resuming in a new conversation, Running a single stage manually

### Community 124 - "PushSubscription"
Cohesion: 0.15
Nodes (4): PushSubscription, PushSubscriptionRepository, push_subscription_to_domain(), PushSubscriptionRepositoryImpl

### Community 131 - "test_ocr_maths.py"
Cohesion: 0.15
Nodes (12): compute_length_weighted_confidence(), OcrEngine, OcrResult, WordBox, test_confidence_bounds_property(), test_confidence_empty_tokens(), test_length_weighted_document_confidence(), 6.1 Document Confidence: Length-Weighted Mean (+4 more)

### Community 135 - "bulk_import.py"
Cohesion: 0.29
Nodes (3): BulkImportFacultyUseCase, BulkImportReport, RowImportResult

### Community 139 - "QuietHours"
Cohesion: 0.29
Nodes (3): UpdateUserQuietHoursUseCase, QuietHours, test_quiet_hours_midnight_crossing()

### Community 140 - "test_parsers.py"
Cohesion: 0.38
Nodes (8): TimetableParserFactory, PdfTimetableParser, test_csv_timetable_parsing(), test_pdf_text_timetable_parsing(), test_scanned_pdf_rejection(), test_xlsx_co_teachers_parsing(), test_xlsx_merged_cell_period_expansion(), test_xlsx_standard_timetable_parsing()

### Community 141 - "delete_push_subscription"
Cohesion: 0.25
Nodes (3): delete_push_subscription(), DeletePushSubscriptionRequest, DeletePushSubscriptionUseCase

### Community 142 - "Stage 04: Timetable upload, parsing and initials resolution"
Cohesion: 0.25
Nodes (7): Acceptance criteria, Goal, Input formats to support, Maths to specify first, Pipeline, Stage 04: Timetable upload, parsing and initials resolution, Tests

### Community 144 - "CircularRepositoryImpl"
Cohesion: 0.48
Nodes (3): CircularModel, circular_to_domain(), CircularRepositoryImpl

### Community 145 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Corpus and tests, Goal, Maths to specify first, Pipeline, Stage 07: Meeting circular scanning, extraction and review queue

### Community 146 - "list_templates"
Cohesion: 0.38
Nodes (3): list_templates(), TaskTemplateResponse, ListTaskTemplatesUseCase

### Community 147 - "TimetableSlotRepositoryImpl"
Cohesion: 0.48
Nodes (3): TimetableSlotModel, timetable_slot_to_domain(), TimetableSlotRepositoryImpl

### Community 148 - "Stage 06: Reminder engine with exactly-once delivery"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 06: Reminder engine with exactly-once delivery, Tests

### Community 149 - "Backend Engineer"
Cohesion: 0.40
Nodes (4): Backend Engineer, Responsibilities, Standards you are held to, Working method

### Community 150 - "TimetableUploadRepositoryImpl"
Cohesion: 0.48
Nodes (3): TimetableUploadModel, timetable_upload_to_domain(), TimetableUploadRepositoryImpl

### Community 152 - "update_quiet_hours"
Cohesion: 0.47
Nodes (3): get_quiet_hours(), QuietHoursResponse, update_quiet_hours()

### Community 153 - "register_push_subscription"
Cohesion: 0.40
Nodes (3): PushSubscriptionRequest, PushSubscriptionResponse, register_push_subscription()

### Community 154 - "5. Initials and Name Matching"
Cohesion: 0.40
Nodes (5): 5.1 Initials Value Object Invariant, 5.2 Timetable Cell Tokenization Grammar, 5.4 Merged-Cell Period Expansion, 5.5 Header Day and Time Normalization, 5. Initials and Name Matching

### Community 155 - "OCR and Parsing Engineer"
Cohesion: 0.50
Nodes (3): OCR and Parsing Engineer, Responsibilities, Rules

### Community 156 - "test_meeting_time_grammar_table"
Cohesion: 0.50
Nodes (4): test_meeting_time_grammar_table(), 7.1 Formal Time Grammar and Assumed Duration Invariant, 7.2 Date Extraction with Cue Words and Timezone Anchoring, 7. Date and Time Extraction

## Knowledge Gaps
- **22 isolated node(s):** `RFC-6455`, `facultydesk-backend`, `clsx`, `@fullcalendar/core`, `@fullcalendar/daygrid` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 852 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `Event`, `NotFoundError`, `UUID`, `auth.py`, `bulk_import.py`, `Principal`, `calendar.py`, `auth.py`, `delete_push_subscription`, `delete_task`, `QuietHours`, `auth.py`, `list_templates`, `reminders.py`, `Circular`, `register_push_subscription`, `update_quiet_hours`, `tasks.py`, `Domain (backend/app/domain)`, `Root Cause Tracing`, `FindFreeSlotsUseCase`, `FacultyProfile`, `timetable.py`, `tasks/use_cases.py`, `metrics.py`, `reminders/use_cases.py`, `Stage 07: Meeting circular scanning, extraction and review queue`, `MinioStorageService`, `.execute`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 52 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RFC-6455`, `facultydesk-backend`, `clsx` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._
- **Why does `Clock` connect `UnitOfWork` to `Event`, `NotFoundError`, `auth.py`, `SqlAlchemyUnitOfWork`, `bulk_import.py`, `Principal`, `calendar.py`, `auth.py`, `deps.py`, `auth.py`, `Backend Engineer`, `Circular`, `tasks.py`, `Root Cause Tracing`, `FrozenClock`, `FacultyProfile`, `timetable.py`, `tasks/use_cases.py`, `metrics.py`, `FacultyDesk Agent Contract`, `MinioStorageService`, `.execute`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Clock` (e.g. with `Standards you are held to` and `Non-negotiables`) actually correct?**
  _`Clock` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Should `Event` be split into smaller, more focused modules?**
  _Cohesion score 0.11656746031746032 - nodes in this community are weakly interconnected._