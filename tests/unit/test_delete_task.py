from uuid import uuid4

import pytest

from task_manager.application.use_cases.create_task import CreateTask
from task_manager.application.use_cases.delete_task import DeleteTask
from task_manager.domain.exceptions import TaskNotFoundError
from tests.fakes.in_memory_task_repository import InMemoryTaskRepository


def test_deletes_task():
    repository = InMemoryTaskRepository()
    user_id = uuid4()
    task = CreateTask(repository).execute(user_id=user_id, title="Task")
    delete_task = DeleteTask(repository)

    delete_task.execute(task_id=task.id, user_id=user_id)

    assert repository.get_by_id(task.id) is None


def test_raises_when_task_does_not_exist():
    repository = InMemoryTaskRepository()
    delete_task = DeleteTask(repository)

    with pytest.raises(TaskNotFoundError):
        delete_task.execute(task_id=uuid4(), user_id=uuid4())


def test_raises_when_task_belongs_to_another_user():
    repository = InMemoryTaskRepository()
    owner_id = uuid4()
    task = CreateTask(repository).execute(user_id=owner_id, title="Task")
    delete_task = DeleteTask(repository)

    with pytest.raises(TaskNotFoundError):
        delete_task.execute(task_id=task.id, user_id=uuid4())
