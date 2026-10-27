from datetime import time
from uuid import UUID, uuid4

from app.application.calendar.use_cases import MaterialiseTimetableEventsUseCase
from app.application.security.policy import AuthorisationPolicy, Principal
from app.core.clock import Clock
from app.domain import (
    AuditLog,
    Course,
    EntityNotFound,
    InvariantViolation,
    Room,
    Section,
    TimeSlot,
    TimetableConfirmed,
    TimetableSlot,
    TimetableUpload,
    UnitOfWork,
)


class ConfirmTimetableUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        principal: Principal,
        upload_id: UUID,
    ) -> tuple[int, TimetableConfirmed]:
        async with self._uow:
            upload: TimetableUpload | None = await self._uow.timetable_uploads.get_by_id(
                upload_id
            )
            if upload is None:
                raise EntityNotFound("TimetableUpload", str(upload_id))

            AuthorisationPolicy.enforce(
                principal,
                resource_dept_id=upload.department_id,
                action="confirm_timetable",
            )

            upload.confirm()

            preview_slots = upload.parse_report.get("preview_slots", [])
            if not preview_slots:
                raise InvariantViolation("No valid preview slots available to confirm")

            course_cache: dict[str, Course] = {}
            section_cache: dict[tuple[UUID, str], Section] = {}
            room_cache: dict[str, Room] = {}

            domain_slots: list[TimetableSlot] = []

            for slot_data in preview_slots:
                c_code = slot_data["course_code"].strip().upper()
                if c_code not in course_cache:
                    c = await self._uow.courses.get_by_department_and_code(
                        upload.department_id, c_code
                    )
                    if c is None:
                        c = Course(
                            id=uuid4(),
                            department_id=upload.department_id,
                            code=c_code,
                            name=c_code,
                            credits=3,
                        )
                        c = await self._uow.courses.save(c)
                    course_cache[c_code] = c
                course = course_cache[c_code]

                sec_name = (slot_data.get("section_name") or "A").strip()
                sec_key = (course.id, sec_name)
                if sec_key not in section_cache:
                    sec = await self._uow.sections.get_by_course_and_name(
                        course.id, sec_name
                    )
                    if sec is None:
                        sec = Section(id=uuid4(), course_id=course.id, name=sec_name)
                        sec = await self._uow.sections.save(sec)
                    section_cache[sec_key] = sec
                section = section_cache[sec_key]

                r_code = (slot_data.get("room_code") or "TBD").strip().upper()
                if r_code not in room_cache:
                    rm = await self._uow.rooms.get_by_code(r_code)
                    if rm is None:
                        rm = Room(id=uuid4(), code=r_code, building="Campus", capacity=60)
                        rm = await self._uow.rooms.save(rm)
                    room_cache[r_code] = rm
                room = room_cache[r_code]

                t_slot = TimeSlot(
                    weekday=int(slot_data["weekday"]),
                    start_time=time.fromisoformat(slot_data["start_time"]),
                    end_time=time.fromisoformat(slot_data["end_time"]),
                )

                domain_slot = TimetableSlot(
                    id=uuid4(),
                    timetable_upload_id=upload.id,
                    time_slot=t_slot,
                    course_id=course.id,
                    section_id=section.id,
                    room_id=room.id,
                    faculty_id=UUID(slot_data["faculty_id"]),
                    source_cell_reference=slot_data.get("source_cell", ""),
                )
                domain_slots.append(domain_slot)

            await self._uow.timetable_slots.delete_by_upload_id(upload.id)
            await self._uow.timetable_slots.save_all(domain_slots)
            await self._uow.timetable_uploads.save(upload)

            materialiser = MaterialiseTimetableEventsUseCase(self._uow, self._clock)
            await materialiser.execute(upload.id)

            now_utc = self._clock.now()
            audit = AuditLog(
                id=uuid4(),
                user_id=principal.user_id,
                action="confirm_timetable",
                resource_type="timetable_upload",
                resource_id=str(upload_id),
                payload={
                    "slots_created": len(domain_slots),
                    "department_id": str(upload.department_id),
                    "academic_term_id": str(upload.academic_term_id),
                },
                timestamp_utc=now_utc,
            )
            await self._uow.audit_logs.save(audit)
            await self._uow.commit()

            event = TimetableConfirmed(
                upload_id=upload.id,
                department_id=upload.department_id,
                academic_term_id=upload.academic_term_id,
                slot_count=len(domain_slots),
            )
            return len(domain_slots), event
