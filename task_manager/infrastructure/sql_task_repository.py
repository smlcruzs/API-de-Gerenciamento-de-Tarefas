from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from task_manager.domain.entities.task import Task, TaskPriority, TaskStatus
from task_manager.domain.interfaces.task_repository import TaskRepository
from task_manager.infrastructure.models import TaskModel


class SQLTaskRepository(TaskRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, task: Task) -> Task:
        model = self.session.get(TaskModel, task.id)
        if model is None:
            model = TaskModel(id=task.id)
            self.session.add(model)
        self._fill_model(model, task)
        self.session.commit()
        return task

    def get_by_id(self, task_id: UUID) -> Task | None:
        model = self.session.get(TaskModel, task_id)
        return self._to_entity(model) if model else None

    def list_by_user(
        self,
        user_id: UUID,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Task]:
        query = self.session.query(TaskModel).filter(TaskModel.user_id == user_id)
        if status is not None:
            query = query.filter(TaskModel.status == status.value)
        if priority is not None:
            query = query.filter(TaskModel.priority == priority.value)
        models = query.order_by(TaskModel.created_at).offset(offset).limit(limit).all()
        return [self._to_entity(model) for model in models]

    def delete(self, task_id: UUID) -> None:
        model = self.session.get(TaskModel, task_id)
        if model is not None:
            self.session.delete(model)
            self.session.commit()

    @staticmethod
    def _fill_model(model: TaskModel, task: Task) -> None:
        model.user_id = task.user_id
        model.title = task.title
        model.description = task.description
        model.status = task.status.value
        model.priority = task.priority.value
        model.due_date = task.due_date
        model.created_at = task.created_at
        model.updated_at = task.updated_at

    @staticmethod
    def _to_entity(model: TaskModel) -> Task:
        return Task(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            description=model.description,
            status=TaskStatus(model.status),
            priority=TaskPriority(model.priority),
            due_date=model.due_date,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
