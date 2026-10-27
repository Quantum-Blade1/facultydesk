from datetime import date, datetime
from typing import Self
from uuid import UUID

from sqlalchemy import delete as sa_delete
from sqlalchemy import select
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
    Role,
    ScheduledNotification,
    Task,
    TaskRepository,
    TaskStatus,
    UnitOfWork,
    User,
    UserRepository,
)
from app.infrastructure.db.models import (
    AcademicTermModel,
    AuditLogModel,
    CircularModel,
    DepartmentModel,
    EventAttendeeModel,
    EventModel,
    FacultyProfileModel,
    HolidayModel,
    ScheduledNotificationModel,
    TaskModel,
    UserModel,
)


def department_to_domain(m: DepartmentModel) -> Department:
    return Department(id=m.id, code=m.code, name=m.name)


def user_to_domain(m: UserModel) -> User:
    return User(
        id=m.id,
        email=m.email,
        password_hash=m.password_hash,
        role=Role(m.role),
        is_active=m.is_active,
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
        status=NotificationStatus(m.status),
    )


def task_to_domain(m: TaskModel) -> Task:
    return Task(
        id=m.id,
        title=m.title,
        description=m.description,
        deadline_utc=m.deadline_utc,
        importance=m.importance,
        status=TaskStatus(m.status),
        assignee_id=m.assignee_id,
        assigner_id=m.assigner_id,
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
            )
            self._session.add(model)
        else:
            model.email = user.email
            model.password_hash = user.password_hash
            model.role = user.role.value
            model.is_active = user.is_active
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
            )
            self._session.add(model)
        else:
            model.department_id = profile.department_id
            model.full_name = profile.full_name
            model.initials = profile.initials.value
            model.aliases = list(profile.aliases)
            model.email = profile.email
            model.phone = profile.phone
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

    async def list_holidays(self, term_id: UUID) -> list[Holiday]:
        stmt = (
            select(HolidayModel)
            .where(HolidayModel.academic_term_id == term_id)
            .order_by(HolidayModel.date)
        )
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

    async def get_by_idempotency_key(
        self, idempotency_key: str
    ) -> ScheduledNotification | None:
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

    async def save(
        self, notification: ScheduledNotification
    ) -> ScheduledNotification:
        model = await self._session.get(ScheduledNotificationModel, notification.id)
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
                status=notification.status.value,
            )
            self._session.add(model)
        else:
            model.channel = notification.channel.value
            model.fire_at_utc = notification.fire_at_utc
            model.attempts = notification.attempts
            model.max_attempts = notification.max_attempts
            model.last_error = notification.last_error
            model.status = notification.status.value
        await self._session.flush()
        return notification_to_domain(model)


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, task_id: UUID) -> Task | None:
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return task_to_domain(model) if model else None

    async def list_by_assignee(self, assignee_id: UUID) -> list[Task]:
        stmt = (
            select(TaskModel)
            .where(TaskModel.assignee_id == assignee_id)
            .order_by(TaskModel.deadline_utc)
        )
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
                status=task.status.value,
                assignee_id=task.assignee_id,
                assigner_id=task.assigner_id,
            )
            self._session.add(model)
        else:
            model.title = task.title
            model.description = task.description
            model.deadline_utc = task.deadline_utc
            model.importance = task.importance
            model.status = task.status.value
            model.assignee_id = task.assignee_id
            model.assigner_id = task.assigner_id
        await self._session.flush()
        return task_to_domain(model)


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

    async def list_by_resource(
        self, resource_type: str, resource_id: str
    ) -> list[AuditLog]:
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
        self.tasks = TaskRepositoryImpl(self._session)
        self.audit_logs = AuditLogRepositoryImpl(self._session)
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
