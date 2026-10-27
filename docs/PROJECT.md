# FacultyDesk

## 1. Problem and users

Faculty juggle classes from a timetable, meetings announced on paper circulars, and documentation deadlines. Today these live in different places and reminders depend on memory. FacultyDesk puts all of it on one calendar and reminds each person at the right time.

| Actor | Goal |
|---|---|
| Admin | Manage departments, faculty directory, terms and holidays |
| HOD | Upload timetables, review circulars, assign documentation tasks, see progress |
| Faculty | See classes and meetings, get reminders, track own tasks |
| Scheduler (system) | Plan and send reminders, refresh calendars nightly |

## 2. Features that exist now

- Monorepo foundation with backend (FastAPI, Python 3.12, SQLAlchemy 2 async, Alembic, Celery, Redis, MinIO) and frontend (Next.js 16 App Router, TypeScript strict, Tailwind, shadcn/ui).
- Injected `Clock` system (`SystemClock`, `FrozenClock`) with mathematical invariants proving canonical UTC handling.
- Structured JSON logging (`structlog`) with distributed request ID tracking (`X-Request-ID`).
- Health probes: `/healthz` (liveness) and `/readyz` (dependency readiness probing PostgreSQL `SELECT 1`, Redis `PING`, and MinIO bucket verification).
- Interactive Frontend dashboard displaying real-time system readiness probe status.
- Framework-free domain layer (`Department`, `User`, `FacultyProfile`, `Initials`, `AcademicTerm`, `Holiday`, `Room`, `Course`, `Section`, `TimetableUpload`, `TimetableSlot`, `Event`, `EventAttendee`, `Circular`, `ScheduledNotification`, `ReminderRule`, `PushSubscription`, `Task`, `AuditLog`, `RefreshToken`).
- Deterministic finite state machines for `Circular` (7 transitions) and `ScheduledNotification` (5 transitions) raising typed `InvalidTransition` on illegal transitions.
- Fully reversible Alembic migrations (`8f3198838ebd_initial_schema.py`, `8434d6a0dd0a_add_refresh_tokens.py`) supporting database schema creation, token rotation, and rollback.
- Async SQLAlchemy repository implementations and `SqlAlchemyUnitOfWork`.
- Authentication system with Argon2id password hashing, 15-minute HS256 access JWTs, and rotating 7-day refresh tokens delivered via httpOnly cookies.
- Refresh token family reuse detection automatically revoking all tokens in a compromised family upon re-presentation.
- Centralized `AuthorisationPolicy` evaluating ownership predicates across `ADMIN`, `HOD`, and `FACULTY` roles.
- Redis-backed Sliding Window Log rate limiter protecting `/api/auth/login` (5/min per IP and account) and `/api/auth/refresh` (30/min per IP).
- Faculty directory management with department CRUD, individual faculty creation/updates, deactivation, and bulk CSV/XLSX import with validation reports.
- Academic calendar terms and holidays management supporting single entry and bulk CSV imports.
- Synthetic database seeder (`make seed`) populating CSE department, Admin, HOD, faculty profiles, academic term, and holidays.
- Multi-format Timetable Ingestion engine supporting XLSX (with merged-cell period expansion), long-format CSV, and text-layer PDF with table extraction.
- Deterministic 3-tier initials resolution (exact initials -> exact alias -> bounded normalized Levenshtein similarity with theta_sim >= 0.85 and theta_margin >= 0.10) preventing false matches.
- Celery worker asynchronous parsing pipeline generating preview slots and detailed unmapped token issue reports.
- Two-phase upload & confirm workflow creating `Course`, `Section`, `Room`, and `TimetableSlot` entities, and emitting `TimetableConfirmed` domain events.
- Rolling 21-day class recurrence materialisation pipeline expanding weekly timetable slots, respecting term boundaries, and skipping academic holidays.
- Sweep-line clash detection algorithm ($O(n \log n)$) evaluating half-open intervals $\max(s_1, s_2) < \min(e_1, e_2)$ across multiple attendees, with explicit override capability returning 409 Conflict with clash details.
- Multi-attendee common free-slot finder detecting non-overlapping working intervals for meeting scheduling.
- RFC 5545 compliant iCalendar (`.ics`) subscription feed with token gating, automatic token rotation, and stable UIDs (`slot-<slot_id>-<date>@facultydesk.local`).
- Celery Beat nightly rolling materialisation task automatically advancing the 21-day window at midnight.
- Multi-channel notification engine (HTML/text Email via aiosmtplib and WebPush via pywebpush with VAPID) delivering reminders for classes and meetings.
- Exactly-once reminder delivery guarantees with deterministic SHA-256 idempotency keys, atomic `SELECT FOR UPDATE SKIP LOCKED` batch claiming, and full-jitter exponential backoff retry scheduling.
- Stale `SENDING` notification worker recovery protecting against worker crashes.
- Configurable reminder rules per event kind (`CLASS`, `MEETING`, `DEADLINE`) with offsets and channel preferences.
- User-specific quiet hours window ($Q = [q_s, q_e)$) supporting midnight-crossing windows and emergency morning class start exemptions.
- Meeting circular upload pipeline supporting PDFs, PNG, and JPEG up to 15 MB with byte-level MIME validation.
- OCR preprocessing engine: Grayscale conversion, Non-Local Means denoising, Adaptive Gaussian thresholding, and Minimum-Area Bounding Rectangle deskewing ($|\theta| \ge 0.5^\circ$).
- Dual-PSM Tesseract OCR engine (PSM 6 uniform text block with PSM 4 variable column/table layout fallback) computing length-weighted document confidence $C = \frac{\sum \operatorname{len}(w_i) \cdot c_i}{\sum \operatorname{len}(w_i)}$.
- Field extraction engine: Date parsing with cue-word priority (`meeting on`, `held on`), regular meeting time grammar $\mathcal{G}_{\text{meeting\_time}}$ (handling 5 time formats with assumed 60-minute duration invariant), venue extraction, and attendee resolution (exact initials, aliases, fuzzy full name, and "all faculty" mapping).
- Review queue gate predicate protecting faculty calendars, routing low-confidence or unconfirmed circulars to HOD review with human-readable reasons.
- Duplicate detection predicate checking calendar day, start time window ($\pm 15$m), and normalized title similarity against existing events.
- Circular confirmation workflow creating `MEETING` events on all attendees' calendars and scheduling multi-channel Stage 06 reminders.
- Task management and assignment system: Personal documentation task creation, HOD bulk assignment to individual faculty, multiple faculty, or department-wide with unique `parent_assignment_id`.
- Transparent Task Priority Scoring engine ($P \in [0, 1]$ for active tasks, $P \in (1, 2]$ for overdue tasks, $-1.0$ for completed tasks) balancing importance ($w_I = 0.4$) and exponential decay urgency ($w_U = 0.6, \tau = 48\text{h}$).
- Standard departmental task templates seeded via `make seed` (CO-PO mapping, IA marks upload, attendance shortage report, lab manual update, course file submission) with pre-filled category, importance, and lead days.
- Multi-tier alert schedule set ($\{D-72\text{h}, D-24\text{h}, D-2\text{h}\}$, daily overdue reminders at 09:00 IST, and 24h HOD escalation summaries at 09:30 IST) with strict exactly-once delivery.
- Automatic calendar synchronization establishing `DEADLINE` events (`EventKind.DEADLINE`) for every task, linked to task lifecycle.
- Full task lifecycle management: Completion automatically cancels all pending alerts, while reopening reactivates alerts for future deadlines.
- HOD dashboard analytics calculating assignment completion rates ($\frac{N_{\text{completed}}}{N_{\text{total}}} \times 100\%$) and per-faculty overdue counts.
- Installable Progressive Web App (PWA) with standard manifest (`standalone` display, theme `#1e3a8a`, background `#f8fafc`) and custom service worker (`sw.js`) with offline caching, push notifications, and deep links.
- Responsive mobile-first AppShell layout featuring a collapsible desktop sidebar and sticky bottom navigation bar supporting mobile viewports down to 360px.
- End-to-end typed API client mapped to OpenAPI 3.1 contracts via `openapi-typescript` generation, with silent refresh rotation and access token storage in-memory.
- Full suite of frontend screens: `/today` (countdown & timeline), `/calendar` (day/week/list + clash overrides + free-slots modal), `/timetables` (drag & drop ingestion + issue audit), `/circulars` (camera capture + confidence review queue), `/tasks` (priority score ranking + HOD cohort assignment), `/settings` (WebPush, quiet hours, ICS feed token), `/directory` (roster, term & holiday setup), and `/login` (quick switcher for Admin, HOD, and Faculty).
- Comprehensive perimeter security headers: Content-Security-Policy, Strict-Transport-Security (HSTS), X-Content-Type-Options: nosniff, X-Frame-Options: DENY, Referrer-Policy, and Permissions-Policy configured across Caddy and Next.js.
- File upload safety guard: Byte-level magic header MIME sniffing (PDF, PNG, JPEG, XLSX, CSV), decompression bomb defense limiting image dimensions to $\Pi \le 25,000,000$ pixels, PDF page bound ($P \le 30$ pages), 15 MB file size limit, and randomized UUID storage keys.
- Automated database backup and streaming restore (`BackupService`): Scheduled nightly PostgreSQL backups (`pg_dump` compressed with gzip) streamed to MinIO S3 bucket `backups` with a rolling 14-day retention horizon ($T_{\text{horizon}} = 1,209,600\text{s}$) and non-destructive streaming `psql` restore pipeline.
- Observability and reliability metrics API: `GET /api/admin/metrics` returning real-time notification status counts, Celery queue depth, lateness percentiles ($p_{50}, p_{95}, p_{99}$), and dead-letter queue; paired with `POST /api/admin/notifications/{id}/retry` for admin dead-letter reprocessing.
- Celery worker resilience: Distributed request ID context tracing, soft timeout (300s), hard timeout (360s), and worker prefetch multiplier 1.
- Database index optimization verified with EXPLAIN ANALYZE on a 120-faculty, 5,000-task, 2-term workload (1-week calendar query p95 = 0.60ms, 1,000 notification batch claim = 0.0012s).
- Docker Compose development and production environments with health checks on all services including Mailpit SMTP testing server.
- Knowledge graph indexing with Graphify and verified trusted skills suite.

