from __future__ import annotations

from uuid import UUID

from task_manager.domain.entities.task import Task, TaskPriority, TaskStatus
from task_manager.domain.interfaces.task_repository import TaskRepository


class ListTasks:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(
        self,
        user_id: UUID,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Task]:
        return self.repository.list_by_user(
            user_id=user_id,
            status=status,
            priority=priority,
            limit=limit,
            offset=offset,
        )
