from datetime import date, datetime
from typing import Self
from uuid import UUID

import structlog
from sqlalchemy import delete as sa_delete
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from app.domain import (
    AcademicTerm,
    AcademicTermRepository,
    AttendeeResponse,
    AuditLog,
    AuditLogRepository,
    Circular,
    CircularRepository,
    CircularStatus,
    Course,
    CourseRepository,
    Department,
    DepartmentRepository,
    Event,
    EventAttendee,
    EventKind,
    EventRepository,
    EventSource,
    FacultyProfile,
    FacultyProfileRepository,
    Holiday,
    Initials,
    NotificationChannel,
    NotificationRepository,
    NotificationStatus,
    PushSubscription,
    PushSubscriptionRepository,
    RefreshToken,
    RefreshTokenRepository,
    ReminderRule,
    ReminderRuleRepository,
    Role,
    Room,
    RoomRepository,
    ScheduledNotification,
    Section,
    SectionRepository,
    Task,
    TaskCategory,
    TaskRecurrence,
    TaskRepository,
    TaskStatus,
    TaskTemplate,
    TaskTemplateRepository,
    TimeSlot,
    TimetableSlot,
    TimetableSlotRepository,
    TimetableUpload,
    TimetableUploadRepository,
    TimetableUploadStatus,
    UnitOfWork,
    User,
    UserRepository,
)
from app.infrastructure.db.models import (
    AcademicTermModel,
    AuditLogModel,
    CircularModel,
    CourseModel,
    DepartmentModel,
    EventAttendeeModel,
    EventModel,
    FacultyProfileModel,
    HolidayModel,
    PushSubscriptionModel,
    RefreshTokenModel,
    ReminderRuleModel,
    RoomModel,
    ScheduledNotificationModel,
    SectionModel,
    TaskModel,
    TaskTemplateModel,
    TimetableSlotModel,
    TimetableUploadModel,
    UserModel,
)

logger = structlog.get_logger(__name__)


def department_to_domain(m: DepartmentModel) -> Department:
    return Department(id=m.id, code=m.code, name=m.name)


def user_to_domain(m: UserModel) -> User:
    return User(
        id=m.id,
        email=m.email,
        password_hash=m.password_hash,
        role=Role(m.role),
        is_active=m.is_active,
        quiet_hours_start=m.quiet_hours_start,
        quiet_hours_end=m.quiet_hours_end,
    )


def faculty_profile_to_domain(m: FacultyProfileModel) -> FacultyProfile:
    return FacultyProfile(
        id=m.id,
        user_id=m.user_id,
        department_id=m.department_id,
        full_name=m.full_name,
        initials=Initials(m.initials),
        aliases=tuple(m.aliases),
        email=m.email,
        phone=m.phone,
        ics_token=m.ics_token,
    )


def academic_term_to_domain(m: AcademicTermModel) -> AcademicTerm:
    return AcademicTerm(
        id=m.id,
        name=m.name,
        start_date=m.start_date,
        end_date=m.end_date,
        timezone=m.timezone,
    )


def holiday_to_domain(m: HolidayModel) -> Holiday:
    return Holiday(
        id=m.id,
        academic_term_id=m.academic_term_id,
        date=m.date,
        label=m.label,
    )


def event_to_domain(m: EventModel) -> Event:
    attendees = [
        EventAttendee(
            id=att.id,
            event_id=att.event_id,
            faculty_id=att.faculty_id,
            response=AttendeeResponse(att.response),
        )
        for att in m.attendees
    ]
    return Event(
        id=m.id,
        kind=EventKind(m.kind),
        title=m.title,
        start_utc=m.start_utc,
        end_utc=m.end_utc,
        location=m.location,
        source=EventSource(m.source),
        source_id=m.source_id,
        recurrence_date=m.recurrence_date,
        attendees=attendees,
    )


def circular_to_domain(m: CircularModel) -> Circular:
    return Circular(
        id=m.id,
        file_key=m.file_key,
        ocr_text=m.ocr_text,
        extracted_fields=dict(m.extracted_fields),
        confidence=m.confidence,
        status=CircularStatus(m.status),
        failure_reason=m.failure_reason,
    )


def notification_to_domain(m: ScheduledNotificationModel) -> ScheduledNotification:
    return ScheduledNotification(
        id=m.id,
        target_id=m.target_id,
        target_kind=m.target_kind,
        user_id=m.user_id,
        channel=NotificationChannel(m.channel),
        fire_at_utc=m.fire_at_utc,
        idempotency_key=m.idempotency_key,
        attempts=m.attempts,
        max_attempts=m.max_attempts,
        last_error=m.last_error,
        delivered_at_utc=m.delivered_at_utc,
        status=NotificationStatus(m.status),
    )


def reminder_rule_to_domain(m: ReminderRuleModel) -> ReminderRule:
    return ReminderRule(
        id=m.id,
        user_id=m.user_id,
        event_kind=EventKind(m.event_kind),
        offsets_minutes=tuple(m.offsets_minutes),
        channels=tuple(NotificationChannel(c) for c in m.channels),
    )


def push_subscription_to_domain(m: PushSubscriptionModel) -> PushSubscription:
    return PushSubscription(
        id=m.id,
        user_id=m.user_id,
        endpoint=m.endpoint,
        p256dh=m.p256dh,
        auth=m.auth,
    )


