from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from uuid import UUID

TITLE_MAX_LENGTH = 200


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    id: UUID
    user_id: UUID
    title: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
    description: str | None = None
    due_date: date | None = None

    def __post_init__(self) -> None:
        self._validate_title(self.title)

    @staticmethod
    def _validate_title(title: str) -> None:
        if not title.strip():
            raise ValueError("title must not be empty")
        if len(title) > TITLE_MAX_LENGTH:
            raise ValueError(f"title must be at most {TITLE_MAX_LENGTH} characters")

    def update_status(self, new_status: TaskStatus) -> None:
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def update_details(
        self,
        title: str | None = None,
        description: str | None = None,
        priority: TaskPriority | None = None,
        due_date: date | None = None,
    ) -> None:
        if title is not None:
            self._validate_title(title)
            self.title = title
        if description is not None:
            self.description = description
        if priority is not None:
            self.priority = priority
        if due_date is not None:
            self.due_date = due_date
        self.updated_at = datetime.utcnow()
