# Graph Report - facultydesk  (2026-10-28)

## Corpus Check
- 240 files · ~218,087 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: (none) 11, .csv 2, .example 1)

## Summary
- 2308 nodes · 6575 edges · 155 communities (121 shown, 34 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 913 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `16996863`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- server.cjs
- Department
- Event
- get_settings
- domain/repositories.py
- FacultyProfileRepositoryImpl
- SqlAlchemyUnitOfWork
- db/repositories.py
- main.py
- UnitOfWork
- sqlalchemy
- calendar.py
- Principal
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
- circulars/use_cases.py
- test_ocr_maths.py
- assign_task
- Systematic Debugging
- RefreshToken
- components.json
- InvariantViolation
- Initials
- ScheduledNotification
- reminders/maths.py
- compute_priority_score
- NotificationRepository
- ReminderRuleRepositoryImpl
- calendar/__init__.py
- Root Cause Tracing
- Defense-in-Depth Validation
- manifest.json
- devDependencies
- Brainstorming
- FrozenClock
- FacultyProfile
- Section
- pytest
- SectionRepositoryImpl
- tasks/use_cases.py
- deps.py
- RoomRepositoryImpl
- helper.js
- Brainstorming
- CourseRepositoryImpl
- EntityNotFound
- Web Application Testing
- db/repositories.py
- NotificationRepositoryImpl
- reminders/use_cases.py
- TimetableUpload
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
- extractor.py
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
- calendar/use_cases.py
- builder-check-prompt.md
- task-done
- Kickoff prompt (paste this into the Antigravity agent)
- ooad-diagrams/SKILL.md
- preprocessor.py
- with_server.py
- test-academic.md
- api/__init__.py
- application/__init__.py
- find-polluter.sh
- infrastructure/__init__.py
- seed/__init__.py
- Department
- NotificationRepositoryImpl
- AuditLogRepository
- TaskRepositoryImpl
- facultydesk-backend
- test_circular_full_pipeline_with_samples
- assign_task
- TimetableSlotRepositoryImpl
- duplicate_detector.py
- Stage 04: Timetable upload, parsing and initials resolution
- delete_task
- Circular
- Stage 07: Meeting circular scanning, extraction and review queue
- tasks.py
- ReminderPlanner

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 165 edges
2. `Clock` - 103 edges
3. `Principal` - 94 edges
4. `FacultyProfile` - 79 edges
5. `ScheduledNotification` - 75 edges
6. `Event` - 67 edges
7. `User` - 64 edges
8. `NotFoundError` - 49 edges
9. `InvariantViolation` - 49 edges
10. `Initials` - 49 edges

## Surprising Connections (you probably didn't know these)
- `Persistence` --references--> `UnitOfWork`  [INFERRED]
  prompts/02-domain-model.md → backend/app/domain/repositories.py
- `10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix` --references--> `AuthorisationPolicy`  [INFERRED]
  docs/MATHS.md → backend/app/application/security/policy.py
- `Standards you are held to` --references--> `Clock`  [INFERRED]
  .agents/agents/backend-engineer.md → backend/app/core/clock.py
- `Non-negotiables` --references--> `Clock`  [INFERRED]
  AGENTS.md → backend/app/core/clock.py
- `5.4 Merged-Cell Period Expansion` --references--> `TimetableSlot`  [INFERRED]
  docs/MATHS.md → backend/app/domain/entities.py

## Import Cycles
- None detected.

## Communities (155 total, 34 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.09
Nodes (37): OCR and Parsing Engineer, Responsibilities, Rules, split_co_teachers(), tokenize_cell(), CsvTimetableParser, _get_col(), _parse_clock_time() (+29 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 2 - "Department"
Cohesion: 0.43
Nodes (3): DepartmentModel, department_to_domain(), DepartmentRepositoryImpl

### Community 3 - "Event"
Cohesion: 0.21
Nodes (8): generate_vcalendar_ics(), Event, EventKind, test_planning_idempotency_property(), test_ics_export_stable_uids(), test_ics_export_valid_rfc5545(), test_duplicate_predicate_worked_example(), 2.4 RFC 5545 ICS Feed Specification

### Community 4 - "get_settings"
Cohesion: 0.16
Nodes (7): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_settings(), Settings, get_db()

### Community 5 - "domain/repositories.py"
Cohesion: 0.05
Nodes (9): CourseRepository, EventRepository, FacultyProfileRepository, RefreshTokenRepository, RoomRepository, SectionRepository, TimetableSlotRepository, TimetableUploadRepository (+1 more)

### Community 6 - "FacultyProfileRepositoryImpl"
Cohesion: 0.38
Nodes (3): FacultyProfileModel, faculty_profile_to_domain(), FacultyProfileRepositoryImpl

### Community 7 - "SqlAlchemyUnitOfWork"
Cohesion: 0.13
Nodes (17): SystemClock, SqlAlchemyUnitOfWork, materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation(), process_circular_upload(), _run_process_circular(), dispatch_due_notifications() (+9 more)

### Community 8 - "db/repositories.py"
Cohesion: 0.16
Nodes (13): Base, CircularModel, EventAttendeeModel, EventModel, HolidayModel, PushSubscriptionModel, RefreshTokenModel, ReminderRuleModel (+5 more)

### Community 9 - "main.py"
Cohesion: 0.08
Nodes (6): configure_logging(), RequestIdMiddleware, domain_exception_handler(), healthz(), lifespan(), readyz()

### Community 10 - "UnitOfWork"
Cohesion: 0.10
Nodes (4): MaterialiseTimetableEventsUseCase, ConfirmTimetableUseCase, Clock, UnitOfWork

### Community 11 - "sqlalchemy"
Cohesion: 0.10
Nodes (14): upgrade(), upgrade(), upgrade(), upgrade(), upgrade(), Interval, intervals_overlap(), pairwise_clashes() (+6 more)

### Community 12 - "calendar.py"
Cohesion: 0.16
Nodes (12): CalendarEventResponse, check_event_clashes(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots(), FindFreeSlotsRequest (+4 more)

### Community 13 - "Principal"
Cohesion: 0.05
Nodes (48): require_admin(), require_hod_or_admin(), AcademicTermResponse, add_holiday(), bulk_import_faculty(), bulk_import_holidays(), BulkImportResponse, create_faculty() (+40 more)

### Community 15 - "Task"
Cohesion: 0.15
Nodes (3): Task, TaskRepository, test_task_invariants()

### Community 16 - "Stage 05: Calendar core, recurrence, clash detection, ICS feed"
Cohesion: 0.33
Nodes (5): Acceptance criteria, Goal, Maths to specify first, Stage 05: Calendar core, recurrence, clash detection, ICS feed, Tests

### Community 17 - "auth.py"
Cohesion: 0.07
Nodes (35): change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest, LoginResponse (+27 more)

### Community 19 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 20 - "reminders.py"
Cohesion: 0.10
Nodes (18): delete_push_subscription(), DeletePushSubscriptionRequest, get_quiet_hours(), get_reminder_rules(), get_upcoming_notifications(), get_vapid_public_key(), PushSubscriptionRequest, PushSubscriptionResponse (+10 more)

### Community 21 - "InvariantViolation"
Cohesion: 0.10
Nodes (11): expand_slot_recurrence(), AcademicTerm, Holiday, TimetableSlot, AcademicTermRepository, main(), seed_database(), test_recurrence_expansion_matching_weekday() (+3 more)

### Community 22 - "deps.py"
Cohesion: 0.08
Nodes (24): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+16 more)

### Community 23 - "Visual Companion Guide"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 24 - "Circular"
Cohesion: 0.16
Nodes (10): CircularDetailResponse, CircularUploadResponse, confirm_circular(), ConfirmCircularRequest, ConfirmCircularResponse, get_circular(), list_review_queue(), reject_circular() (+2 more)

### Community 25 - "AcademicTermRepositoryImpl"
Cohesion: 0.31
Nodes (4): AcademicTermModel, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 26 - "demo_setup.py"
Cohesion: 0.22
Nodes (4): http_get_json(), http_post_json(), http_post_multipart(), run_demo_setup()

### Community 27 - "circulars/use_cases.py"
Cohesion: 0.14
Nodes (7): ConfirmCircularUseCase, GetCircularUseCase, ListReviewQueueUseCase, ProcessCircularUseCase, RejectCircularUseCase, UploadCircularUseCase, has_pdf_text_layer()

### Community 28 - "test_ocr_maths.py"
Cohesion: 0.15
Nodes (13): compute_length_weighted_confidence(), OcrEngine, OcrResult, WordBox, test_confidence_bounds_property(), test_confidence_empty_tokens(), test_length_weighted_document_confidence(), test_meeting_time_grammar_table() (+5 more)

### Community 29 - "assign_task"
Cohesion: 0.20
Nodes (6): complete_task(), create_task(), get_task(), list_tasks(), reopen_task(), TaskResponse

### Community 30 - "Systematic Debugging"
Cohesion: 0.10
Nodes (19): Browser Events Format, Cards (visual designs), Cleaning Up, CSS Classes Available, Design Tips, File Naming, How It Works, Mock elements (wireframe building blocks) (+11 more)

### Community 31 - "RefreshToken"
Cohesion: 0.10
Nodes (19): Bulletproofing Elements, Creation Log: Systematic Debugging Skill, Enhancement 1: TDD Reference, Extraction Decisions, Final Outcome, Initial Version, Iterations, Key Insight (+11 more)

### Community 32 - "components.json"
Cohesion: 0.10
Nodes (19): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+11 more)

### Community 33 - "InvariantViolation"
Cohesion: 0.17
Nodes (15): Course, Room, Section, InvariantViolation, DomainEvent, EventCancelled, EventRescheduled, TaskCreated (+7 more)

### Community 34 - "Initials"
Cohesion: 0.14
Nodes (13): Initials, TimeSlot, test_circular_state_machine_exhaustive(), test_initials_invalid_property(), test_initials_valid_property(), test_notification_state_machine_exhaustive(), test_timeslot_half_open_overlap(), test_timeslot_invariants() (+5 more)

### Community 36 - "ScheduledNotification"
Cohesion: 0.09
Nodes (22): 1. Problem and users, 3. Architecture, 4.10 Reminder Dispatch and Exactly-Once Delivery Sequence, 4.11 Meeting Circular Scanning, Extraction, and Review Sequence, 4.11 Task Assignment, Alert Lifecycle and Escalation Sequence, 4.1 Component Diagram, 4.2 Domain Class Diagram, 4.3 Circular State Machine (+14 more)

### Community 37 - "reminders/maths.py"
Cohesion: 0.19
Nodes (10): adjust_for_quiet_hours(), compute_backoff_delay(), compute_fire_time(), compute_idempotency_key(), QuietHours, test_quiet_hours_midnight_crossing(), test_backoff_bounds(), test_fire_time_computation() (+2 more)

### Community 38 - "compute_priority_score"
Cohesion: 0.21
Nodes (14): compute_completion_rate(), compute_lead_alert_times(), compute_overdue_alert_times(), compute_priority_score(), test_completed_task_priority(), test_completion_rate(), test_lead_alert_times(), test_overdue_alert_times() (+6 more)

### Community 40 - "ReminderRuleRepositoryImpl"
Cohesion: 0.18
Nodes (4): ReminderRule, ReminderRuleRepository, reminder_rule_to_domain(), ReminderRuleRepositoryImpl

### Community 41 - "calendar/__init__.py"
Cohesion: 0.17
Nodes (9): BusyInterval, FreeSlotFinder, merge_busy_intervals(), FindFreeSlotsUseCase, test_free_slots_never_intersect_busy_property(), test_free_slots_worked_example(), 2.1 Half-Open Overlap Predicate, 2.3 Multi-Attendee Common Free-Slot Finder (+1 more)

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
Cohesion: 0.18
Nodes (9): FrozenClock, test_clock_always_returns_utc_property(), test_frozen_clock_advance_property(), test_frozen_clock_rejects_naive_datetime(), 1.1 Canonical Time Representation and Clock Invariant, Acceptance criteria, Goal, Stage 01: Foundation, environment, Graphify, trusted skills (+1 more)

### Community 48 - "FacultyProfile"
Cohesion: 0.06
Nodes (26): Backend Engineer, Responsibilities, Standards you are held to, Working method, ReminderDispatcher, FacultyProfile, ScheduledNotification, User (+18 more)

### Community 49 - "Section"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 50 - "pytest"
Cohesion: 0.23
Nodes (14): compute_lateness_percentiles(), ValidationError, detect_mime_and_extension(), validate_upload_content(), rasterise_pdf_page(), test_event_invariants(), test_compute_lateness_percentiles_100_elements(), test_compute_lateness_percentiles_empty() (+6 more)

### Community 51 - "SectionRepositoryImpl"
Cohesion: 0.48
Nodes (3): SectionModel, section_to_domain(), SectionRepositoryImpl

### Community 52 - "tasks/use_cases.py"
Cohesion: 0.22
Nodes (11): AssignmentProgress, CompleteTaskUseCase, CreateTaskUseCase, FacultyOverdueSummary, GetHodDashboardUseCase, HodDashboardData, ListTasksUseCase, ReopenTaskUseCase (+3 more)

### Community 53 - "deps.py"
Cohesion: 0.16
Nodes (10): get_current_principal(), get_rate_limiter(), get_redis(), get_uow(), AdminMetricsResponse, DeadLetterResponse, get_system_metrics(), LatenessPercentilesResponse (+2 more)

### Community 54 - "RoomRepositoryImpl"
Cohesion: 0.48
Nodes (3): RoomModel, room_to_domain(), RoomRepositoryImpl

### Community 55 - "helper.js"
Cohesion: 0.17
Nodes (11): Applying the Pattern, Defense-in-Depth Validation, Example from Session, Key Insight, Layer 1: Entry Point Validation, Layer 2: Business Logic Validation, Layer 3: Environment Guards, Layer 4: Debug Instrumentation (+3 more)

### Community 56 - "Brainstorming"
Cohesion: 0.17
Nodes (11): Execution Handoff, File Structure, Overview, Plan Document Header, Scope Check, Self-Review, Step Granularity, Task Right-Sizing (+3 more)

### Community 57 - "CourseRepositoryImpl"
Cohesion: 0.48
Nodes (3): CourseModel, course_to_domain(), CourseRepositoryImpl

### Community 58 - "EntityNotFound"
Cohesion: 0.24
Nodes (5): get_ics_feed(), rotate_ics_token(), GenerateIcsFeedUseCase, RotateIcsTokenUseCase, EntityNotFound

### Community 59 - "Web Application Testing"
Cohesion: 0.15
Nodes (13): devDependencies, eslint, eslint-config-next, openapi-typescript, @playwright/test, prettier, prettier-plugin-tailwindcss, tailwindcss (+5 more)

### Community 60 - "db/repositories.py"
Cohesion: 0.36
Nodes (11): EventAttendee, AttendeeResponse, CircularStatus, EventSource, NotificationStatus, Role, TaskCategory, TaskRecurrence (+3 more)

### Community 61 - "NotificationRepositoryImpl"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 62 - "reminders/use_cases.py"
Cohesion: 0.12
Nodes (6): GetUpcomingNotificationsUseCase, GetUserQuietHoursUseCase, GetUserReminderRulesUseCase, RegisterPushSubscriptionUseCase, UpdateReminderRuleUseCase, UpdateUserQuietHoursUseCase

### Community 63 - "TimetableUpload"
Cohesion: 0.13
Nodes (7): TimetableUpload, ConflictError, DomainError, InvalidTransition, timetable_upload_to_domain(), TimetableUploadRepositoryImpl, Pipeline

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
Cohesion: 0.31
Nodes (4): BackupService, backup_database_to_minio(), test_backup_prune_expired(), test_backup_prune_preserves_single_expired_backup()

### Community 70 - "FacultyDesk Maths"
Cohesion: 0.08
Nodes (24): 10.1 Token Lifetimes, Rotation, and Family Reuse Detection, 10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix, 10.3 Sliding Window Log Rate Limiting, 10. Security Limits, 11.1 Dispatch Lateness Percentile Computation, 11.2 Backup Retention Arithmetic & Bounded Pruning, 11.3 Upload Decompression Bomb and Page Count Limits, 11. Hardening, Observability and Reliability (+16 more)

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

### Community 79 - "extractor.py"
Cohesion: 0.22
Nodes (13): CircularExtractor, ExtractedAttendee, ExtractedTime, ExtractionResult, parse_meeting_date(), parse_meeting_time(), parse_military_time(), parse_title_and_agenda() (+5 more)

### Community 80 - "TaskTemplate"
Cohesion: 0.20
Nodes (5): TaskTemplate, TaskTemplateRepository, TaskTemplateModel, task_template_to_domain(), TaskTemplateRepositoryImpl

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
Cohesion: 0.15
Nodes (4): PushSubscription, PushSubscriptionRepository, push_subscription_to_domain(), PushSubscriptionRepositoryImpl

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
Cohesion: 0.11
Nodes (15): get_clock(), get_storage(), confirm_timetable(), ConfirmTimetableResponse, TimetableSlotResponse, TimetableUploadDetailResponse, upload_timetable(), UploadTimetableResponse (+7 more)

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

### Community 108 - "calendar/use_cases.py"
Cohesion: 0.29
Nodes (6): CheckClashesUseCase, CreateEventUseCase, GetCalendarEventsUseCase, ClashDetectedError, EventScheduled, test_calendar_full_pipeline()

### Community 109 - "builder-check-prompt.md"
Cohesion: 0.50
Nodes (3): eslintConfig, eslint, eslint-config-next

### Community 110 - "task-done"
Cohesion: 0.50
Nodes (3): Deploy on Vercel, Getting Started, Learn More

### Community 111 - "Kickoff prompt (paste this into the Antigravity agent)"
Cohesion: 0.50
Nodes (3): Kickoff prompt (paste this into the Antigravity agent), Resuming in a new conversation, Running a single stage manually

### Community 113 - "preprocessor.py"
Cohesion: 0.25
Nodes (9): compute_deskew_angle(), deskew_image(), preprocess_image_for_ocr(), _get_font(), main(), _make_pdf_with_text(), _render_text_to_image(), test_deskew_skip_sub_threshold() (+1 more)

### Community 114 - "with_server.py"
Cohesion: 0.29
Nodes (4): is_server_ready(), main(), main(), main()

### Community 124 - "Department"
Cohesion: 0.21
Nodes (3): Department, DepartmentRepository, test_bulk_import_from_sample_csv()

### Community 127 - "NotificationRepositoryImpl"
Cohesion: 0.22
Nodes (3): ScheduledNotificationModel, notification_to_domain(), NotificationRepositoryImpl

### Community 131 - "AuditLogRepository"
Cohesion: 0.24
Nodes (4): AuditLogRepository, AuditLogModel, audit_log_to_domain(), AuditLogRepositoryImpl

### Community 135 - "TaskRepositoryImpl"
Cohesion: 0.33
Nodes (3): TaskModel, task_to_domain(), TaskRepositoryImpl

### Community 138 - "test_circular_full_pipeline_with_samples"
Cohesion: 0.25
Nodes (3): InMemoryStorageService, sample_dir(), test_circular_full_pipeline_with_samples()

### Community 139 - "assign_task"
Cohesion: 0.36
Nodes (4): assign_task(), AssignTaskUseCase, ListTaskTemplatesUseCase, test_task_creation_and_assignment_pipeline()

### Community 140 - "TimetableSlotRepositoryImpl"
Cohesion: 0.39
Nodes (3): TimetableSlotModel, timetable_slot_to_domain(), TimetableSlotRepositoryImpl

### Community 142 - "Stage 04: Timetable upload, parsing and initials resolution"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Goal, Input formats to support, Maths to specify first, Stage 04: Timetable upload, parsing and initials resolution, Tests

### Community 144 - "Circular"
Cohesion: 0.16
Nodes (5): Circular, CircularRepository, circular_to_domain(), CircularRepositoryImpl, test_round_trip_all_aggregates()

### Community 145 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Corpus and tests, Goal, Maths to specify first, Pipeline, Stage 07: Meeting circular scanning, extraction and review queue

### Community 146 - "tasks.py"
Cohesion: 0.17
Nodes (12): AssignmentProgressResponse, AssignTaskRequest, CreateTaskRequest, ensure_utc(), FacultyOverdueSummaryResponse, get_hod_dashboard(), HodDashboardResponse, list_templates() (+4 more)

### Community 149 - "ReminderPlanner"
Cohesion: 0.26
Nodes (5): cancel_calendar_event(), CancelEventUseCase, UpdateEventUseCase, ReminderPlanner, test_reschedule_and_cancel_lifecycle()

## Knowledge Gaps
- **22 isolated node(s):** `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react`, `@fullcalendar/timegrid`, `@hookform/resolvers` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 854 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `Event`, `domain/repositories.py`, `SqlAlchemyUnitOfWork`, `assign_task`, `calendar.py`, `Principal`, `delete_task`, `auth.py`, `tasks.py`, `reminders.py`, `ReminderPlanner`, `Circular`, `circulars/use_cases.py`, `assign_task`, `InvariantViolation`, `calendar/__init__.py`, `FacultyProfile`, `tasks/use_cases.py`, `deps.py`, `EntityNotFound`, `db/repositories.py`, `reminders/use_cases.py`, `Stage 07: Meeting circular scanning, extraction and review queue`, `MinioStorageService`, `calendar/use_cases.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 34 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 34 INFERRED edges - model-reasoned connections that need verification._
- **What connects `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `datetime` be split into smaller, more focused modules?**
  _Cohesion score 0.09027777777777778 - nodes in this community are weakly interconnected._
- **Why does `FacultyProfile` connect `FacultyProfile` to `datetime`, `Event`, `domain/repositories.py`, `FacultyProfileRepositoryImpl`, `test_circular_full_pipeline_with_samples`, `assign_task`, `Principal`, `Circular`, `auth.py`, `InvariantViolation`, `ReminderPlanner`, `test_ocr_maths.py`, `InvariantViolation`, `Initials`, `tasks/use_cases.py`, `db/repositories.py`, `extractor.py`, `MinioStorageService`, `calendar/use_cases.py`, `Department`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 46 inferred relationships involving `Clock` (e.g. with `Standards you are held to` and `Non-negotiables`) actually correct?**
  _`Clock` has 46 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._