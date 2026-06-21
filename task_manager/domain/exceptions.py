from __future__ import annotations

from uuid import UUID


class TaskNotFoundError(Exception):
    def __init__(self, task_id: UUID) -> None:
        super().__init__(f"Task {task_id} not found")
        self.task_id = task_id
