from __future__ import annotations

from uuid import UUID


class TaskNotFoundError(Exception):
    def __init__(self, task_id: UUID) -> None:
        super().__init__(f"Task {task_id} not found")
        self.task_id = task_id


class UserAlreadyExistsError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"User with email {email} already exists")
        self.email = email


class InvalidCredentialsError(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid email or password")
