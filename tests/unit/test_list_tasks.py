from uuid import uuid4

from task_manager.application.use_cases.create_task import CreateTask
from task_manager.application.use_cases.list_tasks import ListTasks
from task_manager.domain.entities.task import TaskPriority, TaskStatus
from tests.fakes.in_memory_task_repository import InMemoryTaskRepository


def test_lists_only_tasks_belonging_to_user():
    repository = InMemoryTaskRepository()
    create_task = CreateTask(repository)
    list_tasks = ListTasks(repository)
    user_id = uuid4()
    other_user_id = uuid4()

    create_task.execute(user_id=user_id, title="Mine")
    create_task.execute(user_id=other_user_id, title="Not mine")

    tasks = list_tasks.execute(user_id=user_id)

    assert len(tasks) == 1
    assert tasks[0].title == "Mine"


def test_filters_by_status_and_priority():
    repository = InMemoryTaskRepository()
    create_task = CreateTask(repository)
    list_tasks = ListTasks(repository)
    user_id = uuid4()

    create_task.execute(user_id=user_id, title="Low one", priority=TaskPriority.LOW)
    high_task = create_task.execute(
        user_id=user_id, title="High one", priority=TaskPriority.HIGH
    )

    tasks = list_tasks.execute(
        user_id=user_id, status=TaskStatus.TODO, priority=TaskPriority.HIGH
    )

    assert [t.id for t in tasks] == [high_task.id]


def test_paginates_results():
    repository = InMemoryTaskRepository()
    create_task = CreateTask(repository)
    list_tasks = ListTasks(repository)
    user_id = uuid4()

    for i in range(5):
        create_task.execute(user_id=user_id, title=f"Task {i}")

    tasks = list_tasks.execute(user_id=user_id, limit=2, offset=2)

    assert len(tasks) == 2
    assert tasks[0].title == "Task 2"
