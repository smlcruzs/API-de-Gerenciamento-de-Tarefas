from datetime import datetime
from uuid import uuid4

import pytest

from task_manager.domain.entities.task import Task, TaskPriority, TaskStatus


def make_task(**overrides):
    defaults = dict(
        id=uuid4(),
        user_id=uuid4(),
        title="Write report",
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    defaults.update(overrides)
    return Task(**defaults)


def test_creates_task_with_valid_data():
    task = make_task()

    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM


def test_rejects_empty_title():
    with pytest.raises(ValueError):
        make_task(title="   ")


def test_rejects_title_longer_than_200_chars():
    with pytest.raises(ValueError):
        make_task(title="x" * 201)


def test_update_status_changes_status_and_updated_at():
    task = make_task()
    previous_updated_at = task.updated_at

    task.update_status(TaskStatus.DONE)

    assert task.status == TaskStatus.DONE
    assert task.updated_at >= previous_updated_at
