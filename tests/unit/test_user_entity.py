from datetime import datetime
from uuid import uuid4

import pytest

from task_manager.domain.entities.user import User


def make_user(**overrides):
    defaults = dict(
        id=uuid4(),
        email="user@example.com",
        hashed_password="hashed",
        name="Jane Doe",
        created_at=datetime.utcnow(),
    )
    defaults.update(overrides)
    return User(**defaults)


def test_creates_user_with_valid_data():
    user = make_user()

    assert user.is_active is True


def test_rejects_invalid_email():
    with pytest.raises(ValueError):
        make_user(email="not-an-email")


def test_rejects_empty_name():
    with pytest.raises(ValueError):
        make_user(name="  ")


def test_deactivate_sets_is_active_false():
    user = make_user()

    user.deactivate()

    assert user.is_active is False