def task_to_domain(m: TaskModel) -> Task:
    return Task(
        id=m.id,
        title=m.title,
        description=m.description,
        deadline_utc=m.deadline_utc,
        importance=m.importance,
        category=TaskCategory(m.category),
        status=TaskStatus(m.status),
        assignee_id=m.assignee_id,
        assigner_id=m.assigner_id,
        parent_assignment_id=m.parent_assignment_id,
        recurrence=TaskRecurrence(m.recurrence) if m.recurrence else None,
        created_at_utc=m.created_at_utc,
    )


def task_template_to_domain(m: TaskTemplateModel) -> TaskTemplate:
    return TaskTemplate(
        id=m.id,
        title=m.title,
        description=m.description,
        default_importance=m.default_importance,
        default_lead_days=m.default_lead_days,
        category=TaskCategory(m.category),
        department_id=m.department_id,
    )


def audit_log_to_domain(m: AuditLogModel) -> AuditLog:
    return AuditLog(
        id=m.id,
        user_id=m.user_id,
        action=m.action,
        resource_type=m.resource_type,
        resource_id=m.resource_id,
        payload=dict(m.payload),
        timestamp_utc=m.timestamp_utc,
    )


def refresh_token_to_domain(m: RefreshTokenModel) -> RefreshToken:
    return RefreshToken(
        id=m.id,
        user_id=m.user_id,
        token_hash=m.token_hash,
        family_id=m.family_id,
        is_revoked=m.is_revoked,
        expires_at_utc=m.expires_at_utc,
        created_at_utc=m.created_at_utc,
    )


def course_to_domain(m: CourseModel) -> Course:
    return Course(
        id=m.id,
        department_id=m.department_id,
        code=m.code,
        name=m.name,
        credits=m.credits,
    )


def section_to_domain(m: SectionModel) -> Section:
    return Section(
        id=m.id,
        course_id=m.course_id,
        name=m.name,
    )


def room_to_domain(m: RoomModel) -> Room:
    return Room(
        id=m.id,
        code=m.code,
        building=m.building,
        capacity=m.capacity,
    )


def timetable_upload_to_domain(m: TimetableUploadModel) -> TimetableUpload:
    return TimetableUpload(
        id=m.id,
        department_id=m.department_id,
        academic_term_id=m.academic_term_id,
        file_key=m.file_key,
        status=TimetableUploadStatus(m.status),
        parse_report=dict(m.parse_report),
        uploaded_at_utc=m.uploaded_at_utc,
    )


def timetable_slot_to_domain(m: TimetableSlotModel) -> TimetableSlot:
    return TimetableSlot(
        id=m.id,
        timetable_upload_id=m.timetable_upload_id,
        time_slot=TimeSlot(
            weekday=m.weekday,
            start_time=m.start_time,
            end_time=m.end_time,
        ),
        course_id=m.course_id,
        section_id=m.section_id,
        room_id=m.room_id,
        faculty_id=m.faculty_id,
        source_cell_reference=m.source_cell_reference,
    )


