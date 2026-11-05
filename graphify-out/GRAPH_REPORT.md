# Graph Report - facultydesk  (2026-11-05)

## Corpus Check
- 240 files · ~368,561 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: (none) 11, .csv 2, .example 1)

## Summary
- 2311 nodes · 6729 edges · 152 communities (125 shown, 27 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 1055 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f04a1392`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- datetime
- server.cjs
- AsyncSession
- ReminderPlanner
- get_settings
- domain/__init__.py
- UUID
- SqlAlchemyUnitOfWork
- db/repositories.py
- main.py
- demo_setup.py
- sqlalchemy
- Clock
- directory.py
- @playwright/test
- Task
- get_settings
- security.py
- Department
- Test-Driven Development (TDD)
- reminders.py
- AcademicTerm
- deps.py
- Visual Companion Guide
- Circular
- Principal
- NotFoundError
- auth.py
- test_ocr_maths.py
- update_task
- Systematic Debugging
- RefreshToken
- components.json
- domain/__init__.py
- InvariantViolation
- CircularRepository
- dataclasses
- QuietHours
- FacultyProfile
- UnitOfWork
- reminders.py
- calendar/__init__.py
- Root Cause Tracing
- Defense-in-Depth Validation
- manifest.json
- devDependencies
- Brainstorming
- clock.py
- FacultyProfile
- Section
- circulars/use_cases.py
- Section
- duplicate_detector.py
- deps.py
- Room
- helper.js
- Brainstorming
- Event
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
- tasks.py
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
- compute_priority_score
- Stage 01: Foundation, environment, Graphify, trusted skills
- test-academic.md
- api/__init__.py
- application/__init__.py
- find-polluter.sh
- infrastructure/__init__.py
- seed/__init__.py
- Stage 03: Authentication, authorization, and faculty directory
- ScheduledNotification
- pytest
- clash_detector.py
- facultydesk-backend
- RedisSlidingWindowRateLimiter
- value_objects.py
- TimetableSlot
- circulars/use_cases.py
- calendar.py
- test_initials_matching.py
- Circular
- Stage 07: Meeting circular scanning, extraction and review queue
- test_circular_full_pipeline_with_samples
- bulk_import.py
- test_calendar_pipeline.py
- Stage 02: Domain model and persistence (OOAD core)
- delete_task

## God Nodes (most connected - your core abstractions)
1. `UnitOfWork` - 182 edges
2. `Clock` - 111 edges
3. `Principal` - 95 edges
4. `FacultyProfile` - 81 edges
5. `ScheduledNotification` - 80 edges
6. `Event` - 72 edges
7. `User` - 64 edges
8. `NotFoundError` - 57 edges
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

## Communities (152 total, 27 thin omitted)

### Community 0 - "datetime"
Cohesion: 0.09
Nodes (35): OCR and Parsing Engineer, Responsibilities, Rules, compute_deskew_angle(), deskew_image(), has_pdf_text_layer(), preprocess_image_for_ocr(), split_co_teachers() (+27 more)

### Community 1 - "server.cjs"
Cohesion: 0.05
Nodes (57): bootstrapPage(), brandMarkup(), broadcast(), browserLauncherForPlatform(), chmodOwnerOnly(), clients, companionUrl(), computeAcceptKey() (+49 more)

### Community 3 - "ReminderPlanner"
Cohesion: 0.30
Nodes (4): CancelEventUseCase, CheckClashesUseCase, MaterialiseTimetableEventsUseCase, ReminderPlanner

### Community 4 - "get_settings"
Cohesion: 0.31
Nodes (5): _build_dispatcher(), dispatch_due_notifications(), recover_stale_sending_notifications(), _run_dispatch(), _run_recover()

### Community 5 - "domain/__init__.py"
Cohesion: 0.05
Nodes (9): AuditLogRepository, CircularRepository, CourseRepository, EventRepository, PushSubscriptionRepository, RefreshTokenRepository, ReminderRuleRepository, SectionRepository (+1 more)

### Community 6 - "UUID"
Cohesion: 0.14
Nodes (4): PushSubscriptionModel, EventRepositoryImpl, push_subscription_to_domain(), PushSubscriptionRepositoryImpl

### Community 7 - "SqlAlchemyUnitOfWork"
Cohesion: 0.23
Nodes (10): SystemClock, materialise_all_timetable_events(), materialise_timetable_upload(), _run_materialisation(), process_circular_upload(), _run_process_circular(), _run_schedule_daily_overdue_alerts(), _run_schedule_hod_escalations() (+2 more)

### Community 8 - "db/repositories.py"
Cohesion: 0.20
Nodes (20): Base, AcademicTermModel, AuditLogModel, CourseModel, DepartmentModel, EventAttendeeModel, EventModel, FacultyProfileModel (+12 more)

### Community 9 - "main.py"
Cohesion: 0.10
Nodes (6): configure_logging(), RequestIdMiddleware, domain_exception_handler(), healthz(), lifespan(), readyz()

### Community 10 - "demo_setup.py"
Cohesion: 0.13
Nodes (8): is_server_ready(), main(), main(), http_get_json(), http_post_json(), http_post_multipart(), run_demo_setup(), main()

### Community 11 - "sqlalchemy"
Cohesion: 0.17
Nodes (5): upgrade(), upgrade(), upgrade(), upgrade(), upgrade()

### Community 12 - "Clock"
Cohesion: 0.08
Nodes (14): compute_completion_rate(), AssignmentProgress, AssignTaskUseCase, CreateTaskUseCase, FacultyOverdueSummary, GetHodDashboardUseCase, HodDashboardData, ListTasksUseCase (+6 more)

### Community 13 - "directory.py"
Cohesion: 0.08
Nodes (29): get_clock(), get_current_principal(), get_uow(), require_admin(), require_hod_or_admin(), AcademicTermResponse, add_holiday(), bulk_import_faculty() (+21 more)

### Community 15 - "Task"
Cohesion: 0.12
Nodes (7): Task, TaskRepository, TaskCategory, TaskRecurrence, TaskStatus, task_to_domain(), TaskRepositoryImpl

### Community 16 - "get_settings"
Cohesion: 0.12
Nodes (9): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), get_settings(), Settings, get_storage_service(), process_timetable_upload() (+1 more)

### Community 17 - "security.py"
Cohesion: 0.17
Nodes (15): ChangePasswordUseCase, LoginResult, LoginUseCase, LogoutUseCase, RefreshResult, RefreshTokenUseCase, UnauthorizedError, create_access_token() (+7 more)

### Community 18 - "Department"
Cohesion: 0.14
Nodes (6): Department, DepartmentRepository, UserRepository, department_to_domain(), DepartmentRepositoryImpl, Stage 02: Domain model and persistence (OOAD core)

### Community 19 - "Test-Driven Development (TDD)"
Cohesion: 0.06
Nodes (29): Common Rationalizations, Debugging Integration, Example: Bug Fix, Final Rule, Good Tests, GREEN - Minimal Code, Overview, Red Flags - STOP and Start Over (+21 more)

### Community 20 - "reminders.py"
Cohesion: 0.12
Nodes (11): delete_push_subscription(), DeletePushSubscriptionRequest, get_quiet_hours(), get_upcoming_notifications(), get_vapid_public_key(), PushSubscriptionRequest, QuietHoursResponse, ScheduledNotificationResponse (+3 more)

### Community 21 - "AcademicTerm"
Cohesion: 0.14
Nodes (6): AcademicTerm, Holiday, AcademicTermRepository, academic_term_to_domain(), AcademicTermRepositoryImpl, holiday_to_domain()

### Community 22 - "deps.py"
Cohesion: 0.08
Nodes (24): name, packageManager, private, version, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react (+16 more)

### Community 23 - "Visual Companion Guide"
Cohesion: 0.09
Nodes (20): 1. Take the task, 2. Work the steps, 3. The completion contract, 4. Complete the task, Common Rationalizations, Executing Plans, Final Review, Finish (+12 more)

### Community 24 - "Circular"
Cohesion: 0.16
Nodes (11): CircularDetailResponse, CircularUploadResponse, confirm_circular(), ConfirmCircularRequest, ConfirmCircularResponse, get_circular(), list_review_queue(), reject_circular() (+3 more)

### Community 25 - "Principal"
Cohesion: 0.20
Nodes (9): update_faculty(), CreateFacultyUseCase, UpdateFacultyUseCase, Principal, ConfirmTimetableUseCase, UploadTimetableUseCase, ConflictError, AuditLog (+1 more)

### Community 26 - "NotFoundError"
Cohesion: 0.21
Nodes (10): DeactivateFacultyUseCase, ManageTermsUseCase, AuthorisationPolicy, FacultyDeskError, ForbiddenError, InvalidTransition, NotFoundError, test_admin_policy_allows_all() (+2 more)

### Community 27 - "auth.py"
Cohesion: 0.18
Nodes (14): change_password(), ChangePasswordRequest, CurrentUserResponse, _get_client_ip(), get_me(), login(), LoginRequest, LoginResponse (+6 more)

### Community 28 - "test_ocr_maths.py"
Cohesion: 0.20
Nodes (11): compute_length_weighted_confidence(), test_confidence_bounds_property(), test_confidence_empty_tokens(), test_length_weighted_document_confidence(), test_meeting_time_grammar_table(), test_review_gate_decision_matrix(), 6.1 Document Confidence: Length-Weighted Mean, 6.3 Field Confidence Rules and Review Queue Gate Predicate (+3 more)

### Community 29 - "update_task"
Cohesion: 0.17
Nodes (9): assign_task(), complete_task(), create_task(), ensure_utc(), get_task(), list_tasks(), reopen_task(), TaskResponse (+1 more)

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
Cohesion: 0.33
Nodes (10): DomainEvent, EventCancelled, EventRescheduled, EventScheduled, TaskCreated, TaskDeadlineChanged, TimetableConfirmed, Domain (backend/app/domain) (+2 more)

### Community 34 - "InvariantViolation"
Cohesion: 0.12
Nodes (4): Course, InvariantViolation, course_to_domain(), CourseRepositoryImpl

### Community 35 - "CircularRepository"
Cohesion: 0.48
Nodes (3): CircularModel, circular_to_domain(), CircularRepositoryImpl

### Community 36 - "dataclasses"
Cohesion: 0.27
Nodes (3): OcrEngine, OcrResult, WordBox

### Community 37 - "QuietHours"
Cohesion: 0.15
Nodes (13): adjust_for_quiet_hours(), compute_backoff_delay(), compute_fire_time(), compute_idempotency_key(), QuietHours, test_quiet_hours_midnight_crossing(), test_backoff_bounds(), test_fire_time_computation() (+5 more)

### Community 38 - "FacultyProfile"
Cohesion: 0.14
Nodes (6): FacultyProfile, FacultyProfileRepository, Initials, faculty_profile_to_domain(), FacultyProfileRepositoryImpl, 4.1.3 Core Domain Classes and Rationales

### Community 40 - "reminders.py"
Cohesion: 0.12
Nodes (15): get_reminder_rules(), ReminderRuleResponse, update_reminder_rule(), UpdateReminderRuleRequest, DeletePushSubscriptionUseCase, GetUpcomingNotificationsUseCase, GetUserQuietHoursUseCase, GetUserReminderRulesUseCase (+7 more)

### Community 41 - "calendar/__init__.py"
Cohesion: 0.20
Nodes (7): BusyInterval, FreeSlotFinder, merge_busy_intervals(), FindFreeSlotsUseCase, GetCalendarEventsUseCase, test_free_slots_never_intersect_busy_property(), test_free_slots_worked_example()

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

### Community 47 - "clock.py"
Cohesion: 0.29
Nodes (5): FrozenClock, test_clock_always_returns_utc_property(), test_frozen_clock_advance_property(), test_frozen_clock_rejects_naive_datetime(), 1.1 Canonical Time Representation and Clock Invariant

### Community 48 - "FacultyProfile"
Cohesion: 0.11
Nodes (8): ReminderDispatcher, NotificationPayload, Notifier, EmailNotifier, CompositeNotifier, WebPushNotifier, ConcurrentMockNotifier, test_mailpit_real_delivery()

### Community 49 - "Section"
Cohesion: 0.13
Nodes (15): dependencies, clsx, @fullcalendar/core, @fullcalendar/daygrid, @fullcalendar/react, @fullcalendar/timegrid, @hookform/resolvers, lucide-react (+7 more)

### Community 50 - "circulars/use_cases.py"
Cohesion: 0.26
Nodes (12): compute_lateness_percentiles(), ValidationError, detect_mime_and_extension(), validate_upload_content(), test_compute_lateness_percentiles_100_elements(), test_compute_lateness_percentiles_empty(), test_compute_lateness_percentiles_single(), test_detect_mime_and_extension_invalid() (+4 more)

### Community 51 - "Section"
Cohesion: 0.36
Nodes (3): Section, section_to_domain(), SectionRepositoryImpl

### Community 53 - "deps.py"
Cohesion: 0.18
Nodes (7): get_redis(), AdminMetricsResponse, DeadLetterResponse, get_system_metrics(), LatenessPercentilesResponse, QueueDepthResponse, retry_failed_notification()

### Community 54 - "Room"
Cohesion: 0.30
Nodes (4): Room, RoomRepository, room_to_domain(), RoomRepositoryImpl

### Community 55 - "helper.js"
Cohesion: 0.17
Nodes (11): Applying the Pattern, Defense-in-Depth Validation, Example from Session, Key Insight, Layer 1: Entry Point Validation, Layer 2: Business Logic Validation, Layer 3: Environment Guards, Layer 4: Debug Instrumentation (+3 more)

### Community 56 - "Brainstorming"
Cohesion: 0.17
Nodes (11): Execution Handoff, File Structure, Overview, Plan Document Header, Scope Check, Self-Review, Step Granularity, Task Right-Sizing (+3 more)

### Community 57 - "Event"
Cohesion: 0.22
Nodes (14): CreateEventUseCase, UpdateEventUseCase, Event, EventAttendee, AttendeeResponse, EventKind, Role, event_to_domain() (+6 more)

### Community 58 - "RefreshToken"
Cohesion: 0.24
Nodes (4): RefreshToken, RefreshTokenModel, refresh_token_to_domain(), RefreshTokenRepositoryImpl

### Community 59 - "Web Application Testing"
Cohesion: 0.15
Nodes (13): devDependencies, eslint, eslint-config-next, openapi-typescript, @playwright/test, prettier, prettier-plugin-tailwindcss, tailwindcss (+5 more)

### Community 60 - "User"
Cohesion: 0.16
Nodes (12): CompleteTaskUseCase, get_db(), hash_password(), User, SqlAlchemyUnitOfWork, main(), seed_database(), test_hod_dashboard_aggregation() (+4 more)

### Community 61 - "NotificationRepositoryImpl"
Cohesion: 0.18
Nodes (10): Brainstorming, First: What Do You Actually Know?, Look Before You Ask, Play It Back, Red Flags, Size the Work, The Conversation, The Written Design (+2 more)

### Community 62 - "4.3 Standard OOAD Diagram Pack"
Cohesion: 0.07
Nodes (26): 1. Problem and users, 3. Architecture, 4.1.1 Actors and System Goals, 4.1 Evaluator Summary (10-Minute Read), 4.3.10 Deployment Diagram: Production & College-LAN Topology, 4.3.11 Entity-Relationship (ER) Diagram, 4.3.12 Collaboration Diagram: Meeting Circular Processing, Confirmation & Reminder Dispatch, 4.3.13 Package Diagram: System Modules, Layer Dependencies & Clean Architecture Boundaries (+18 more)

### Community 63 - "TimetableUpload"
Cohesion: 0.12
Nodes (12): TimetableUpload, InvalidTransition, TimetableUploadRepository, timetable_upload_to_domain(), TimetableUploadRepositoryImpl, Acceptance criteria, Goal, Input formats to support (+4 more)

### Community 64 - "celery_app.py"
Cohesion: 0.19
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

### Community 69 - "tasks.py"
Cohesion: 0.20
Nodes (10): AssignmentProgressResponse, AssignTaskRequest, CreateTaskRequest, FacultyOverdueSummaryResponse, get_hod_dashboard(), HodDashboardResponse, list_templates(), TaskTemplateResponse (+2 more)

### Community 70 - "FacultyDesk Maths"
Cohesion: 0.06
Nodes (30): 10.1 Token Lifetimes, Rotation, and Family Reuse Detection, 10.2 Role-Based Access Control (RBAC) Ownership Policy Matrix, 10.3 Sliding Window Log Rate Limiting, 10. Security Limits, 11.1 Dispatch Lateness Percentile Computation, 11.2 Backup Retention Arithmetic & Bounded Pruning, 11.3 Upload Decompression Bomb and Page Count Limits, 11. Hardening, Observability and Reliability (+22 more)

### Community 71 - "directory/page.tsx"
Cohesion: 0.09
Nodes (36): nextConfig, CalendarPage(), CircularsPage(), DirectoryPage(), metadata, RootLayout(), viewport, LoginPage() (+28 more)

### Community 72 - "Graphify Protocol"
Cohesion: 0.25
Nodes (7): Best Practices, Common Pitfall, Decision Tree: Choosing Your Approach, Example: Using with_server.py, Reconnaissance-Then-Action Pattern, Reference Files, Web Application Testing

### Community 74 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.15
Nodes (10): Acceptance criteria, Goal, Maths to specify first, Stage 05: Calendar core, recurrence, clash detection, ICS feed, Tests, Acceptance criteria, Goal, Maths to specify first (+2 more)

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
Cohesion: 0.23
Nodes (12): CircularExtractor, ExtractedAttendee, ExtractedTime, ExtractionResult, parse_meeting_date(), parse_meeting_time(), parse_military_time(), parse_title_and_agenda() (+4 more)

### Community 80 - "TaskTemplate"
Cohesion: 0.50
Nodes (4): TaskTemplate, TaskTemplateModel, task_template_to_domain(), TaskTemplateRepositoryImpl

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
Cohesion: 0.20
Nodes (3): PushSubscriptionResponse, register_push_subscription(), PushSubscription

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
Cohesion: 0.11
Nodes (11): get_storage(), confirm_timetable(), ConfirmTimetableResponse, get_faculty_slots(), get_timetable_upload(), TimetableSlotResponse, TimetableUploadDetailResponse, upload_timetable() (+3 more)

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

### Community 113 - "compute_priority_score"
Cohesion: 0.23
Nodes (12): compute_lead_alert_times(), compute_overdue_alert_times(), compute_priority_score(), test_completed_task_priority(), test_lead_alert_times(), test_overdue_alert_times(), test_priority_bounds_property_active(), test_priority_bounds_property_overdue() (+4 more)

### Community 114 - "Stage 01: Foundation, environment, Graphify, trusted skills"
Cohesion: 0.40
Nodes (4): Acceptance criteria, Goal, Stage 01: Foundation, environment, Graphify, trusted skills, Tasks

### Community 124 - "Stage 03: Authentication, authorization, and faculty directory"
Cohesion: 0.17
Nodes (8): BackupService, backup_database_to_minio(), test_backup_prune_expired(), test_backup_prune_preserves_single_expired_backup(), FacultyDesk Decisions, Stage 00: Agent setup, Stage 01: Foundation, environment, Graphify, trusted skills, Stage 03: Authentication, authorization, and faculty directory

### Community 127 - "ScheduledNotification"
Cohesion: 0.08
Nodes (5): ScheduledNotification, NotificationRepository, NotificationStatus, notification_to_domain(), NotificationRepositoryImpl

### Community 131 - "pytest"
Cohesion: 0.21
Nodes (9): cleanup_db_connections(), test_circular_state_machine_exhaustive(), test_event_invariants(), test_initials_invalid_property(), test_initials_valid_property(), test_notification_state_machine_exhaustive(), test_task_invariants(), test_timeslot_invariants() (+1 more)

### Community 135 - "clash_detector.py"
Cohesion: 0.33
Nodes (8): Interval, intervals_overlap(), pairwise_clashes(), SweepLineClashDetector, test_adjacent_intervals_no_clash(), test_sweep_line_clash_detection_matches_pairwise_property(), test_worked_example_from_maths_md(), 2.2 Sweep-Line Interval Clash Detection Algorithm

### Community 138 - "RedisSlidingWindowRateLimiter"
Cohesion: 0.27
Nodes (5): get_rate_limiter(), RateLimitExceededError, get_redis_client(), RedisSlidingWindowRateLimiter, test_sliding_window_rate_limiter()

### Community 139 - "value_objects.py"
Cohesion: 0.29
Nodes (8): generate_vcalendar_ics(), EventSource, test_ics_export_stable_uids(), test_ics_export_valid_rfc5545(), 2.1 Half-Open Overlap Predicate, 2.3 Multi-Attendee Common Free-Slot Finder, 2.4 RFC 5545 ICS Feed Specification, 2. Clash Detection and Calendar Operations

### Community 140 - "TimetableSlot"
Cohesion: 0.13
Nodes (11): expand_slot_recurrence(), TimetableSlot, TimetableSlotRepository, TimeSlot, timetable_slot_to_domain(), TimetableSlotRepositoryImpl, test_timeslot_half_open_overlap(), test_recurrence_expansion_matching_weekday() (+3 more)

### Community 141 - "circulars/use_cases.py"
Cohesion: 0.24
Nodes (5): GetCircularUseCase, ProcessCircularUseCase, RejectCircularUseCase, UploadCircularUseCase, rasterise_pdf_page()

### Community 142 - "calendar.py"
Cohesion: 0.13
Nodes (14): CalendarEventResponse, cancel_calendar_event(), check_event_clashes(), CheckClashesRequest, create_calendar_event(), CreateEventRequest, EventAttendeeResponse, find_common_free_slots() (+6 more)

### Community 143 - "test_initials_matching.py"
Cohesion: 0.25
Nodes (8): InitialsResolver, normalized_similarity(), ResolutionOutcome, test_ambiguity_threshold_rejection(), test_cell_tokenization_topologies(), test_exact_and_alias_resolution(), test_normalized_similarity_properties(), 5.3 Initials Resolution via Normalized Levenshtein Distance

### Community 144 - "Circular"
Cohesion: 0.22
Nodes (3): Circular, CircularStatus, test_round_trip_all_aggregates()

### Community 145 - "Stage 07: Meeting circular scanning, extraction and review queue"
Cohesion: 0.29
Nodes (6): Acceptance criteria, Corpus and tests, Goal, Maths to specify first, Pipeline, Stage 07: Meeting circular scanning, extraction and review queue

### Community 146 - "test_circular_full_pipeline_with_samples"
Cohesion: 0.18
Nodes (3): InMemoryStorageService, sample_dir(), test_circular_full_pipeline_with_samples()

### Community 147 - "bulk_import.py"
Cohesion: 0.33
Nodes (3): BulkImportFacultyUseCase, BulkImportReport, RowImportResult

### Community 148 - "test_calendar_pipeline.py"
Cohesion: 0.15
Nodes (9): get_ics_feed(), GenerateIcsFeedUseCase, RotateIcsTokenUseCase, ClashDetectedError, ConflictError, DomainError, EntityNotFound, TimetableUploadStatus (+1 more)

### Community 150 - "Stage 02: Domain model and persistence (OOAD core)"
Cohesion: 0.25
Nodes (7): Acceptance criteria, Diagrams, Goal, Maths to specify first (MATHS.md), Persistence, Stage 02: Domain model and persistence (OOAD core), Tests

## Knowledge Gaps
- **22 isolated node(s):** `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core`, `@fullcalendar/daygrid`, `@fullcalendar/react` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 850 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UnitOfWork` connect `UnitOfWork` to `ReminderPlanner`, `domain/__init__.py`, `db/repositories.py`, `Clock`, `directory.py`, `calendar.py`, `circulars/use_cases.py`, `get_settings`, `security.py`, `Department`, `bulk_import.py`, `test_calendar_pipeline.py`, `reminders.py`, `Stage 02: Domain model and persistence (OOAD core)`, `delete_task`, `Circular`, `Principal`, `NotFoundError`, `auth.py`, `update_task`, `domain/__init__.py`, `QuietHours`, `reminders.py`, `calendar/__init__.py`, `FacultyProfile`, `deps.py`, `Event`, `User`, `tasks.py`, `PushSubscription`, `timetable.py`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 52 inferred relationships involving `UnitOfWork` (e.g. with `cancel_calendar_event()` and `check_event_clashes()`) actually correct?**
  _`UnitOfWork` has 52 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RFC-6455`, `facultydesk-backend`, `@fullcalendar/core` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `datetime` be split into smaller, more focused modules?**
  _Cohesion score 0.09230769230769231 - nodes in this community are weakly interconnected._
- **Why does `Event` connect `Event` to `ReminderPlanner`, `pytest`, `domain/__init__.py`, `UUID`, `db/repositories.py`, `value_objects.py`, `Clock`, `circulars/use_cases.py`, `calendar.py`, `Task`, `Circular`, `test_circular_full_pipeline_with_samples`, `Department`, `Circular`, `test_ocr_maths.py`, `domain/__init__.py`, `InvariantViolation`, `QuietHours`, `FacultyProfile`, `calendar/__init__.py`, `duplicate_detector.py`, `User`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Clock` (e.g. with `Standards you are held to` and `Non-negotiables`) actually correct?**
  _`Clock` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Should `server.cjs` be split into smaller, more focused modules?**
  _Cohesion score 0.05034965034965035 - nodes in this community are weakly interconnected._