## 3. Architecture

```mermaid
flowchart LR
    U["Faculty / HOD / Admin<br/>Browser / PWA"] --> C["Caddy Reverse Proxy"]
    C --> F["Next.js Frontend (:3000)"]
    C --> A["FastAPI Backend (:8000)"]
    A --> P[("PostgreSQL 16")]
    A --> R[("Redis 7")]
    A --> M[("MinIO S3")]
    W["Celery Worker"] --> P
    W --> M
    W --> R
    B["Celery Beat"] --> R
```

## 4. OOAD Design and Architecture

### 4.1 Evaluator Summary (10-Minute Read)

FacultyDesk is designed following strict Clean Architecture and Object-Oriented Analysis and Design (OOAD) principles. The software coordinates academic timetables, OCR-scanned paper circulars, personal calendars, and departmental task deadlines into a single automated, clash-aware schedule.

#### 4.1.1 Actors and System Goals
- **Admin**: System-wide configuration, department management, academic term boundaries, institution-wide holidays, and faculty directory administration.
- **HOD (Head of Department)**: Department timetable ingestion, unmapped initials review, paper circular confirmation, cohort task assignment, and compliance monitoring.
- **Faculty**: Personal schedule inspection across classes and meetings, schedule clash detection/override, token-gated RFC 5545 ICS feeds, personal and assigned task completion, and notification lead-time / quiet-hour preferences.
- **System Scheduler (Celery Beat & Workers)**: Periodic background tasks executing atomic `SKIP LOCKED` reminder dispatches (30s interval), nightly calendar recurrence materialisation (00:00 UTC), overdue task escalation summaries (09:30 IST), and automated database backups (02:00 UTC).

