class DomainError(Exception):
    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class InvariantViolation(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidTransition(DomainError):
    def __init__(self, current_state: str, target_state: str, entity_name: str) -> None:
        msg = (
            f"Invalid transition for {entity_name}: "
            f"cannot move from '{current_state}' to '{target_state}'"
        )
        super().__init__(msg)
        self.current_state = current_state
        self.target_state = target_state
        self.entity_name = entity_name


class EntityNotFound(DomainError):
    def __init__(self, entity_name: str, identifier: str) -> None:
        super().__init__(f"{entity_name} with identifier '{identifier}' was not found")
        self.entity_name = entity_name
        self.identifier = identifier


class ConflictError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ClashDetectedError(ConflictError):
    def __init__(self, message: str, clashes: list[dict[str, str]] | None = None) -> None:
        super().__init__(message)
        self.clashes = clashes or []

