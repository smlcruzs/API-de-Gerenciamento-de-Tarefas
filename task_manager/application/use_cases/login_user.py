from __future__ import annotations

from task_manager.domain.exceptions import InvalidCredentialsError
from task_manager.domain.interfaces.password_hasher import PasswordHasher
from task_manager.domain.interfaces.token_service import TokenService
from task_manager.domain.interfaces.user_repository import UserRepository


class LoginUser:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self.repository = repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    def execute(self, email: str, password: str) -> str:
        user = self.repository.get_by_email(email)
        if user is None or not self.password_hasher.verify(
            password, user.hashed_password
        ):
            raise InvalidCredentialsError()
        if not user.is_active:
            raise InvalidCredentialsError()

        return self.token_service.generate(user.id)