#### 4.1.2 Clean Architecture Layer Isolation
The backend codebase (`backend/app/`) enforces a unidirectional inward dependency rule across four isolated layers:
1. **Domain Layer (`domain/`)**: Pure business logic containing entities (`Event`, `Task`, `Circular`, `ScheduledNotification`), value objects (`Initials`, intervals), domain services (`SweepLineClashDetector`, `InitialsResolver`, `ReminderLeadTimeCalculator`, `TaskPriorityCalculator`), and repository interfaces (`EventRepository`, `TaskRepository`, etc.). **Law**: Zero dependencies on FastAPI, SQLAlchemy, Celery, Redis, or any I/O library.
2. **Application Layer (`application/`)**: Use cases orchestrating business flows (`CreateEventUseCase`, `ProcessCircularUseCase`, `AssignTaskUseCase`, `DispatchDueNotificationsUseCase`). Depends solely on domain abstractions and Unit of Work interfaces.
3. **Infrastructure Layer (`infrastructure/`)**: Concrete implementations of domain interfaces. Contains SQLAlchemy 2 async models, asyncpg repository adapters, Tesseract OCR wrappers, OpenCV image preprocessors, MinIO S3 object storage clients, and aiosmtplib / pywebpush notification senders.
4. **API Layer (`api/`)**: FastAPI routing, OpenAPI schema generation, HTTP header processing, authentication dependency wiring, and rate limiting.

#### 4.1.3 Core Domain Classes and Rationales
- **`Event` & `EventAttendee`**: Aggregate root representing any scheduled calendar interval $[s, e)$ in canonical UTC. Maintains recurrence invariants and attendee RSVP states.
- **`Circular`**: Aggregate managing the lifecycle of an uploaded meeting document, tracking dual-PSM OCR text, length-weighted confidence score, and extracted structured metadata.
- **`ScheduledNotification`**: Represents a scheduled communication channel delivery event. Governed by a state machine ensuring atomic dispatch, deterministic SHA-256 idempotency, and full-jitter exponential backoff retries.
- **`Task`**: Prioritised documentation task tracker with mathematical urgency-importance scoring ($P \in [0, 2]$), calendar synchronization (`DEADLINE` event), and multi-tier alert triggers.
- **`FacultyProfile` & `Initials`**: Encapsulates faculty identity, institutional initials (e.g. `KKS`), aliases, and token-gated ICS feed secrets.
- **`TimetableUpload` & `TimetableSlot`**: Aggregates for raw timetable files (XLSX, CSV, PDF), holding extracted grid cells, resolved faculty mappings, and unmapped tokens awaiting HOD review.
- **`RefreshToken`**: Security entity supporting rotating refresh token families with automated replay detection and revocation.

#### 4.1.4 Design Patterns in Codebase
| Design Pattern | Concrete Class(es) in Code | Purpose |
|---|---|---|
| **Repository** | `SqlAlchemyEventRepository`, `SqlAlchemyTaskRepository`, `SqlAlchemyCircularRepository`, `SqlAlchemyNotificationRepository` | Decouples domain logic from SQL schema and query construction |
| **Unit of Work** | `SqlAlchemyUnitOfWork` | Coordinates atomic transactional boundaries across multiple repositories |
| **Strategy** | `XlsxTimetableParser`, `CsvTimetableParser`, `PdfTimetableParser` | Encapsulates format-specific parsing algorithms behind `TimetableParser` interface |
| **Strategy (Notification)** | `EmailNotificationSender`, `WebPushNotificationSender`, `CompositeNotifier` | Decouples message delivery channel mechanics from dispatch orchestration |
| **Factory** | `TimetableParserFactory` | Dynamically instantiates the correct parser strategy based on sniffed magic bytes |
| **Observer (Domain Events)** | `TimetableConfirmed`, `CircularProcessed`, `TaskCompleted` | Decouples event generation from background materialisation and notification scheduling |
| **State** | `CircularStatus` (`Circular.start_processing()`, `mark_needs_review()`, `confirm()`, `fail()`), `NotificationStatus` (`ScheduledNotification.mark_sending()`, `mark_sent()`, `mark_failed()`) | Enforces legal lifecycle transitions via formal mathematical state algebras |

---

### 4.2 Requirements Traceability Matrix

Every functional requirement specified for FacultyDesk maps directly to use cases, domain classes, REST endpoints, UI screens, and verification tests:

| Requirement | Use Case Class | Domain Classes | REST Endpoints | Frontend Screen | Proof Test Name |
|---|---|---|---|---|---|
| **Timetable Upload & Ingestion** | `IngestTimetableUseCase`, `ConfirmTimetableUseCase` | `TimetableUpload`, `TimetableSlot`, `Course`, `Section`, `Room` | `POST /api/timetables/upload`, `GET /api/timetables/{id}`, `POST /api/timetables/{id}/confirm` | `/timetables` | `test_timetable_pipeline_e2e`, `test_parse_grid_xlsx_merged_cells`, `01-timetable-classes.spec.ts` |
| **Initials Detection & Matching** | `ResolveInitialsUseCase`, `InitialsResolver` | `Initials`, `FacultyProfile`, `InitialsResolution` | `GET /api/timetables/{id}` (audit report) | `/timetables` | `test_initials_matching_exact`, `test_initials_matching_fuzzy_levenshtein`, `test_co_teacher_initials_split` |
| **Meeting Circular OCR Scan** | `ProcessCircularUseCase`, `ReviewCircularUseCase` | `Circular`, `CircularStatus`, `FieldExtractor`, `DualPsmOcr` | `POST /api/circulars/upload`, `GET /api/circulars/review-queue`, `POST /api/circulars/{id}/confirm` | `/circulars` | `test_circular_pipeline_e2e`, `test_length_weighted_confidence`, `test_meeting_time_grammar_extraction`, `02-circular-meeting.spec.ts` |
| **Faculty Calendar & Clash Detection** | `CreateEventUseCase`, `GetFacultyCalendarUseCase`, `SweepLineClashDetector` | `Event`, `EventAttendee`, `EventKind`, `Clash` | `GET /api/calendar/events`, `POST /api/calendar/events`, `GET /api/calendar/free-slots`, `GET /api/calendar/ics/{token}.ics` | `/calendar`, `/today` | `test_sweep_line_clash_detection`, `test_free_slots_complement`, `test_ics_export_valid_rfc5545`, `01-timetable-classes.spec.ts` |
| **Meeting & Class Reminders** | `ScheduleRemindersUseCase`, `DispatchDueNotificationsUseCase` | `ScheduledNotification`, `NotificationStatus`, `ReminderRule` | `GET /api/reminders/upcoming`, `POST /api/reminders/rules`, `POST /api/settings/push-subscription` | `/settings`, `/today` | `test_reminder_dispatch_atomic_skip_locked`, `test_quiet_hours_shift_algebra`, `test_full_jitter_exponential_backoff`, `03-meeting-reminder-sent.spec.ts` |
| **To-Do List & Documentation Tasks** | `CreateTaskUseCase`, `AssignTaskUseCase`, `CompleteTaskUseCase` | `Task`, `TaskStatus`, `TaskPriorityCalculator` | `GET /api/tasks`, `POST /api/tasks`, `POST /api/tasks/assign`, `POST /api/tasks/{id}/complete` | `/tasks`, `/today` | `test_task_pipeline_e2e`, `test_task_priority_score_ordering`, `test_task_deadline_event_sync`, `04-task-completion-alerts.spec.ts` |
| **Documentation Work Escalation Alerts** | `ScheduleTaskAlertsUseCase`, `ScheduleHodEscalationAlertsUseCase` | `Task`, `ScheduledNotification`, `AuditLog` | `GET /api/tasks/cohorts/{parent_id}`, `GET /api/admin/metrics` | `/tasks` | `test_task_alert_schedule_d72_d24_d2`, `test_hod_overdue_escalation_summary`, `04-task-completion-alerts.spec.ts` |

