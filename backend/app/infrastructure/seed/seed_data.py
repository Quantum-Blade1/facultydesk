import asyncio
from datetime import date
from uuid import uuid4

from app.core.db import async_session_factory
from app.core.security import hash_password
from app.domain import (
    AcademicTerm,
    Department,
    FacultyProfile,
    Holiday,
    Initials,
    Role,
    TaskCategory,
    TaskTemplate,
    User,
)
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork


async def seed_database() -> None:
    uow = SqlAlchemyUnitOfWork(async_session_factory)
    async with uow:
        dept = await uow.departments.get_by_code("CSE")
        if dept is None:
            dept = Department(
                id=uuid4(),
                code="CSE",
                name="Computer Science and Engineering",
            )
            dept = await uow.departments.save(dept)

        admin = await uow.users.get_by_email("admin@facultydesk.local")
        if admin is None:
            admin = User(
                id=uuid4(),
                email="admin@facultydesk.local",
                password_hash=hash_password("Admin123!"),
                role=Role.ADMIN,
                is_active=True,
            )
            await uow.users.save(admin)

        hod_user = await uow.users.get_by_email("hod.cse@facultydesk.local")
        if hod_user is None:
            hod_user = User(
                id=uuid4(),
                email="hod.cse@facultydesk.local",
                password_hash=hash_password("Hod123!"),
                role=Role.HOD,
                is_active=True,
            )
            hod_user = await uow.users.save(hod_user)

            hod_profile = FacultyProfile(
                id=uuid4(),
                user_id=hod_user.id,
                department_id=dept.id,
                full_name="Dr. Head of Department",
                initials=Initials("HOD"),
                aliases=("HOD CSE", "Department Head"),
                email=hod_user.email,
                phone="+919876543210",
            )
            await uow.faculty_profiles.save(hod_profile)

        faculty_specs = [
            (
                "KKS",
                "Dr. Krish Kumar Sharma",
                "kks@facultydesk.local",
                ("K. K. Sharma", "Krish Kumar"),
            ),
            ("CN", "Prof. C. Naveen", "cn@facultydesk.local", ("C. Naveen", "Naveen C")),
            (
                "RSV",
                "Dr. R. S. Venkatesh",
                "rsv@facultydesk.local",
                ("R. S. Venkatesh", "Venkatesh R S"),
            ),
            ("AP", "Prof. Ananya Patel", "ap@facultydesk.local", ("A. Patel", "Ananya P")),
            (
                "MKS",
                "Dr. Manoj Kumar Singh",
                "mks@facultydesk.local",
                ("M. K. Singh", "Manoj Singh"),
            ),
            ("SBR", "Prof. S. B. Rao", "sbr@facultydesk.local", ("S. B. Rao", "Rao S B")),
            ("VK", "Prof. Vikas Kumar", "vk@facultydesk.local", ("V. Kumar", "Vikas K")),
            ("RTR", "Dr. R. T. Raman", "rtr@facultydesk.local", ("R. T. Raman", "Raman R T")),
            ("RS", "Prof. Rohit Sharma", "rs@facultydesk.local", ("R. Sharma", "Rohit S")),
            ("PN", "Prof. Priya Nair", "pn@facultydesk.local", ("P. Nair", "Priya N")),
        ]

        for inits_str, name, email, aliases in faculty_specs:
            user = await uow.users.get_by_email(email)
            if user is None:
                user = User(
                    id=uuid4(),
                    email=email,
                    password_hash=hash_password("Faculty123!"),
                    role=Role.FACULTY,
                    is_active=True,
                )
                user = await uow.users.save(user)

                profile = FacultyProfile(
                    id=uuid4(),
                    user_id=user.id,
                    department_id=dept.id,
                    full_name=name,
                    initials=Initials(inits_str),
                    aliases=aliases,
                    email=email,
                )
                await uow.faculty_profiles.save(profile)

        term_start = date(2026, 8, 1)
        term_end = date(2026, 12, 31)
        term = await uow.academic_terms.get_active_term(date(2026, 9, 1))
        if term is None:
            term = AcademicTerm(
                id=uuid4(),
                name="Odd Semester 2026-27",
                start_date=term_start,
                end_date=term_end,
                timezone="Asia/Kolkata",
            )
            term = await uow.academic_terms.save(term)

            holidays = [
                (date(2026, 8, 15), "Independence Day"),
                (date(2026, 10, 2), "Gandhi Jayanti"),
                (date(2026, 10, 20), "Dussehra"),
                (date(2026, 11, 9), "Diwali"),
                (date(2026, 12, 25), "Christmas"),
            ]
            for h_date, label in holidays:
                h = Holiday(
                    id=uuid4(),
                    academic_term_id=term.id,
                    date=h_date,
                    label=label,
                )
                await uow.academic_terms.save_holiday(h)

        templates_spec = [
            (
                "CO-PO mapping",
                "Map Course Outcomes to Program Outcomes for assigned courses.",
                TaskCategory.ACADEMIC_DOCUMENTATION,
                14,
                4,
            ),
            (
                "IA marks upload",
                "Upload Internal Assessment test marks to the departmental portal.",
                TaskCategory.EXAM_WORK,
                7,
                5,
            ),
            (
                "Attendance shortage report",
                "Generate and submit list of students with attendance below 75%.",
                TaskCategory.ACADEMIC_DOCUMENTATION,
                3,
                4,
            ),
            (
                "Lab manual update",
                "Review and update lab experiment procedures and rubrics.",
                TaskCategory.ACADEMIC_DOCUMENTATION,
                21,
                3,
            ),
            (
                "Course file submission",
                "Submit complete course file including syllabus, notes, question papers.",
                TaskCategory.ACADEMIC_DOCUMENTATION,
                10,
                4,
            ),
        ]
        existing_templates = await uow.task_templates.list_by_department(dept.id)
        existing_titles = {t.title for t in existing_templates}
        for title, desc, cat, lead_days, imp in templates_spec:
            if title not in existing_titles:
                tpl = TaskTemplate(
                    id=uuid4(),
                    department_id=dept.id,
                    title=title,
                    description=desc,
                    category=cat,
                    default_lead_days=lead_days,
                    default_importance=imp,
                )
                await uow.task_templates.save(tpl)

        await uow.commit()


def main() -> None:
    asyncio.run(seed_database())


if __name__ == "__main__":
    main()
