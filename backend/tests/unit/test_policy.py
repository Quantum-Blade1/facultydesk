from uuid import uuid4

import pytest

from app.application.security.policy import AuthorisationPolicy, Principal
from app.core.errors import ForbiddenError
from app.domain import Role


def test_admin_policy_allows_all() -> None:
    principal = Principal(user_id=uuid4(), role=Role.ADMIN)
    owner_id = uuid4()
    dept_id = uuid4()

    assert AuthorisationPolicy.can_access(principal, owner_id, dept_id, "read")
    assert AuthorisationPolicy.can_access(principal, None, None, "delete")
    AuthorisationPolicy.enforce(principal, owner_id, dept_id, "manage")


def test_hod_policy_department_scoped() -> None:
    dept_a = uuid4()
    dept_b = uuid4()
    hod = Principal(user_id=uuid4(), role=Role.HOD, department_id=dept_a)

    assert AuthorisationPolicy.can_access(hod, resource_dept_id=dept_a)
    assert not AuthorisationPolicy.can_access(hod, resource_dept_id=dept_b)
    assert not AuthorisationPolicy.can_access(hod, resource_dept_id=None)

    with pytest.raises(ForbiddenError):
        AuthorisationPolicy.enforce(hod, resource_dept_id=dept_b, action="create_faculty")


def test_faculty_policy_user_scoped() -> None:
    user_a = uuid4()
    user_b = uuid4()
    faculty = Principal(user_id=user_a, role=Role.FACULTY, department_id=uuid4())

    assert AuthorisationPolicy.can_access(faculty, resource_owner_id=user_a)
    assert not AuthorisationPolicy.can_access(faculty, resource_owner_id=user_b)
    assert not AuthorisationPolicy.can_access(faculty, resource_owner_id=None)

    with pytest.raises(ForbiddenError):
        AuthorisationPolicy.enforce(faculty, resource_owner_id=user_b, action="update_profile")
