from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from task_manager.domain.entities.task import Task, TaskPriority, TaskStatus


class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:
        ...

    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Task | None:
        ...

    @abstractmethod
    def list_by_user(
        self,
        user_id: UUID,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Task]:
        ...

    @abstractmethod
    def delete(self, task_id: UUID) -> None:
        ...