---

### 4.3 Standard OOAD Diagram Pack

All eleven presentation diagrams below have been generated from real code and validated with `@mermaid-js/mermaid-cli`. High-resolution PNG and vector SVG versions are located in [`docs/diagrams/`](docs/diagrams/).

#### 4.3.1 Use Case Diagram
*Source: [`docs/diagrams/01-use-case.svg`](docs/diagrams/01-use-case.svg) | [`PNG`](docs/diagrams/01-use-case.png)*

```mermaid
flowchart LR
    Admin([Admin User])
    HOD([HOD User])
    Faculty([Faculty User])
    Scheduler([System Scheduler / Beat])

    subgraph FacultyDesk["FacultyDesk System Boundary"]
        UC_Auth["Authenticate & Rotate Refresh Tokens"]
        UC_Dept["Manage Departments & Terms"]
        UC_Roster["Manage Faculty Roster & Bulk Import"]
        UC_TT_Upload["Upload Timetable (XLSX, CSV, PDF)"]
        UC_TT_Review["Review Grid Parse & Resolve Initials"]
        UC_TT_Confirm["Confirm Timetable & Materialise Classes"]
        UC_Circ_Upload["Upload Meeting Circular (Photo, Scan, PDF)"]
        UC_Circ_Review["Review OCR Extractions & Low-Confidence Queue"]
        UC_Circ_Confirm["Confirm Meeting & Invite Attendees"]
        UC_Task_Assign["Assign Department Tasks & Templates"]
        UC_Task_Complete["Complete Documentation Tasks & Upload Marks"]
        UC_Cal_View["View Aggregated Personal Calendar & Free Slots"]
        UC_Cal_Clash["Detect Clashes & Manual Override"]
        UC_Cal_ICS["Subscribe to Token-Gated ICS Calendar Feed"]
        UC_Settings["Configure Lead Times, Quiet Hours & WebPush"]
        UC_Job_Dispatch["Atomic SKIP LOCKED Reminder Dispatch"]
        UC_Job_Escalate["Generate Daily Escalation Summary"]
        UC_Job_Backup["Automated Nightly Database Backup to MinIO"]
    end

    Admin --> UC_Auth
    Admin --> UC_Dept
    Admin --> UC_Roster
    Admin --> UC_TT_Upload
    Admin --> UC_Job_Backup

    HOD --> UC_Auth
    HOD --> UC_Roster
    HOD --> UC_TT_Upload
    HOD --> UC_TT_Review
    HOD --> UC_TT_Confirm
    HOD --> UC_Circ_Review
    HOD --> UC_Circ_Confirm
    HOD --> UC_Task_Assign
    HOD --> UC_Cal_View

    Faculty --> UC_Auth
    Faculty --> UC_Circ_Upload
    Faculty --> UC_Cal_View
    Faculty --> UC_Cal_Clash
    Faculty --> UC_Cal_ICS
    Faculty --> UC_Task_Complete
    Faculty --> UC_Settings

    Scheduler --> UC_Job_Dispatch
    Scheduler --> UC_Job_Escalate
    Scheduler --> UC_Job_Backup
```

#### 4.3.2 Domain Class Diagram
*Source: [`docs/diagrams/02-class-domain.svg`](docs/diagrams/02-class-domain.svg) | [`PNG`](docs/diagrams/02-class-domain.png)*

```mermaid
classDiagram
    class Department {
        +UUID id
        +str code
        +str name
        +datetime created_at_utc
    }

    class User {
        +UUID id
        +str email
        +str password_hash
        +Role role
        +bool is_active
        +datetime created_at_utc
    }

    class FacultyProfile {
        +UUID id
        +UUID user_id
        +UUID department_id
        +str full_name
        +Initials initials
        +tuple~str~ aliases
        +str email
        +str phone
        +str feed_token
    }

    class AcademicTerm {
        +UUID id
        +str name
        +date start_date
        +date end_date
        +str timezone
    }

    class Holiday {
        +UUID id
        +UUID academic_term_id
        +date date
        +str label
    }

    class Event {
        +UUID id
        +EventKind kind
        +str title
        +datetime start_utc
        +datetime end_utc
        +str location
        +EventSource source
        +UUID source_id
        +reschedule(new_start, new_end)
        +cancel(reason)
        +add_attendee(faculty_id, response)
    }

    class EventAttendee {
        +UUID id
        +UUID event_id
        +UUID faculty_id
        +AttendeeResponse response
    }

    class Circular {
        +UUID id
        +str file_key
        +str ocr_text
        +dict extracted_fields
        +float confidence
        +CircularStatus status
        +start_processing()
        +mark_needs_review(fields, conf)
        +confirm(fields)
        +reject(reason)
        +fail(reason)
    }

    class ScheduledNotification {
        +UUID id
        +UUID target_id
        +str target_kind
        +UUID user_id
        +NotificationChannel channel
        +datetime fire_at_utc
        +str idempotency_key
        +int attempts
        +int max_attempts
        +NotificationStatus status
        +mark_sending()
        +mark_sent()
        +mark_failed(error)
        +retry()
        +cancel()
    }

    class Task {
        +UUID id
        +str title
        +str description
        +datetime deadline_utc
        +int importance
        +TaskStatus status
        +UUID assignee_id
        +UUID assigner_id
        +UUID parent_assignment_id
        +update_deadline(new_deadline)
        +change_status(new_status)
    }

    class SweepLineClashDetector {
        +detect_clashes(target_event, existing_events) list~Clash~
    }

    class InitialsResolver {
        +resolve(token, profiles) ResolutionResult
    }

    class ReminderLeadTimeCalculator {
        +compute_firing_times(event_start, offsets, quiet_hours) list~datetime~
    }

    class TaskPriorityCalculator {
        +compute_priority(deadline, importance, status, now) float
    }

    Department "1" --> "*" FacultyProfile
    User "1" <--> "1" FacultyProfile
    AcademicTerm "1" --> "*" Holiday
    Event "1" *-- "*" EventAttendee
    FacultyProfile "1" --> "*" EventAttendee
    User "1" --> "*" Task : assigned
    User "1" --> "*" ScheduledNotification : receives
    Event "1" ..> SweepLineClashDetector : validates with
    Circular "1" ..> InitialsResolver : resolves with
    Event "1" ..> ReminderLeadTimeCalculator : schedules with
    Task "1" ..> TaskPriorityCalculator : ranked by
```

