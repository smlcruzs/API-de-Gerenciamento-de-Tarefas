from __future__ import annotations

from uuid import UUID

from task_manager.domain.entities.user import User
from task_manager.domain.interfaces.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users: dict[UUID, User] = {}

    def save(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        return self._users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        return next((u for u in self._users.values() if u.email == email), None)
