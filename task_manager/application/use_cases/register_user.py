from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from task_manager.domain.entities.user import User
from task_manager.domain.exceptions import UserAlreadyExistsError
from task_manager.domain.interfaces.password_hasher import PasswordHasher
from task_manager.domain.interfaces.user_repository import UserRepository


class RegisterUser:
    def __init__(
        self, repository: UserRepository, password_hasher: PasswordHasher
    ) -> None:
        self.repository = repository
        self.password_hasher = password_hasher

    def execute(self, email: str, password: str, name: str) -> User:
        if self.repository.get_by_email(email) is not None:
            raise UserAlreadyExistsError(email)

        user = User(
            id=uuid4(),
            email=email,
            hashed_password=self.password_hasher.hash(password),
            name=name,
            created_at=datetime.utcnow(),
        )
        return self.repository.save(user)
