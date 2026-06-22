from datetime import datetime
from uuid import uuid4

from task_manager.domain.entities.task import Task, TaskPriority, TaskStatus
from task_manager.infrastructure.sql_task_repository import SQLTaskRepository


def make_task(**overrides):
    now = datetime.utcnow()
    defaults = dict(
        id=uuid4(),
        user_id=uuid4(),
        title="Task",
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        created_at=now,
        updated_at=now,
    )
    defaults.update(overrides)
    return Task(**defaults)


def test_saves_and_retrieves_task(db_session):
    repository = SQLTaskRepository(db_session)
    task = make_task()

    repository.save(task)
    retrieved = repository.get_by_id(task.id)

    assert retrieved.id == task.id
    assert retrieved.title == task.title
    assert retrieved.status == TaskStatus.TODO


def test_updates_existing_task(db_session):
    repository = SQLTaskRepository(db_session)
    task = make_task()
    repository.save(task)

    task.update_status(TaskStatus.DONE)
    repository.save(task)

    retrieved = repository.get_by_id(task.id)
    assert retrieved.status == TaskStatus.DONE


def test_list_by_user_filters_by_priority_and_excludes_other_users(db_session):
    repository = SQLTaskRepository(db_session)
    user_id = uuid4()
    low = make_task(user_id=user_id, priority=TaskPriority.LOW)
    high = make_task(user_id=user_id, priority=TaskPriority.HIGH)
    other_user_task = make_task()
    for task in (low, high, other_user_task):
        repository.save(task)

    results = repository.list_by_user(user_id, priority=TaskPriority.HIGH)

    assert [t.id for t in results] == [high.id]


def test_delete_removes_task(db_session):
    repository = SQLTaskRepository(db_session)
    task = make_task()
    repository.save(task)

    repository.delete(task.id)

    assert repository.get_by_id(task.id) is None
