from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from task_manager.domain.entities.user import User
from task_manager.domain.interfaces.user_repository import UserRepository
from task_manager.infrastructure.models import UserModel


class SQLUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, user: User) -> User:
        model = self.session.get(UserModel, user.id)
        if model is None:
            model = UserModel(id=user.id)
            self.session.add(model)
        model.email = user.email
        model.hashed_password = user.hashed_password
        model.name = user.name
        model.is_active = user.is_active
        model.created_at = user.created_at
        self.session.commit()
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        model = self.session.get(UserModel, user_id)
        return self._to_entity(model) if model else None

    def get_by_email(self, email: str) -> User | None:
        model = self.session.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            name=model.name,
            created_at=model.created_at,
            is_active=model.is_active,
        )
