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
- Docker Compose development and production environments with health checks on all services.
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

## 4. OOAD diagrams

### 4.1 Component Diagram

```mermaid
flowchart TD
    subgraph ClientLayer["Presentation Layer"]
        UI["Next.js App Router (React 19)"]
        Badge["Readiness Probe Component"]
    end

    subgraph APILayer["API & Application Gateway"]
        FastAPI["FastAPI App (uvicorn)"]
        ReqMiddleware["RequestIdMiddleware"]
        HealthRouter["Healthz & Readyz Endpoints"]
    end

    subgraph CoreDomain["Core & Domain Services"]
        ClockSvc["Clock Protocol (SystemClock / FrozenClock)"]
        SettingsSvc["Pydantic Settings"]
        LogSvc["Structlog JSON Logging"]
        SecSvc["Argon2id & JWT Security"]
    end

    subgraph InfraStorage["Infrastructure & Persistence"]
        DB["SQLAlchemy 2 Async Engine / asyncpg"]
        RedisClient["aioredis Client"]
        MinioClient["MinIO S3 Client"]
    end

    subgraph BackgroundLayer["Background Jobs"]
        CeleryWorker["Celery Worker"]
        CeleryBeat["Celery Beat Scheduler"]
    end

    UI --> Badge
    Badge --> HealthRouter
    FastAPI --> ReqMiddleware
    FastAPI --> HealthRouter
    HealthRouter --> DB
    HealthRouter --> RedisClient
    HealthRouter --> MinioClient
    FastAPI --> CoreDomain
    CeleryWorker --> RedisClient
    CeleryBeat --> RedisClient
```

### 4.2 Domain Class Diagram

```mermaid
classDiagram
    class Department {
        +UUID id
        +str code
        +str name
    }

    class User {
        +UUID id
        +str email
        +str password_hash
        +Role role
        +bool is_active
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
        +update_deadline(new_deadline)
        +change_status(new_status)
    }

    Department "1" --> "*" FacultyProfile
    User "1" <--> "1" FacultyProfile
    AcademicTerm "1" --> "*" Holiday
    Event "1" *-- "*" EventAttendee
    FacultyProfile "1" --> "*" EventAttendee
```

### 4.3 Circular State Machine

```mermaid
stateDiagram-v2
    [*] --> UPLOADED
    UPLOADED --> PROCESSING : start_processing()
    PROCESSING --> NEEDS_REVIEW : mark_needs_review()
    PROCESSING --> CONFIRMED : confirm()
    PROCESSING --> FAILED : fail()
    NEEDS_REVIEW --> CONFIRMED : confirm()
    NEEDS_REVIEW --> REJECTED : reject()
    FAILED --> PROCESSING : retry
    CONFIRMED --> [*]
    REJECTED --> [*]
```

### 4.4 ScheduledNotification State Machine

```mermaid
stateDiagram-v2
    [*] --> PENDING
    PENDING --> SENDING : mark_sending()
    SENDING --> SENT : mark_sent()
    SENDING --> FAILED : mark_failed()
    FAILED --> PENDING : retry (attempts < max)
    PENDING --> CANCELLED : cancel()
    SENT --> [*]
    CANCELLED --> [*]
```

