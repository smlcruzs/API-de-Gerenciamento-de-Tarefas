from __future__ import annotations

from uuid import UUID

from task_manager.domain.entities.task import Task, TaskPriority, TaskStatus
from task_manager.domain.interfaces.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}

    def save(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def get_by_id(self, task_id: UUID) -> Task | None:
        return self._tasks.get(task_id)

    def list_by_user(
        self,
        user_id: UUID,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Task]:
        tasks = [t for t in self._tasks.values() if t.user_id == user_id]
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if priority is not None:
            tasks = [t for t in tasks if t.priority == priority]
        tasks.sort(key=lambda t: t.created_at)
        return tasks[offset : offset + limit]

    def delete(self, task_id: UUID) -> None:
        self._tasks.pop(task_id, None)