#### 4.3.3 Sequence Diagram: Timetable Upload and Class Materialisation
*Source: [`docs/diagrams/03-seq-timetable.svg`](docs/diagrams/03-seq-timetable.svg) | [`PNG`](docs/diagrams/03-seq-timetable.png)*

```mermaid
sequenceDiagram
    autonumber
    actor HOD as HOD / Admin
    participant API as FastAPI Router
    participant MinIO as MinIO S3
    participant DB as PostgreSQL
    participant Worker as Celery Worker
    participant EventUC as MaterialiseTimetableEvents
    participant Sched as ReminderScheduler

    HOD->>API: POST /api/timetables/upload (File, dept_id, term_id)
    API->>MinIO: upload_file(key, file_bytes)
    API->>DB: Save TimetableUpload (Status: UPLOADED)
    API->>Worker: Enqueue process_timetable_upload(upload_id)
    API-->>HOD: 202 Accepted {upload_id, status: "UPLOADED"}

    Worker->>MinIO: download_file(key)
    Worker->>Worker: Sniff MIME & Parse Grid (Merged-cell expansion)
    Worker->>DB: Fetch Department Faculty Profiles
    Worker->>Worker: Resolve Initials (Exact -> Alias -> Levenshtein)
    Worker->>DB: Update TimetableUpload (Status: PREVIEW_READY, report)

    HOD->>API: GET /api/timetables/{upload_id}
    API->>DB: Read TimetableUpload
    API-->>HOD: 200 OK {preview_slots, unresolved_tokens}

    HOD->>API: POST /api/timetables/{upload_id}/confirm
    API->>DB: Save Courses, Sections, Rooms, TimetableSlots
    API->>DB: Update TimetableUpload (Status: CONFIRMED)
    API->>Worker: Enqueue materialise_all_timetable_events(term_id)
    API-->>HOD: 200 OK {upload_id, status: "CONFIRMED"}

    Worker->>DB: Query Confirmed Slots, Term Boundaries, Holidays
    Worker->>EventUC: Expand Weekly Recurrence across Term
    loop For each non-holiday occurrence
        EventUC->>DB: INSERT INTO events (kind=CLASS, start_utc, end_utc)
        EventUC->>DB: INSERT INTO event_attendees (faculty_id)
        EventUC->>Sched: Schedule Class Reminders (15 min lead time)
        Sched->>DB: INSERT INTO scheduled_notifications (PENDING, idempotency_key)
    end
```

#### 4.3.4 Sequence Diagram: Circular OCR Scan & Review Queue
*Source: [`docs/diagrams/04-seq-circular.svg`](docs/diagrams/04-seq-circular.svg) | [`PNG`](docs/diagrams/04-seq-circular.png)*

```mermaid
sequenceDiagram
    autonumber
    actor User as Faculty / HOD
    participant API as FastAPI Router
    participant MinIO as MinIO S3
    participant DB as PostgreSQL
    participant Worker as Celery Worker
    participant Pre as Image Preprocessor
    participant OCR as Tesseract Dual-PSM
    participant Ext as Field Extractor
    actor HOD as HOD User
    participant EventUC as Calendar Engine

    User->>API: POST /api/circulars/upload (file, dept_id)
    API->>MinIO: upload_file(random_key, bytes)
    API->>DB: INSERT INTO circulars (status=UPLOADED)
    API->>Worker: Enqueue process_circular_upload(circular_id)
    API-->>User: 202 Accepted {circular_id, status: "UPLOADED"}

    Worker->>DB: UPDATE circulars SET status=PROCESSING
    Worker->>MinIO: download_file(file_key)
    alt PDF has text layer
        Worker->>Worker: Extract text stream
    else Scanned image or PDF
        Worker->>Pre: Rasterise & preprocess (threshold, deskew)
        Pre-->>Worker: Clean image & rotation angle
        Worker->>OCR: extract_text (PSM 6 block -> PSM 4 column)
        OCR-->>Worker: Extracted text & word-confidence scores
    end

    Worker->>Ext: extract_fields(text, confidence, faculty_profiles)
    Ext-->>Worker: date, time, venue, attendees, review_reasons
    Worker->>DB: UPDATE circulars SET status=NEEDS_REVIEW, extracted_fields

    HOD->>API: GET /api/circulars/review-queue
    API->>DB: SELECT FROM circulars WHERE status=NEEDS_REVIEW
    API-->>HOD: 200 OK (Queue items with extractions & confidence)

    HOD->>API: POST /api/circulars/{id}/confirm (Verified fields)
    API->>EventUC: CreateEventUseCase(MEETING, start, end, venue, attendees)
    EventUC->>DB: INSERT INTO events & event_attendees
    EventUC->>DB: INSERT INTO scheduled_notifications (offsets: 24h, 1h, 10m)
    API->>DB: UPDATE circulars SET status=CONFIRMED
    API-->>HOD: 200 OK (Event details & confirmed meeting)
```

