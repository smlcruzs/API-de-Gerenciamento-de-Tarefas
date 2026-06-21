from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from task_manager.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        ...

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        ...