class DepartmentRepositoryImpl(DepartmentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, department_id: UUID) -> Department | None:
        stmt = select(DepartmentModel).where(DepartmentModel.id == department_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return department_to_domain(model) if model else None

    async def get_by_code(self, code: str) -> Department | None:
        stmt = select(DepartmentModel).where(DepartmentModel.code == code)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return department_to_domain(model) if model else None

    async def list_all(self) -> list[Department]:
        stmt = select(DepartmentModel).order_by(DepartmentModel.code)
        result = await self._session.execute(stmt)
        return [department_to_domain(m) for m in result.scalars().all()]

    async def save(self, department: Department) -> Department:
        model = await self._session.get(DepartmentModel, department.id)
        if model is None:
            model = DepartmentModel(
                id=department.id,
                code=department.code,
                name=department.name,
            )
            self._session.add(model)
        else:
            model.code = department.code
            model.name = department.name
        await self._session.flush()
        return department_to_domain(model)


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return user_to_domain(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return user_to_domain(model) if model else None

    async def save(self, user: User) -> User:
        model = await self._session.get(UserModel, user.id)
        if model is None:
            model = UserModel(
                id=user.id,
                email=user.email,
                password_hash=user.password_hash,
                role=user.role.value,
                is_active=user.is_active,
                quiet_hours_start=user.quiet_hours_start,
                quiet_hours_end=user.quiet_hours_end,
            )
            self._session.add(model)
        else:
            model.email = user.email
            model.password_hash = user.password_hash
            model.role = user.role.value
            model.is_active = user.is_active
            model.quiet_hours_start = user.quiet_hours_start
            model.quiet_hours_end = user.quiet_hours_end
        await self._session.flush()
        return user_to_domain(model)


class FacultyProfileRepositoryImpl(FacultyProfileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, profile_id: UUID) -> FacultyProfile | None:
        stmt = select(FacultyProfileModel).where(FacultyProfileModel.id == profile_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return faculty_profile_to_domain(model) if model else None

    async def get_by_user_id(self, user_id: UUID) -> FacultyProfile | None:
        stmt = select(FacultyProfileModel).where(FacultyProfileModel.user_id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return faculty_profile_to_domain(model) if model else None

    async def get_by_department_and_initials(
        self, department_id: UUID, initials: Initials
    ) -> FacultyProfile | None:
        stmt = select(FacultyProfileModel).where(
            FacultyProfileModel.department_id == department_id,
            FacultyProfileModel.initials == initials.value,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return faculty_profile_to_domain(model) if model else None

    async def list_by_department(self, department_id: UUID) -> list[FacultyProfile]:
        stmt = (
            select(FacultyProfileModel)
            .where(FacultyProfileModel.department_id == department_id)
            .order_by(FacultyProfileModel.full_name)
        )
        result = await self._session.execute(stmt)
        return [faculty_profile_to_domain(m) for m in result.scalars().all()]

    async def list_all(self) -> list[FacultyProfile]:
        stmt = select(FacultyProfileModel).order_by(FacultyProfileModel.full_name)
        result = await self._session.execute(stmt)
        return [faculty_profile_to_domain(m) for m in result.scalars().all()]

    async def get_by_ics_token(self, token: str) -> FacultyProfile | None:
        stmt = select(FacultyProfileModel).where(FacultyProfileModel.ics_token == token)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return faculty_profile_to_domain(model) if model else None

    async def save(self, profile: FacultyProfile) -> FacultyProfile:
        model = await self._session.get(FacultyProfileModel, profile.id)
        if model is None:
            model = FacultyProfileModel(
                id=profile.id,
                user_id=profile.user_id,
                department_id=profile.department_id,
                full_name=profile.full_name,
                initials=profile.initials.value,
                aliases=list(profile.aliases),
                email=profile.email,
                phone=profile.phone,
                ics_token=profile.ics_token,
            )
            self._session.add(model)
        else:
            model.department_id = profile.department_id
            model.full_name = profile.full_name
            model.initials = profile.initials.value
            model.aliases = list(profile.aliases)
            model.email = profile.email
            model.phone = profile.phone
            model.ics_token = profile.ics_token
        await self._session.flush()
        return faculty_profile_to_domain(model)


class AcademicTermRepositoryImpl(AcademicTermRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, term_id: UUID) -> AcademicTerm | None:
        stmt = select(AcademicTermModel).where(AcademicTermModel.id == term_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return academic_term_to_domain(model) if model else None

    async def get_active_term(self, on_date: date) -> AcademicTerm | None:
        stmt = (
            select(AcademicTermModel)
            .where(
                AcademicTermModel.start_date <= on_date,
                AcademicTermModel.end_date >= on_date,
            )
            .order_by(AcademicTermModel.start_date.desc())
        )
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return academic_term_to_domain(model) if model else None

    async def save(self, term: AcademicTerm) -> AcademicTerm:
        model = await self._session.get(AcademicTermModel, term.id)
        if model is None:
            model = AcademicTermModel(
                id=term.id,
                name=term.name,
                start_date=term.start_date,
                end_date=term.end_date,
                timezone=term.timezone,
            )
            self._session.add(model)
        else:
            model.name = term.name
            model.start_date = term.start_date
            model.end_date = term.end_date
            model.timezone = term.timezone
        await self._session.flush()
        return academic_term_to_domain(model)

    async def list_all(self) -> list[AcademicTerm]:
        stmt = select(AcademicTermModel).order_by(AcademicTermModel.start_date.desc())
        result = await self._session.execute(stmt)
        return [academic_term_to_domain(m) for m in result.scalars().all()]

    async def list_holidays(self, term_id: UUID) -> list[Holiday]:
        stmt = (
            select(HolidayModel)
            .where(HolidayModel.academic_term_id == term_id)
            .order_by(HolidayModel.date)
        )
        result = await self._session.execute(stmt)
        return [holiday_to_domain(m) for m in result.scalars().all()]

    async def list_all_holidays(self) -> list[Holiday]:
        stmt = select(HolidayModel).order_by(HolidayModel.date)
        result = await self._session.execute(stmt)
        return [holiday_to_domain(m) for m in result.scalars().all()]

    async def save_holiday(self, holiday: Holiday) -> Holiday:
        model = await self._session.get(HolidayModel, holiday.id)
        if model is None:
            model = HolidayModel(
                id=holiday.id,
                academic_term_id=holiday.academic_term_id,
                date=holiday.date,
                label=holiday.label,
            )
            self._session.add(model)
        else:
            model.date = holiday.date
            model.label = holiday.label
        await self._session.flush()
        return holiday_to_domain(model)


class EventRepositoryImpl(EventRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, event_id: UUID) -> Event | None:
        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.attendees))
            .where(EventModel.id == event_id)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return event_to_domain(model) if model else None

    async def list_by_faculty_and_range(
        self, faculty_id: UUID, start_utc: datetime, end_utc: datetime
    ) -> list[Event]:
        stmt = (
            select(EventModel)
            .join(EventAttendeeModel, EventAttendeeModel.event_id == EventModel.id)
            .options(selectinload(EventModel.attendees))
            .where(
                EventAttendeeModel.faculty_id == faculty_id,
                EventModel.start_utc < end_utc,
                EventModel.end_utc > start_utc,
            )
            .order_by(EventModel.start_utc)
        )
        result = await self._session.execute(stmt)
        return [event_to_domain(m) for m in result.scalars().all()]

    async def save(self, event: Event) -> Event:
        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.attendees))
            .where(EventModel.id == event.id)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            model = EventModel(
                id=event.id,
                kind=event.kind.value,
                title=event.title,
                start_utc=event.start_utc,
                end_utc=event.end_utc,
                location=event.location,
                source=event.source.value,
                source_id=event.source_id,
                recurrence_date=event.recurrence_date,
            )
            self._session.add(model)
            for domain_att in event.attendees:
                att_model = EventAttendeeModel(
                    id=domain_att.id,
                    event_id=model.id,
                    faculty_id=domain_att.faculty_id,
                    response=domain_att.response.value,
                )
                self._session.add(att_model)
        else:
            model.kind = event.kind.value
            model.title = event.title
            model.start_utc = event.start_utc
            model.end_utc = event.end_utc
            model.location = event.location
            model.source = event.source.value
            model.source_id = event.source_id
            model.recurrence_date = event.recurrence_date

            existing_att = {att.faculty_id: att for att in model.attendees}
            target_faculty_ids = {att.faculty_id for att in event.attendees}

            for fid, att_model in list(existing_att.items()):
                if fid not in target_faculty_ids:
                    await self._session.delete(att_model)

            for domain_att in event.attendees:
                if domain_att.faculty_id in existing_att:
                    existing_att[domain_att.faculty_id].response = domain_att.response.value
                else:
                    new_att = EventAttendeeModel(
                        id=domain_att.id,
                        event_id=model.id,
                        faculty_id=domain_att.faculty_id,
                        response=domain_att.response.value,
                    )
                    self._session.add(new_att)

        await self._session.flush()
        reloaded = await self.get_by_id(event.id)
        assert reloaded is not None
        return reloaded

    async def delete(self, event_id: UUID) -> None:
        stmt = sa_delete(EventModel).where(EventModel.id == event_id)
        await self._session.execute(stmt)
        await self._session.flush()

    async def get_by_slot_and_date(self, slot_id: UUID, recurrence_date: date) -> Event | None:
        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.attendees))
            .where(
                EventModel.source_id == slot_id,
                EventModel.recurrence_date == recurrence_date,
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return event_to_domain(model) if model else None

    async def delete_future_by_slot(self, slot_id: UUID, from_date: date) -> None:
        stmt = sa_delete(EventModel).where(
            EventModel.source_id == slot_id,
            EventModel.recurrence_date >= from_date,
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def get_by_source_id(self, source_id: UUID) -> Event | None:
        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.attendees))
            .where(EventModel.source_id == source_id)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return event_to_domain(model) if model else None

    async def delete_by_source_id(self, source_id: UUID) -> None:
        stmt = sa_delete(EventModel).where(EventModel.source_id == source_id)
        await self._session.execute(stmt)
        await self._session.flush()