#### 4.3.5 Sequence Diagram: Periodic Reminder Dispatch (Atomic SKIP LOCKED)
*Source: [`docs/diagrams/05-seq-reminder.svg`](docs/diagrams/05-seq-reminder.svg) | [`PNG`](docs/diagrams/05-seq-reminder.png)*

```mermaid
sequenceDiagram
    autonumber
    actor Beat as Celery Beat (Every 30s)
    participant Worker as Celery Worker
    participant DB as PostgreSQL
    participant Disp as ReminderDispatcher
    participant Notifier as CompositeNotifier
    participant Ext as Email / WebPush Service

    Beat->>Worker: Enqueue dispatch_due_notifications
    Worker->>Disp: dispatch_due(batch_size=100)
    Disp->>DB: BEGIN Transaction
    Disp->>DB: SELECT FOR UPDATE SKIP LOCKED (status=PENDING, fire_at_utc <= now, LIMIT 100)
    Disp->>DB: UPDATE scheduled_notifications SET status='SENDING', attempts=attempts+1
    Disp->>DB: COMMIT Transaction

    loop For each claimed notification
        Disp->>DB: Fetch user, profile, event details
        Disp->>Notifier: send(notification, payload, user, profile)
        alt Delivery Successful
            Notifier->>Ext: Deliver Email (SMTP) / WebPush (VAPID)
            Ext-->>Notifier: 200 OK / 202 Accepted
            Notifier-->>Disp: Success
            Disp->>DB: UPDATE scheduled_notifications SET status='SENT', delivered_at_utc=now()
        else Delivery Fails (Transient network / 5xx)
            Notifier-->>Disp: Raise DeliveryError
            Disp->>Disp: Compute full-jitter exponential backoff delay(n)
            alt attempts < 5
                Disp->>DB: UPDATE scheduled_notifications SET status='PENDING', fire_at_utc=now()+delay, last_error=err
            else attempts >= 5
                Disp->>DB: UPDATE scheduled_notifications SET status='FAILED', last_error=err
            end
        end
    end
```

#### 4.3.6 State Diagram: Circular Lifecycle
*Source: [`docs/diagrams/06-state-circular.svg`](docs/diagrams/06-state-circular.svg) | [`PNG`](docs/diagrams/06-state-circular.png)*

```mermaid
stateDiagram-v2
    [*] --> UPLOADED : File uploaded to MinIO
    UPLOADED --> PROCESSING : start_processing()
    PROCESSING --> NEEDS_REVIEW : mark_needs_review()<br/>(low conf / missing field / dup)
    PROCESSING --> CONFIRMED : auto_confirm()<br/>(high conf & valid fields)
    PROCESSING --> FAILED : fail(reason)<br/>(OCR error / corrupted file)
    NEEDS_REVIEW --> CONFIRMED : confirm(verified_fields)<br/>(HOD approval)
    NEEDS_REVIEW --> REJECTED : reject(reason)<br/>(HOD rejection)
    FAILED --> PROCESSING : retry
    CONFIRMED --> [*]
    REJECTED --> [*]
```

#### 4.3.7 State Diagram: ScheduledNotification Lifecycle
*Source: [`docs/diagrams/07-state-notification.svg`](docs/diagrams/07-state-notification.svg) | [`PNG`](docs/diagrams/07-state-notification.png)*

```mermaid
stateDiagram-v2
    [*] --> PENDING : Event scheduled with lead time
    PENDING --> SENDING : mark_sending()<br/>(claimed by dispatcher via SKIP LOCKED)
    SENDING --> SENT : mark_sent()<br/>(delivered via Email / WebPush)
    SENDING --> FAILED : mark_failed()<br/>(attempts >= max_attempts)
    SENDING --> PENDING : retry()<br/>(attempts < max with full-jitter backoff)
    PENDING --> CANCELLED : cancel()<br/>(event deleted or task completed)
    SENT --> [*]
    FAILED --> PENDING : admin_retry()<br/>(POST /api/admin/notifications/{id}/retry)
    CANCELLED --> [*]
```

#### 4.3.8 Activity Diagram: Timetable Ingestion & Initials Resolution
*Source: [`docs/diagrams/08-activity-timetable.svg`](docs/diagrams/08-activity-timetable.svg) | [`PNG`](docs/diagrams/08-activity-timetable.png)*

```mermaid
flowchart TD
    Start([Upload File Received]) --> Sniff[Sniff MIME Type from Magic Bytes]
    Sniff --> CheckType{File Type?}
    CheckType -->|XLSX| ParseXlsx[openpyxl: Detect Grid & Merged Period Cells]
    CheckType -->|CSV| ParseCsv[CSV Reader: Parse Tokens & Delimiters]
    CheckType -->|PDF| CheckPdf{Text Layer Present?}
    CheckType -->|Unsupported| RejectFormat[Reject Unsupported Format]

    CheckPdf -->|No: Scanned| RejectScanned[Reject with Resolution Guidance]
    CheckPdf -->|Yes: Native Text| ParsePdf[pdfplumber: Extract Table Cells]

    ParseXlsx --> ExpandPeriods["Merged Period Expansion: Period k..m -> s(k)..e(m)"]
    ParseCsv --> Tokenize
    ParsePdf --> Tokenize
    ExpandPeriods --> Tokenize["Tokenize Cells: Course, Section, Room, Initials"]

    Tokenize --> CheckCoTeachers{"Co-Teacher Delimiters: /, &, , ?"}
    CheckCoTeachers -->|Yes| SplitCo[Split into Individual Tokens]
    CheckCoTeachers -->|No| InitialsEngine[Initials Resolution Engine]
    SplitCo --> InitialsEngine

    InitialsEngine --> MatchTier{Resolution Tier}
    MatchTier -->|Tier 1: Exact Initials| Resolved[Resolved: FacultyProfile ID]
    MatchTier -->|Tier 2: Exact Alias| Resolved
    MatchTier -->|Tier 3: Fuzzy sim >= 0.85 & margin >= 0.10| Resolved
    MatchTier -->|Below Threshold / Ambiguous| Unresolved[Flag Unresolved / Ambiguous Token]

    Resolved --> BuildPreview[Compile Preview Slots & Audit Report]
    Unresolved --> BuildPreview
    BuildPreview --> StateReady[TimetableUpload State -> PREVIEW_READY]
    StateReady --> AwaitConfirm([Awaiting HOD Confirmation])

    AwaitConfirm --> Confirm[HOD Confirms Preview Slots]
    Confirm --> Materialise[Materialise Events & Schedule Notifications]
    Materialise --> Done([Faculty Calendars Populated])
```

