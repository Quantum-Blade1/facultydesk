from dataclasses import dataclass
from uuid import UUID

from app.core.errors import ForbiddenError
from app.domain import Role


@dataclass(frozen=True)
class Principal:
    user_id: UUID
    role: Role
    department_id: UUID | None = None


class AuthorisationPolicy:
    @staticmethod
    def can_access(
        principal: Principal,
        resource_owner_id: UUID | None = None,
        resource_dept_id: UUID | None = None,
        action: str = "read",
    ) -> bool:
        if principal.role == Role.ADMIN:
            return True

        if principal.role == Role.HOD:
            if resource_dept_id is not None and principal.department_id is not None:
                return principal.department_id == resource_dept_id
            return False

        if principal.role == Role.FACULTY:
            if resource_owner_id is not None:
                return principal.user_id == resource_owner_id
            return False

    @classmethod
    def enforce(
        cls,
        principal: Principal,
        resource_owner_id: UUID | None = None,
        resource_dept_id: UUID | None = None,
        action: str = "read",
    ) -> None:
        if not cls.can_access(principal, resource_owner_id, resource_dept_id, action):
            msg = (
                f"Principal {principal.user_id} with role {principal.role.value} "
                f"is not authorized to perform '{action}' on this resource"
            )
            raise ForbiddenError(msg)