### 4.5 Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    departments ||--o{ faculty_profiles : employs
    departments ||--o{ courses : offers
    users ||--|| faculty_profiles : identifies
    users ||--o{ tasks : assigned
    users ||--o{ scheduled_notifications : receives
    academic_terms ||--o{ holidays : includes
    courses ||--o{ sections : has
    events ||--o{ event_attendees : invites
    faculty_profiles ||--o{ event_attendees : attends
    timetable_uploads ||--o{ timetable_slots : contains

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

    faculty_profiles {
        uuid id PK
        uuid user_id FK
        uuid department_id FK
        varchar full_name
        varchar initials
        jsonb aliases
        varchar email
    }

    events {
        uuid id PK
        varchar kind
        varchar title
        timestamptz start_utc
        timestamptz end_utc
        varchar location
        varchar source
    }

    scheduled_notifications {
        uuid id PK
        uuid target_id
        uuid user_id FK
        varchar channel
        timestamptz fire_at_utc
        varchar idempotency_key UK
        int attempts
        varchar status
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
    }
```

### 4.6 Authentication & Token Rotation Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Client as Browser / Client
    participant API as FastAPI Router
    participant Limit as Redis RateLimiter
    participant UC as Login / Refresh UseCase
    participant DB as PostgreSQL
    participant Cookie as httpOnly Cookie

    Note over Client, DB: Step 1: Initial Login
    Client->>API: POST /api/auth/login {email, password}
    API->>Limit: check_and_consume(ip, account)
    Limit-->>API: Allow (within 5/min limit)
    API->>UC: execute(email, password)
    UC->>DB: Verify user & argon2id hash
    UC->>DB: Save RefreshToken (Family F1, Token T0)
    UC-->>API: Access JWT + Raw RefreshToken T0
    API->>Cookie: Set-Cookie refresh_token=T0 (httpOnly, Lax)
    API-->>Client: 200 OK {access_token, user, profile}

    Note over Client, DB: Step 2: Token Rotation
    Client->>API: POST /api/auth/refresh (Cookie: T0)
    API->>Limit: check_and_consume(ip)
    Limit-->>API: Allow (within 30/min limit)
    API->>UC: execute(T0)
    UC->>DB: Find token by hash(T0)
    alt T0 is active
        UC->>DB: Mark T0 revoked
        UC->>DB: Save RefreshToken (Family F1, Token T1)
        API->>Cookie: Set-Cookie refresh_token=T1
        API-->>Client: 200 OK {access_token}
    else T0 is already revoked (Reuse Attack)
        UC->>DB: Revoke all tokens in Family F1
        API-->>Client: 401 Unauthorized (Family Revoked)
    end
```

### 4.7 Timetable Ingestion Activity Diagram

```mermaid
flowchart TD
    Start([Upload File Received]) --> Sniff[Sniff MIME Type from Bytes]
    Sniff --> CheckType{MIME Type}
    CheckType -->|XLSX| ParseXlsx[openpyxl: Detect Grid & Merged Cells]
    CheckType -->|CSV| ParseCsv[CSV Reader: Long-format Tokens]
    CheckType -->|PDF| CheckPdf{Text Layer Present?}
    CheckType -->|Other| RejectFormat[Reject Unsupported Format]

    CheckPdf -->|No: Scanned| RejectScanned[Reject with Guided Message]
    CheckPdf -->|Yes: Text| ParsePdf[pdfplumber: Extract Tables & Cells]

    ParseXlsx --> ExpandPeriods["Merged-Cell Period Expansion: k..m to s(k)..e(m)"]
    ParseCsv --> Tokenize
    ParsePdf --> Tokenize
    ExpandPeriods --> Tokenize["Tokenize Cells: Course, Section, Room, Initials"]

    Tokenize --> CoTeachers{"Co-Teacher Delimiters /, &, ,?"}
    CoTeachers -->|Yes| SplitCo[Split into Individual Initials]
    CoTeachers -->|No| InitialsResolution[Initials Resolution Engine]
    SplitCo --> InitialsResolution

    InitialsResolution --> MatchTier{Resolution Tiers}
    MatchTier -->|Exact Initials| Resolved[Resolved: Faculty Profile ID]
    MatchTier -->|Exact Alias| Resolved
    MatchTier -->|Fuzzy: sim >= 0.85 & margin >= 0.10| Resolved
    MatchTier -->|sim < 0.85 or margin < 0.10| Ambiguous[Record Unresolved / Ambiguous Issue]

    Resolved --> BuildPreview[Build Preview Slots & Issues Report]
    Ambiguous --> BuildPreview
    BuildPreview --> StateReady[TimetableUpload State -> PREVIEW_READY]
    StateReady --> End([Awaiting HOD Confirmation])
```

### 4.8 Timetable Upload to Confirmation Sequence

```mermaid
sequenceDiagram
    autonumber
    actor HOD as HOD / Admin
    participant API as FastAPI Router
    participant MinIO as MinIO Storage
    participant DB as PostgreSQL
    participant Worker as Celery Worker
    participant Event as Domain Event Bus

    HOD->>API: POST /api/timetables/upload (File, dept_id, term_id)
    API->>MinIO: upload_file(key, file_bytes)
    API->>DB: Save TimetableUpload (Status: UPLOADED)
    API->>Worker: Enqueue process_timetable_upload(upload_id)
    API-->>HOD: 202 Accepted {upload_id, status: "UPLOADED"}

    Worker->>MinIO: download_file(key)
    Worker->>Worker: Parse Grid & Normalize Header Times
    Worker->>DB: Fetch Department Faculty Profiles
    Worker->>Worker: Resolve Initials (Exact -> Alias -> Levenshtein)
    Worker->>DB: Update TimetableUpload (Status: PREVIEW_READY, parse_report)

    HOD->>API: GET /api/timetables/{upload_id}
    API->>DB: Read TimetableUpload
    API-->>HOD: 200 OK {status: PREVIEW_READY, preview_slots, unresolved_tokens}

    HOD->>API: POST /api/timetables/{upload_id}/confirm
    API->>DB: Get or Create Courses, Sections, Rooms
    API->>DB: Save TimetableSlots
    API->>DB: Update TimetableUpload (Status: CONFIRMED)
    API->>Event: Emit TimetableConfirmed(upload_id, dept_id, term_id, slot_count)
    API-->>HOD: 200 OK {upload_id, slots_created, status: "CONFIRMED"}
```

### 4.9 Calendar Recurrence Materialisation and Sweep-Line Clash Detection

```mermaid
sequenceDiagram
    autonumber
    actor User as Faculty / HOD / Admin
    participant API as FastAPI Router
    participant UC as Calendar UseCases
    participant Clash as SweepLineClashDetector
    participant DB as PostgreSQL
    participant Ext as External Calendar (Apple/Google)

    Note over User, DB: Scenario 1: Meeting Creation with Clash Detection
    User->>API: POST /api/calendar/events {title, start, end, attendees, override: false}
    API->>UC: CreateEventUseCase.execute(...)
    UC->>DB: Fetch existing attendee events in [start, end)
    UC->>Clash: detect_clashes(new_event, existing_events)
    alt Overlap Detected: max(s1, s2) < min(e1, e2)
        Clash-->>UC: Clashes list [attendee_id, title, start, end]
        UC-->>API: raise ClashDetectedError(clashes)
        API-->>User: 409 Conflict {message, clashes}
    else No Overlap or override=true
        UC->>DB: Save Event + EventAttendees
        DB-->>UC: event
        UC-->>API: event
        API-->>User: 201 Created {event_id, title, start_utc, end_utc}
    end

    Note over User, Ext: Scenario 2: Token-Gated RFC 5545 ICS Feed Sync
    Ext->>API: GET /api/calendar/ics/{feed_token}.ics
    API->>UC: GenerateIcsFeedUseCase.execute(feed_token)
    UC->>DB: Look up FacultyProfile by feed_token
    UC->>DB: Query attendee events for faculty in window
    UC->>UC: Generate VCALENDAR with stable UIDs & PRODID
    UC-->>API: VCALENDAR text/calendar payload
    API-->>Ext: 200 OK text/calendar; charset=utf-8
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

# Tear down environment
make down
```

### URLs
- Frontend: `http://localhost:3000`
- API & Docs: `http://localhost:8000/docs`
- Health Probe: `http://localhost:8000/healthz`
- Readiness Probe: `http://localhost:8000/readyz`
- MinIO Console: `http://localhost:9001`
