from typing import Any
from uuid import UUID

from app.domain import EntityNotFound, TimetableUpload, UnitOfWork
from app.infrastructure.parsers.factory import TimetableParserFactory
from app.infrastructure.parsers.initials_resolver import InitialsResolver
from app.infrastructure.storage.minio_storage import MinioStorageService


class ParseTimetableUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        storage: MinioStorageService,
    ) -> None:
        self._uow = uow
        self._storage = storage

    async def execute(self, upload_id: UUID) -> dict[str, Any]:
        async with self._uow:
            upload: TimetableUpload | None = await self._uow.timetable_uploads.get_by_id(
                upload_id
            )
            if upload is None:
                raise EntityNotFound("TimetableUpload", str(upload_id))

            upload.start_parsing()
            await self._uow.timetable_uploads.save(upload)
            await self._uow.commit()

        try:
            content = self._storage.download_file(upload.file_key)
            parser = TimetableParserFactory.get_parser(content, upload.file_key)
            parse_result = parser.parse(content)
        except Exception as e:
            async with self._uow:
                upload = await self._uow.timetable_uploads.get_by_id(upload_id)
                if upload:
                    upload.fail(str(e))
                    await self._uow.timetable_uploads.save(upload)
                    await self._uow.commit()
            raise

        async with self._uow:
            profiles = await self._uow.faculty_profiles.list_by_department(
                upload.department_id
            )
            resolver = InitialsResolver(profiles)

            preview_slots: list[dict[str, Any]] = []
            unresolved_tokens: list[dict[str, Any]] = []

            for candidate in parse_result.candidates:
                for init in candidate.raw_initials:
                    outcome = resolver.resolve(init)
                    if outcome.status == "RESOLVED" and outcome.faculty_id:
                        preview_slots.append(
                            {
                                "weekday": candidate.weekday,
                                "start_time": candidate.start_time.isoformat(),
                                "end_time": candidate.end_time.isoformat(),
                                "course_code": candidate.course_code,
                                "section_name": candidate.section_name,
                                "room_code": candidate.room_code,
                                "faculty_id": str(outcome.faculty_id),
                                "faculty_initials": outcome.candidate_initials,
                                "source_cell": candidate.source_cell,
                            }
                        )
                    else:
                        unresolved_tokens.append(
                            {
                                "cell": candidate.source_cell,
                                "token": init,
                                "status": outcome.status,
                                "reason": outcome.error_detail,
                            }
                        )

            for un in parse_result.unparsed_cells:
                unresolved_tokens.append(un)

            parse_report: dict[str, Any] = {
                "preview_slots": preview_slots,
                "unresolved_tokens": unresolved_tokens,
                "total_slots": len(preview_slots),
                "unresolved_count": len(unresolved_tokens),
            }

            upload = await self._uow.timetable_uploads.get_by_id(upload_id)
            if upload is None:
                raise EntityNotFound("TimetableUpload", str(upload_id))

            upload.mark_preview_ready(parse_report)
            await self._uow.timetable_uploads.save(upload)
            await self._uow.commit()

            return parse_report
