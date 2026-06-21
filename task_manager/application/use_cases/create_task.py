from __future__ import annotations

from datetime import date, datetime
from uuid import UUID, uuid4

from task_manager.domain.entities.task import Task, TaskPriority, TaskStatus
from task_manager.domain.interfaces.task_repository import TaskRepository


class CreateTask:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def execute(
        self,
        user_id: UUID,
        title: str,
        description: str | None = None,
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: date | None = None,
    ) -> Task:
        now = datetime.utcnow()
        task = Task(
            id=uuid4(),
            user_id=user_id,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            priority=priority,
            due_date=due_date,
            created_at=now,
            updated_at=now,
        )
        return self.repository.save(task)