#### 4.3.9 Component Diagram: Clean Architecture & System Layers
*Source: [`docs/diagrams/09-component.svg`](docs/diagrams/09-component.svg) | [`PNG`](docs/diagrams/09-component.png)*

```mermaid
flowchart TD
    subgraph Presentation["Presentation Tier (Next.js 15)"]
        UI["React 19 App Router & shadcn/ui"]
        State["TanStack Query & AuthContext"]
        Form["react-hook-form & Zod Schemas"]
        CalView["FullCalendar Engine"]
    end

    subgraph APILayer["API Gateway & Routers (FastAPI)"]
        AuthRouter["Auth Router (Argon2id, Refresh Cookie)"]
        CalRouter["Calendar Router (Clash, Free Slots, ICS)"]
        TaskRouter["Tasks Router (Assignment, Alerts)"]
        CircRouter["Circulars Router (OCR, Review Queue)"]
        DirRouter["Directory Router (Faculty, Terms, Holidays)"]
        AdminRouter["Admin Metrics & Hardening Router"]
    end

    subgraph Application["Application Layer (Use Cases)"]
        AuthUC["Auth & Session Use Cases"]
        CalUC["Event Creation & Recurrence Use Cases"]
        CircUC["Process Circular & Confirmation Use Cases"]
        TaskUC["Assign Task & Escalation Use Cases"]
        RemindUC["Reminder Dispatch & Retry Use Cases"]
        Policy["AuthorisationPolicy (ADMIN, HOD, FACULTY)"]
    end

    subgraph Domain["Domain Layer (Clean Core)"]
        Entities["Entities: Event, Task, Circular, Notification, FacultyProfile"]
        Services["Domain Services: SweepLineClash, InitialsResolver, PriorityScore"]
        Repos["Repository & UnitOfWork Interfaces"]
        Events["Domain Events: TimetableConfirmed, CircularProcessed"]
    end

    subgraph Infrastructure["Infrastructure & Persistence Tier"]
        SQLA["SQLAlchemy 2 Async & asyncpg"]
        RedisAdapt["Redis Client (RateLimiting, TokenBlacklist)"]
        MinioAdapt["MinIO S3 Client (Storage, UploadGuard)"]
        OCRAdapt["Tesseract OCR & OpenCV Preprocessing"]
        NotifAdapt["CompositeNotifier (aiosmtplib, pywebpush)"]
    end

    subgraph Workers["Background Processing (Celery)"]
        CeleryWorker["Celery Worker (OCR, Ingestion, Batch Tasks)"]
        CeleryBeat["Celery Beat (Dispatcher 30s, Nightly Backup 02:00)"]
    end

    UI --> State
    State --> Form
    State --> CalView
    State --> APILayer
    APILayer --> Application
    Application --> Policy
    Application --> Domain
    Application --> Repos
    SQLA -.->|Implements| Repos
    Workers --> Application
    Workers --> OCRAdapt
    Workers --> NotifAdapt
    SQLA --> Domain
    RedisAdapt --> Application
    MinioAdapt --> Application
```

#### 4.3.10 Deployment Diagram: Production & College-LAN Topology
*Source: [`docs/diagrams/10-deployment.svg`](docs/diagrams/10-deployment.svg) | [`PNG`](docs/diagrams/10-deployment.png)*

```mermaid
flowchart TD
    subgraph Client["Client Workstations & Mobile Devices"]
        Web["Modern Desktop Browser"]
        Mobile["Mobile PWA (WebPush Enabled)"]
        ExternalCal["External Calendar Client (Apple / Google)"]
    end

    subgraph Edge["Perimeter & Edge Gateway"]
        Caddy["Caddy Reverse Proxy<br/>Auto HTTPS (ACME) or College-LAN Internal CA<br/>Security Headers: HSTS, CSP, X-Frame-Options"]
    end

    subgraph AppContainers["Application Service Containers (Non-Root UID 10001)"]
        Frontend["frontend:3000 (Next.js Standalone)<br/>Internal /api/* Reverse Proxy"]
        Backend["backend:8000 (FastAPI / Uvicorn)<br/>Clean Architecture Application"]
        Worker["worker (Celery 5)<br/>OCR, Ingestion, Notification Delivery"]
        Beat["beat (Celery Beat)<br/>Scheduled Ticks (30s Dispatch, 02:00 Backup)"]
    end

    subgraph Persistence["Storage & Broker Services"]
        Postgres[("PostgreSQL 16 Database<br/>Port: 5432 / Internal asyncpg")]
        Redis[("Redis 7 Cache & Broker<br/>Port: 6379 / Celery & RateLimiter")]
        MinIO[("MinIO S3 Object Storage<br/>Buckets: circulars, timetables, backups")]
        Mailpit["Mailpit Dev SMTP / WebUI<br/>Ports: 1025 (SMTP), 8025 (Web)"]
    end

    Web -->|HTTPS 443| Caddy
    Mobile -->|HTTPS 443| Caddy
    ExternalCal -->|HTTPS 443 /api/calendar/ics/*| Caddy

    Caddy -->|/api/*, /docs, /openapi.json| Backend
    Caddy -->|UI Routes| Frontend
    Frontend -.->|Internal API Proxy| Backend

    Backend --> Postgres
    Backend --> Redis
    Backend --> MinIO
    Worker --> Postgres
    Worker --> Redis
    Worker --> MinIO
    Worker --> Mailpit
    Beat --> Redis
```

#### 4.3.11 Entity-Relationship (ER) Diagram
*Source: [`docs/diagrams/11-er.svg`](docs/diagrams/11-er.svg) | [`PNG`](docs/diagrams/11-er.png)*

