from __future__ import annotations

from datetime import date
from uuid import UUID

from task_manager.domain.entities.task import Task, TaskPriority, TaskStatus
from task_manager.domain.exceptions import TaskNotFoundError
from task_manager.domain.interfaces.task_repository import TaskRepository


class UpdateTask:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(
        self,
        task_id: UUID,
        user_id: UUID,
        title: str | None = None,
        description: str | None = None,
        priority: TaskPriority | None = None,
        due_date: date | None = None,
        status: TaskStatus | None = None,
    ) -> Task:
        task = self._get_owned_task(task_id, user_id)
        task.update_details(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
        )
        if status is not None:
            task.update_status(status)
        return self.repository.save(task)

    def _get_owned_task(self, task_id: UUID, user_id: UUID) -> Task:
        task = self.repository.get_by_id(task_id)
        if task is None or task.user_id != user_id:
            raise TaskNotFoundError(task_id)
        return task
