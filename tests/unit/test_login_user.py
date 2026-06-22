import pytest

from task_manager.application.use_cases.login_user import LoginUser
from task_manager.application.use_cases.register_user import RegisterUser
from task_manager.domain.exceptions import InvalidCredentialsError
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.fake_token_service import FakeTokenService
from tests.fakes.in_memory_user_repository import InMemoryUserRepository


def _register(repository, password_hasher):
    return RegisterUser(repository, password_hasher).execute(
        email="jane@example.com", password="s3cret", name="Jane Doe"
    )


def test_logs_in_with_valid_credentials_and_returns_token():
    repository = InMemoryUserRepository()
    password_hasher = FakePasswordHasher()
    user = _register(repository, password_hasher)
    login_user = LoginUser(repository, password_hasher, FakeTokenService())

    token = login_user.execute(email="jane@example.com", password="s3cret")

    assert token == f"token-for-{user.id}"


def test_raises_when_password_is_wrong():
    repository = InMemoryUserRepository()
    password_hasher = FakePasswordHasher()
    _register(repository, password_hasher)
    login_user = LoginUser(repository, password_hasher, FakeTokenService())

    with pytest.raises(InvalidCredentialsError):
        login_user.execute(email="jane@example.com", password="wrong")


def test_raises_when_email_does_not_exist():
    repository = InMemoryUserRepository()
    password_hasher = FakePasswordHasher()
    login_user = LoginUser(repository, password_hasher, FakeTokenService())

    with pytest.raises(InvalidCredentialsError):
        login_user.execute(email="ghost@example.com", password="s3cret")


def test_raises_when_user_is_inactive():
    repository = InMemoryUserRepository()
    password_hasher = FakePasswordHasher()
    user = _register(repository, password_hasher)
    user.deactivate()
    repository.save(user)
    login_user = LoginUser(repository, password_hasher, FakeTokenService())

    with pytest.raises(InvalidCredentialsError):
        login_user.execute(email="jane@example.com", password="s3cret")
