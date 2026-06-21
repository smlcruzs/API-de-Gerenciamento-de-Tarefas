import pytest

from task_manager.domain.interfaces.task_repository import TaskRepository
from task_manager.domain.interfaces.user_repository import UserRepository


def test_cannot_instantiate_task_repository_directly():
    with pytest.raises(TypeError):
        TaskRepository()


def test_cannot_instantiate_user_repository_directly():
    with pytest.raises(TypeError):
        UserRepository()


def test_partial_task_repository_implementation_is_still_abstract():
    class PartialTaskRepository(TaskRepository):
        def save(self, task):
            return task

    with pytest.raises(TypeError):
        PartialTaskRepository()
