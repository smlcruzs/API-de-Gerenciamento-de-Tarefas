from uuid import uuid4

import pytest

from task_manager.application.use_cases.create_task import CreateTask
from task_manager.application.use_cases.update_task import UpdateTask
from task_manager.domain.entities.task import TaskPriority, TaskStatus
from task_manager.domain.exceptions import TaskNotFoundError
from tests.fakes.in_memory_task_repository import InMemoryTaskRepository


def test_updates_task_fields():
    repository = InMemoryTaskRepository()
    user_id = uuid4()
    task = CreateTask(repository).execute(user_id=user_id, title="Old title")
    update_task = UpdateTask(repository)

    updated = update_task.execute(
        task_id=task.id,
        user_id=user_id,
        title="New title",
        priority=TaskPriority.HIGH,
    )

    assert updated.title == "New title"
    assert updated.priority == TaskPriority.HIGH


def test_updates_task_status():
    repository = InMemoryTaskRepository()
    user_id = uuid4()
    task = CreateTask(repository).execute(user_id=user_id, title="Task")
    update_task = UpdateTask(repository)

    updated = update_task.execute(
        task_id=task.id, user_id=user_id, status=TaskStatus.DONE
    )

    assert updated.status == TaskStatus.DONE


def test_raises_when_task_does_not_exist():
    repository = InMemoryTaskRepository()
    update_task = UpdateTask(repository)

    with pytest.raises(TaskNotFoundError):
        update_task.execute(task_id=uuid4(), user_id=uuid4(), title="X")


def test_raises_when_task_belongs_to_another_user():
    repository = InMemoryTaskRepository()
    owner_id = uuid4()
    task = CreateTask(repository).execute(user_id=owner_id, title="Task")
    update_task = UpdateTask(repository)

    with pytest.raises(TaskNotFoundError):
        update_task.execute(task_id=task.id, user_id=uuid4(), title="Hijacked")
