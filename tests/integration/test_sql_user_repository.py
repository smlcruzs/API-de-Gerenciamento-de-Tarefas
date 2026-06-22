from datetime import datetime
from uuid import uuid4

from task_manager.domain.entities.user import User
from task_manager.infrastructure.sql_user_repository import SQLUserRepository


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


def test_saves_and_retrieves_user_by_id(db_session):
    repository = SQLUserRepository(db_session)
    user = make_user()

    repository.save(user)
    retrieved = repository.get_by_id(user.id)

    assert retrieved.email == user.email


def test_retrieves_user_by_email(db_session):
    repository = SQLUserRepository(db_session)
    user = make_user(email="jane@example.com")
    repository.save(user)

    retrieved = repository.get_by_email("jane@example.com")

    assert retrieved.id == user.id


def test_get_by_email_returns_none_when_not_found(db_session):
    repository = SQLUserRepository(db_session)

    assert repository.get_by_email("ghost@example.com") is None
