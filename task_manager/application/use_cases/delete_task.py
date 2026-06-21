from __future__ import annotations

from uuid import UUID

from task_manager.domain.exceptions import TaskNotFoundError
from task_manager.domain.interfaces.task_repository import TaskRepository


class DeleteTask:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(self, task_id: UUID, user_id: UUID) -> None:
        task = self.repository.get_by_id(task_id)
        if task is None or task.user_id != user_id:
            raise TaskNotFoundError(task_id)
        self.repository.delete(task_id)