class CircularRepositoryImpl(CircularRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, circular_id: UUID) -> Circular | None:
        stmt = select(CircularModel).where(CircularModel.id == circular_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return circular_to_domain(model) if model else None

    async def list_pending_review(self) -> list[Circular]:
        stmt = (
            select(CircularModel)
            .where(CircularModel.status == CircularStatus.NEEDS_REVIEW.value)
            .order_by(CircularModel.created_at_utc.desc())
        )
        result = await self._session.execute(stmt)
        return [circular_to_domain(m) for m in result.scalars().all()]

    async def save(self, circular: Circular) -> Circular:
        model = await self._session.get(CircularModel, circular.id)
        old_status = model.status if model else None
        if model is None:
            model = CircularModel(
                id=circular.id,
                file_key=circular.file_key,
                ocr_text=circular.ocr_text,
                extracted_fields=circular.extracted_fields,
                confidence=circular.confidence,
                status=circular.status.value,
                failure_reason=circular.failure_reason,
            )
            self._session.add(model)
        else:
            model.file_key = circular.file_key
            model.ocr_text = circular.ocr_text
            model.extracted_fields = circular.extracted_fields
            model.confidence = circular.confidence
            model.status = circular.status.value
            model.failure_reason = circular.failure_reason
        await self._session.flush()
        if old_status != model.status:
            logger.info(
                "circular_state_transition",
                circular_id=str(model.id),
                from_status=old_status,
                to_status=model.status,
            )
        return circular_to_domain(model)


class NotificationRepositoryImpl(NotificationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, notification_id: UUID) -> ScheduledNotification | None:
        stmt = select(ScheduledNotificationModel).where(
            ScheduledNotificationModel.id == notification_id
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return notification_to_domain(model) if model else None

    async def get_by_idempotency_key(self, idempotency_key: str) -> ScheduledNotification | None:
        stmt = select(ScheduledNotificationModel).where(
            ScheduledNotificationModel.idempotency_key == idempotency_key
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return notification_to_domain(model) if model else None

    async def list_due(self, up_to_utc: datetime) -> list[ScheduledNotification]:
        stmt = (
            select(ScheduledNotificationModel)
            .where(
                ScheduledNotificationModel.status == NotificationStatus.PENDING.value,
                ScheduledNotificationModel.fire_at_utc <= up_to_utc,
            )
            .order_by(ScheduledNotificationModel.fire_at_utc)
        )
        result = await self._session.execute(stmt)
        return [notification_to_domain(m) for m in result.scalars().all()]

    async def claim_due_batch(self, up_to_utc: datetime, limit: int) -> list[ScheduledNotification]:
        stmt = (
            select(ScheduledNotificationModel)
            .where(
                ScheduledNotificationModel.status == NotificationStatus.PENDING.value,
                ScheduledNotificationModel.fire_at_utc <= up_to_utc,
            )
            .order_by(ScheduledNotificationModel.fire_at_utc.asc())
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        result = await self._session.execute(stmt)
        models = list(result.scalars().all())
        for m in models:
            logger.info(
                "notification_state_transition",
                notification_id=str(m.id),
                from_status=m.status,
                to_status=NotificationStatus.SENDING.value,
                channel=m.channel,
            )
            m.status = NotificationStatus.SENDING.value
            m.attempts += 1
        await self._session.flush()
        return [notification_to_domain(m) for m in models]

    async def recover_stale_sending(self, older_than_utc: datetime) -> int:
        stmt = (
            update(ScheduledNotificationModel)
            .where(
                ScheduledNotificationModel.status == NotificationStatus.SENDING.value,
                ScheduledNotificationModel.fire_at_utc <= older_than_utc,
            )
            .values(status=NotificationStatus.PENDING.value)
            .returning(ScheduledNotificationModel.id)
        )
        result = await self._session.execute(stmt)
        return len(result.scalars().all())

    async def list_by_user(
        self, user_id: UUID, status: NotificationStatus | None = None, limit: int = 50
    ) -> list[ScheduledNotification]:
        stmt = select(ScheduledNotificationModel).where(
            ScheduledNotificationModel.user_id == user_id
        )
        if status is not None:
            stmt = stmt.where(ScheduledNotificationModel.status == status.value)
        stmt = stmt.order_by(ScheduledNotificationModel.fire_at_utc.desc()).limit(limit)
        result = await self._session.execute(stmt)
        return [notification_to_domain(m) for m in result.scalars().all()]

    async def list_by_target(self, target_id: UUID) -> list[ScheduledNotification]:
        stmt = select(ScheduledNotificationModel).where(
            ScheduledNotificationModel.target_id == target_id
        )
        result = await self._session.execute(stmt)
        return [notification_to_domain(m) for m in result.scalars().all()]

    async def cancel_pending_by_target(self, target_id: UUID) -> int:
        stmt = (
            update(ScheduledNotificationModel)
            .where(
                ScheduledNotificationModel.target_id == target_id,
                ScheduledNotificationModel.status == NotificationStatus.PENDING.value,
            )
            .values(status=NotificationStatus.CANCELLED.value)
            .returning(ScheduledNotificationModel.id)
        )
        result = await self._session.execute(stmt)
        return len(result.scalars().all())

    async def count_by_status(self) -> dict[str, int]:
        stmt = select(
            ScheduledNotificationModel.status,
            func.count(ScheduledNotificationModel.id),
        ).group_by(ScheduledNotificationModel.status)
        result = await self._session.execute(stmt)
        return {str(status): int(count) for status, count in result.all()}

    async def list_delivered_lateness_samples(self, limit: int = 5000) -> list[float]:
        stmt = (
            select(
                func.extract(
                    "epoch",
                    ScheduledNotificationModel.delivered_at_utc
                    - ScheduledNotificationModel.fire_at_utc,
                )
            )
            .where(
                ScheduledNotificationModel.status == NotificationStatus.SENT.value,
                ScheduledNotificationModel.delivered_at_utc.is_not(None),
            )
            .order_by(ScheduledNotificationModel.delivered_at_utc.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [float(x) for x in result.scalars().all() if x is not None]

    async def list_dead_letters(self, limit: int = 50) -> list[ScheduledNotification]:
        stmt = (
            select(ScheduledNotificationModel)
            .where(ScheduledNotificationModel.status == NotificationStatus.FAILED.value)
            .order_by(ScheduledNotificationModel.fire_at_utc.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [notification_to_domain(m) for m in result.scalars().all()]

    async def save(self, notification: ScheduledNotification) -> ScheduledNotification:
        model = await self._session.get(ScheduledNotificationModel, notification.id)
        old_status = model.status if model else None
        if model is None:
            model = ScheduledNotificationModel(
                id=notification.id,
                target_id=notification.target_id,
                target_kind=notification.target_kind,
                user_id=notification.user_id,
                channel=notification.channel.value,
                fire_at_utc=notification.fire_at_utc,
                idempotency_key=notification.idempotency_key,
                attempts=notification.attempts,
                max_attempts=notification.max_attempts,
                last_error=notification.last_error,
                delivered_at_utc=notification.delivered_at_utc,
                status=notification.status.value,
            )
            self._session.add(model)
        else:
            model.channel = notification.channel.value
            model.fire_at_utc = notification.fire_at_utc
            model.attempts = notification.attempts
            model.max_attempts = notification.max_attempts
            model.last_error = notification.last_error
            model.delivered_at_utc = notification.delivered_at_utc
            model.status = notification.status.value
        await self._session.flush()
        if old_status != model.status:
            logger.info(
                "notification_state_transition",
                notification_id=str(model.id),
                from_status=old_status,
                to_status=model.status,
                channel=model.channel,
            )
        return notification_to_domain(model)


class ReminderRuleRepositoryImpl(ReminderRuleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_and_kind(
        self, user_id: UUID, event_kind: EventKind
    ) -> ReminderRule | None:
        stmt = select(ReminderRuleModel).where(
            ReminderRuleModel.user_id == user_id,
            ReminderRuleModel.event_kind == event_kind.value,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return reminder_rule_to_domain(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[ReminderRule]:
        stmt = select(ReminderRuleModel).where(ReminderRuleModel.user_id == user_id)
        result = await self._session.execute(stmt)
        return [reminder_rule_to_domain(m) for m in result.scalars().all()]

    async def save(self, rule: ReminderRule) -> ReminderRule:
        model = await self._session.get(ReminderRuleModel, rule.id)
        if model is None:
            model = ReminderRuleModel(
                id=rule.id,
                user_id=rule.user_id,
                event_kind=rule.event_kind.value,
                offsets_minutes=list(rule.offsets_minutes),
                channels=[c.value for c in rule.channels],
            )
            self._session.add(model)
        else:
            model.offsets_minutes = list(rule.offsets_minutes)
            model.channels = [c.value for c in rule.channels]
        await self._session.flush()
        return reminder_rule_to_domain(model)

    async def delete(self, rule_id: UUID) -> None:
        model = await self._session.get(ReminderRuleModel, rule_id)
        if model is not None:
            await self._session.delete(model)


class PushSubscriptionRepositoryImpl(PushSubscriptionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, subscription_id: UUID) -> PushSubscription | None:
        stmt = select(PushSubscriptionModel).where(PushSubscriptionModel.id == subscription_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return push_subscription_to_domain(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[PushSubscription]:
        stmt = select(PushSubscriptionModel).where(PushSubscriptionModel.user_id == user_id)
        result = await self._session.execute(stmt)
        return [push_subscription_to_domain(m) for m in result.scalars().all()]

    async def save(self, subscription: PushSubscription) -> PushSubscription:
        stmt = select(PushSubscriptionModel).where(
            PushSubscriptionModel.user_id == subscription.user_id,
            PushSubscriptionModel.endpoint == subscription.endpoint,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            model = PushSubscriptionModel(
                id=subscription.id,
                user_id=subscription.user_id,
                endpoint=subscription.endpoint,
                p256dh=subscription.p256dh,
                auth=subscription.auth,
            )
            self._session.add(model)
        else:
            model.p256dh = subscription.p256dh
            model.auth = subscription.auth
        await self._session.flush()
        return push_subscription_to_domain(model)

    async def delete_by_endpoint(self, endpoint: str) -> None:
        stmt = sa_delete(PushSubscriptionModel).where(PushSubscriptionModel.endpoint == endpoint)
        await self._session.execute(stmt)

    async def delete(self, subscription_id: UUID) -> None:
        model = await self._session.get(PushSubscriptionModel, subscription_id)
        if model is not None:
            await self._session.delete(model)


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, task_id: UUID) -> Task | None:
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return task_to_domain(model) if model else None

    async def list_by_assignee(
        self, assignee_id: UUID, status: TaskStatus | None = None
    ) -> list[Task]:
        stmt = select(TaskModel).where(TaskModel.assignee_id == assignee_id)
        if status is not None:
            stmt = stmt.where(TaskModel.status == status.value)
        stmt = stmt.order_by(TaskModel.deadline_utc.asc())
        result = await self._session.execute(stmt)
        return [task_to_domain(m) for m in result.scalars().all()]

    async def list_by_parent_assignment(self, parent_assignment_id: UUID) -> list[Task]:
        stmt = (
            select(TaskModel)
            .where(TaskModel.parent_assignment_id == parent_assignment_id)
            .order_by(TaskModel.deadline_utc.asc())
        )
        result = await self._session.execute(stmt)
        return [task_to_domain(m) for m in result.scalars().all()]

    async def list_by_assigner(self, assigner_id: UUID) -> list[Task]:
        stmt = (
            select(TaskModel)
            .where(TaskModel.assigner_id == assigner_id)
            .order_by(TaskModel.deadline_utc.asc())
        )
        result = await self._session.execute(stmt)
        return [task_to_domain(m) for m in result.scalars().all()]

    async def list_overdue(self, as_of_utc: datetime) -> list[Task]:
        stmt = (
            select(TaskModel)
            .where(
                TaskModel.status != TaskStatus.DONE.value,
                TaskModel.deadline_utc < as_of_utc,
            )
            .order_by(TaskModel.deadline_utc.asc())
        )
        result = await self._session.execute(stmt)
        return [task_to_domain(m) for m in result.scalars().all()]

    async def list_all(self) -> list[Task]:
        stmt = select(TaskModel).order_by(TaskModel.deadline_utc.asc())
        result = await self._session.execute(stmt)
        return [task_to_domain(m) for m in result.scalars().all()]

    async def save(self, task: Task) -> Task:
        model = await self._session.get(TaskModel, task.id)
        if model is None:
            model = TaskModel(
                id=task.id,
                title=task.title,
                description=task.description,
                deadline_utc=task.deadline_utc,
                importance=task.importance,
                category=task.category.value,
                status=task.status.value,
                assignee_id=task.assignee_id,
                assigner_id=task.assigner_id,
                parent_assignment_id=task.parent_assignment_id,
                recurrence=task.recurrence.value if task.recurrence else None,
                created_at_utc=task.created_at_utc,
            )
            self._session.add(model)
        else:
            model.title = task.title
            model.description = task.description
            model.deadline_utc = task.deadline_utc
            model.importance = task.importance
            model.category = task.category.value
            model.status = task.status.value
            model.assignee_id = task.assignee_id
            model.assigner_id = task.assigner_id
            model.parent_assignment_id = task.parent_assignment_id
            model.recurrence = task.recurrence.value if task.recurrence else None
        await self._session.flush()
        return task_to_domain(model)

    async def delete(self, task_id: UUID) -> None:
        model = await self._session.get(TaskModel, task_id)
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()


class TaskTemplateRepositoryImpl(TaskTemplateRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, template_id: UUID) -> TaskTemplate | None:
        stmt = select(TaskTemplateModel).where(TaskTemplateModel.id == template_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return task_template_to_domain(model) if model else None

    async def list_by_department(self, department_id: UUID | None) -> list[TaskTemplate]:
        if department_id is None:
            stmt = select(TaskTemplateModel).where(TaskTemplateModel.department_id.is_(None))
        else:
            stmt = select(TaskTemplateModel).where(
                (TaskTemplateModel.department_id == department_id)
                | (TaskTemplateModel.department_id.is_(None))
            )
        stmt = stmt.order_by(TaskTemplateModel.title.asc())
        result = await self._session.execute(stmt)
        return [task_template_to_domain(m) for m in result.scalars().all()]

    async def save(self, template: TaskTemplate) -> TaskTemplate:
        model = await self._session.get(TaskTemplateModel, template.id)
        if model is None:
            model = TaskTemplateModel(
                id=template.id,
                department_id=template.department_id,
                title=template.title,
                description=template.description,
                category=template.category.value,
                default_lead_days=template.default_lead_days,
                default_importance=template.default_importance,
            )
            self._session.add(model)
        else:
            model.department_id = template.department_id
            model.title = template.title
            model.description = template.description
            model.category = template.category.value
            model.default_lead_days = template.default_lead_days
            model.default_importance = template.default_importance
        await self._session.flush()
        return task_template_to_domain(model)

    async def delete(self, template_id: UUID) -> None:
        model = await self._session.get(TaskTemplateModel, template_id)
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()


class AuditLogRepositoryImpl(AuditLogRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, audit_log: AuditLog) -> AuditLog:
        model = AuditLogModel(
            id=audit_log.id,
            user_id=audit_log.user_id,
            action=audit_log.action,
            resource_type=audit_log.resource_type,
            resource_id=audit_log.resource_id,
            payload=audit_log.payload,
            timestamp_utc=audit_log.timestamp_utc,
        )
        self._session.add(model)
        await self._session.flush()
        return audit_log_to_domain(model)

    async def list_by_resource(self, resource_type: str, resource_id: str) -> list[AuditLog]:
        stmt = (
            select(AuditLogModel)
            .where(
                AuditLogModel.resource_type == resource_type,
                AuditLogModel.resource_id == resource_id,
            )
            .order_by(AuditLogModel.timestamp_utc.desc())
        )
        result = await self._session.execute(stmt)
        return [audit_log_to_domain(m) for m in result.scalars().all()]


class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return refresh_token_to_domain(model) if model else None

    async def save(self, token: RefreshToken) -> RefreshToken:
        model = await self._session.get(RefreshTokenModel, token.id)
        if model is None:
            model = RefreshTokenModel(
                id=token.id,
                user_id=token.user_id,
                token_hash=token.token_hash,
                family_id=token.family_id,
                is_revoked=token.is_revoked,
                expires_at_utc=token.expires_at_utc,
                created_at_utc=token.created_at_utc,
            )
            self._session.add(model)
        else:
            model.is_revoked = token.is_revoked
            model.expires_at_utc = token.expires_at_utc
        await self._session.flush()
        return refresh_token_to_domain(model)

    async def revoke_family(self, family_id: UUID) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.family_id == family_id)
            .values(is_revoked=True)
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.user_id == user_id)
            .values(is_revoked=True)
        )
        await self._session.execute(stmt)
        await self._session.flush()


class CourseRepositoryImpl(CourseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, course_id: UUID) -> Course | None:
        stmt = select(CourseModel).where(CourseModel.id == course_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return course_to_domain(model) if model else None

    async def get_by_department_and_code(self, department_id: UUID, code: str) -> Course | None:
        stmt = select(CourseModel).where(
            CourseModel.department_id == department_id,
            CourseModel.code == code,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return course_to_domain(model) if model else None

    async def save(self, course: Course) -> Course:
        model = await self._session.get(CourseModel, course.id)
        if model is None:
            model = CourseModel(
                id=course.id,
                department_id=course.department_id,
                code=course.code,
                name=course.name,
                credits=course.credits,
            )
            self._session.add(model)
        else:
            model.code = course.code
            model.name = course.name
            model.credits = course.credits
        await self._session.flush()
        return course_to_domain(model)


class SectionRepositoryImpl(SectionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, section_id: UUID) -> Section | None:
        stmt = select(SectionModel).where(SectionModel.id == section_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return section_to_domain(model) if model else None

    async def get_by_course_and_name(self, course_id: UUID, name: str) -> Section | None:
        stmt = select(SectionModel).where(
            SectionModel.course_id == course_id,
            SectionModel.name == name,
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return section_to_domain(model) if model else None

    async def save(self, section: Section) -> Section:
        model = await self._session.get(SectionModel, section.id)
        if model is None:
            model = SectionModel(
                id=section.id,
                course_id=section.course_id,
                name=section.name,
            )
            self._session.add(model)
        else:
            model.name = section.name
        await self._session.flush()
        return section_to_domain(model)


class RoomRepositoryImpl(RoomRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, room_id: UUID) -> Room | None:
        stmt = select(RoomModel).where(RoomModel.id == room_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return room_to_domain(model) if model else None

    async def get_by_code(self, code: str) -> Room | None:
        stmt = select(RoomModel).where(RoomModel.code == code)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return room_to_domain(model) if model else None

    async def save(self, room: Room) -> Room:
        model = await self._session.get(RoomModel, room.id)
        if model is None:
            model = RoomModel(
                id=room.id,
                code=room.code,
                building=room.building,
                capacity=room.capacity,
            )
            self._session.add(model)
        else:
            model.building = room.building
            model.capacity = room.capacity
        await self._session.flush()
        return room_to_domain(model)


class TimetableUploadRepositoryImpl(TimetableUploadRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, upload_id: UUID) -> TimetableUpload | None:
        stmt = select(TimetableUploadModel).where(TimetableUploadModel.id == upload_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return timetable_upload_to_domain(model) if model else None

    async def list_by_term_id(self, term_id: UUID) -> list[TimetableUpload]:
        stmt = (
            select(TimetableUploadModel)
            .where(TimetableUploadModel.academic_term_id == term_id)
            .order_by(TimetableUploadModel.uploaded_at_utc.desc())
        )
        result = await self._session.execute(stmt)
        return [timetable_upload_to_domain(m) for m in result.scalars().all()]

    async def save(self, upload: TimetableUpload) -> TimetableUpload:

        model = await self._session.get(TimetableUploadModel, upload.id)
        if model is None:
            model = TimetableUploadModel(
                id=upload.id,
                department_id=upload.department_id,
                academic_term_id=upload.academic_term_id,
                file_key=upload.file_key,
                status=upload.status.value,
                parse_report=upload.parse_report,
                uploaded_at_utc=upload.uploaded_at_utc,
            )
            self._session.add(model)
        else:
            model.status = upload.status.value
            model.parse_report = upload.parse_report
            model.uploaded_at_utc = upload.uploaded_at_utc
        await self._session.flush()
        return timetable_upload_to_domain(model)


class TimetableSlotRepositoryImpl(TimetableSlotRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_upload_id(self, upload_id: UUID) -> list[TimetableSlot]:
        stmt = (
            select(TimetableSlotModel)
            .where(TimetableSlotModel.timetable_upload_id == upload_id)
            .order_by(TimetableSlotModel.weekday, TimetableSlotModel.start_time)
        )
        result = await self._session.execute(stmt)
        return [timetable_slot_to_domain(m) for m in result.scalars().all()]

    async def list_by_faculty_id(self, faculty_id: UUID) -> list[TimetableSlot]:
        stmt = (
            select(TimetableSlotModel)
            .where(TimetableSlotModel.faculty_id == faculty_id)
            .order_by(TimetableSlotModel.weekday, TimetableSlotModel.start_time)
        )
        result = await self._session.execute(stmt)
        return [timetable_slot_to_domain(m) for m in result.scalars().all()]

    async def save_all(self, slots: list[TimetableSlot]) -> list[TimetableSlot]:
        saved_models: list[TimetableSlotModel] = []
        for slot in slots:
            model = await self._session.get(TimetableSlotModel, slot.id)
            if model is None:
                model = TimetableSlotModel(
                    id=slot.id,
                    timetable_upload_id=slot.timetable_upload_id,
                    weekday=slot.time_slot.weekday,
                    start_time=slot.time_slot.start_time,
                    end_time=slot.time_slot.end_time,
                    course_id=slot.course_id,
                    section_id=slot.section_id,
                    room_id=slot.room_id,
                    faculty_id=slot.faculty_id,
                    source_cell_reference=slot.source_cell_reference,
                )
                self._session.add(model)
            else:
                model.weekday = slot.time_slot.weekday
                model.start_time = slot.time_slot.start_time
                model.end_time = slot.time_slot.end_time
                model.course_id = slot.course_id
                model.section_id = slot.section_id
                model.room_id = slot.room_id
                model.faculty_id = slot.faculty_id
                model.source_cell_reference = slot.source_cell_reference
            saved_models.append(model)
        await self._session.flush()
        return [timetable_slot_to_domain(m) for m in saved_models]

    async def delete_by_upload_id(self, upload_id: UUID) -> None:
        stmt = sa_delete(TimetableSlotModel).where(
            TimetableSlotModel.timetable_upload_id == upload_id
        )
        await self._session.execute(stmt)
        await self._session.flush()


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        self.departments = DepartmentRepositoryImpl(self._session)
        self.users = UserRepositoryImpl(self._session)
        self.faculty_profiles = FacultyProfileRepositoryImpl(self._session)
        self.academic_terms = AcademicTermRepositoryImpl(self._session)
        self.events = EventRepositoryImpl(self._session)
        self.circulars = CircularRepositoryImpl(self._session)
        self.notifications = NotificationRepositoryImpl(self._session)
        self.reminder_rules = ReminderRuleRepositoryImpl(self._session)
        self.push_subscriptions = PushSubscriptionRepositoryImpl(self._session)
        self.tasks = TaskRepositoryImpl(self._session)
        self.task_templates = TaskTemplateRepositoryImpl(self._session)
        self.audit_logs = AuditLogRepositoryImpl(self._session)
        self.refresh_tokens = RefreshTokenRepositoryImpl(self._session)
        self.timetable_uploads = TimetableUploadRepositoryImpl(self._session)
        self.timetable_slots = TimetableSlotRepositoryImpl(self._session)
        self.courses = CourseRepositoryImpl(self._session)
        self.sections = SectionRepositoryImpl(self._session)
        self.rooms = RoomRepositoryImpl(self._session)
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object
    ) -> None:
        if self._session:
            if exc_type is not None:
                await self.rollback()
            await self._session.close()

    async def commit(self) -> None:
        if self._session:
            await self._session.commit()

    async def rollback(self) -> None:
        if self._session:
            await self._session.rollback()
