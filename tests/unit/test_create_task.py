from uuid import uuid4

from task_manager.application.use_cases.create_task import CreateTask
from task_manager.domain.entities.task import TaskPriority, TaskStatus
from tests.fakes.in_memory_task_repository import InMemoryTaskRepository


def test_creates_task_with_todo_status_by_default():
    repository = InMemoryTaskRepository()
    use_case = CreateTask(repository)
    user_id = uuid4()

    task = use_case.execute(user_id=user_id, title="Buy milk")

    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert repository.get_by_id(task.id) == task


def test_creates_task_with_custom_priority_and_description():
    repository = InMemoryTaskRepository()
    use_case = CreateTask(repository)
    user_id = uuid4()

    task = use_case.execute(
        user_id=user_id,
        title="Ship release",
        description="Cut v1.0",
        priority=TaskPriority.HIGH,
    )

    assert task.description == "Cut v1.0"
    assert task.priority == TaskPriority.HIGH