```mermaid
erDiagram
    departments ||--o{ faculty_profiles : employs
    departments ||--o{ courses : offers
    departments ||--o{ timetable_uploads : owns
    departments ||--o{ circulars : owns
    users ||--|| faculty_profiles : identifies
    users ||--o{ refresh_tokens : has
    users ||--o{ tasks : assigned
    users ||--o{ scheduled_notifications : receives
    users ||--o{ audit_logs : triggers
    academic_terms ||--o{ holidays : includes
    academic_terms ||--o{ timetable_uploads : schedules
    courses ||--o{ sections : has
    timetable_uploads ||--o{ timetable_slots : contains
    events ||--o{ event_attendees : invites
    faculty_profiles ||--o{ event_attendees : attends
    tasks ||--o{ tasks : cohort_parent

    departments {
        uuid id PK
        varchar code UK
        varchar name
        timestamptz created_at_utc
    }

    users {
        uuid id PK
        varchar email UK
        text password_hash
        varchar role
        bool is_active
        timestamptz created_at_utc
    }

    refresh_tokens {
        uuid id PK
        uuid user_id FK
        varchar token_hash UK
        uuid family_id
        bool is_revoked
        timestamptz expires_at_utc
    }

    faculty_profiles {
        uuid id PK
        uuid user_id FK
        uuid department_id FK
        varchar full_name
        varchar initials
        jsonb aliases
        varchar email
        varchar phone
        varchar feed_token UK
    }

    academic_terms {
        uuid id PK
        varchar name
        date start_date
        date end_date
        varchar timezone
    }

    holidays {
        uuid id PK
        uuid academic_term_id FK
        date date
        varchar label
    }

    events {
        uuid id PK
        varchar kind
        varchar title
        timestamptz start_utc
        timestamptz end_utc
        varchar location
        varchar source
        uuid source_id
    }

    event_attendees {
        uuid id PK
        uuid event_id FK
        uuid faculty_id FK
        varchar response
    }

    circulars {
        uuid id PK
        uuid department_id FK
        varchar file_key
        text ocr_text
        jsonb extracted_fields
        float confidence
        varchar status
    }

    scheduled_notifications {
        uuid id PK
        uuid target_id
        varchar target_kind
        uuid user_id FK
        varchar channel
        timestamptz fire_at_utc
        varchar idempotency_key UK
        int attempts
        varchar status
        timestamptz delivered_at_utc
    }

    tasks {
        uuid id PK
        varchar title
        text description
        timestamptz deadline_utc
        int importance
        varchar status
        uuid assignee_id FK
        uuid assigner_id FK
        uuid parent_assignment_id FK
    }

    audit_logs {
        uuid id PK
        uuid actor_id FK
        varchar action
        varchar resource_type
        varchar resource_id
        jsonb details
        timestamptz created_at_utc
    }
```


## 5. How to run, test and deploy

### Prerequisites
- Docker & Docker Compose
- `uv` (Python 3.12 package manager)
- `pnpm` (Node package manager)
- Node.js 20+

### Development commands
```bash
# Boot the entire stack in background
make up

# Check status of running containers
docker compose ps

# Run database migrations
make migrate

# Seed synthetic departments, users, term, and holidays
make seed

# Run quality checks (lint, typecheck, targeted tests)
make lint
make typecheck
make test

# Run Playwright E2E smoke tests
cd frontend && pnpm test:e2e

# Prepare fresh environment for live demonstration
make demo

# Tear down environment
make down
```

### Production deployment

FacultyDesk ships with a production-hardened compose definition (`docker-compose.prod.yml`) utilizing:
- Multi-stage non-root containers for both backend (`appuser:10001`) and frontend (`nextjs:10001`).
- Standalone Next.js runner with automatic `/api/*` internal reverse proxy to backend.
- Caddy reverse proxy serving automatic HTTPS with HTTP/2 and HTTP/3 support.
- MinIO S3 object storage with automated bucket provisioning (`create-buckets`).
- Resource limits (`cpus: "2"`, `memory: 2G`) and strict restart policies across all services.

To deploy in production with a public domain:
```bash
# 1. Configure environment variables in .env
DOMAIN=facultydesk.example.edu
CADDY_TLS_DIRECTIVE=acme

# 2. Boot production stack
docker compose -f docker-compose.prod.yml up -d

# 3. Apply database migrations
docker compose -f docker-compose.prod.yml exec backend uv run alembic upgrade head
```

### College-LAN mode (Department Server deployment)

For college intranets or department server labs operating without a public internet domain or public DNS, FacultyDesk supports **College-LAN mode**. Caddy acts as an internal Certificate Authority (CA) issuing locally trusted TLS certificates on LAN IP addresses or internal hostname aliases (e.g. `facultydesk.local` or `192.168.1.100`).

Configuration:
```env
# In .env:
DOMAIN=facultydesk.cse.college.local
CADDY_TLS_DIRECTIVE=internal
```

In `Caddyfile`:
```caddy
{$DOMAIN:localhost} {
    tls {$CADDY_TLS_DIRECTIVE:internal}

    # API and docs routed to backend
    handle /api/* {
        reverse_proxy backend:8000
    }
    handle /docs* {
        reverse_proxy backend:8000
    }
    handle /openapi.json {
        reverse_proxy backend:8000
    }

    # All UI routes handled by Next.js standalone runner
    handle {
        reverse_proxy frontend:3000
    }
}
```

To trust Caddy's internal root CA on faculty workstations connected to the department Wi-Fi/LAN:
1. Fetch root CA certificate: `curl -k https://<server-ip>/caddy-pki-root.crt` or copy `/data/caddy/pki/authorities/local/root.crt` from the Caddy container.
2. Install into OS trust store (macOS Keychain, Windows Trusted Root Authorities, or Linux `/usr/local/share/ca-certificates/`).
3. Department faculty can navigate securely to `https://facultydesk.cse.college.local` with zero browser certificate warnings.

### Service URLs (Dev Mode)
- Frontend: `http://localhost:3000`
- API & Docs: `http://localhost:8000/docs`
- Health Probe: `http://localhost:8000/healthz`
- Readiness Probe: `http://localhost:8000/readyz`
- MinIO Console: `http://localhost:9001`
- Mailpit Web UI: `http://localhost:8025`
