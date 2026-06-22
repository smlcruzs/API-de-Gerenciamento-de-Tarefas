import pytest

from task_manager.application.use_cases.register_user import RegisterUser
from task_manager.domain.exceptions import UserAlreadyExistsError
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.in_memory_user_repository import InMemoryUserRepository


def test_registers_user_with_hashed_password():
    repository = InMemoryUserRepository()
    register_user = RegisterUser(repository, FakePasswordHasher())

    user = register_user.execute(
        email="jane@example.com", password="s3cret", name="Jane Doe"
    )

    assert user.email == "jane@example.com"
    assert user.hashed_password == "hashed:s3cret"
    assert repository.get_by_email("jane@example.com") == user


def test_raises_when_email_already_registered():
    repository = InMemoryUserRepository()
    register_user = RegisterUser(repository, FakePasswordHasher())
    register_user.execute(email="jane@example.com", password="s3cret", name="Jane")

    with pytest.raises(UserAlreadyExistsError):
        register_user.execute(
            email="jane@example.com", password="other", name="Jane 2"
        )
