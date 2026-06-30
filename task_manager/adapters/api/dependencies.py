from __future__ import annotations

import os
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from task_manager.application.use_cases.create_task import CreateTask
from task_manager.application.use_cases.delete_task import DeleteTask
from task_manager.application.use_cases.get_task import GetTask
from task_manager.application.use_cases.list_tasks import ListTasks
from task_manager.application.use_cases.login_user import LoginUser
from task_manager.application.use_cases.register_user import RegisterUser
from task_manager.application.use_cases.update_task import UpdateTask
from task_manager.domain.interfaces.password_hasher import PasswordHasher
from task_manager.domain.interfaces.task_repository import TaskRepository
from task_manager.domain.interfaces.token_service import TokenService
from task_manager.domain.interfaces.user_repository import UserRepository
from task_manager.infrastructure.database import get_db
from task_manager.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from task_manager.infrastructure.security.jwt_token_service import JWTTokenService
from task_manager.infrastructure.sql_task_repository import SQLTaskRepository
from task_manager.infrastructure.sql_user_repository import SQLUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return SQLTaskRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SQLUserRepository(db)


def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


def get_token_service() -> TokenService:
    return JWTTokenService(
        secret_key=os.environ.get("JWT_SECRET_KEY", "change-me"),
        algorithm=os.environ.get("JWT_ALGORITHM", "HS256"),
        expire_minutes=int(os.environ.get("JWT_EXPIRE_MINUTES", "60")),
    )


def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    token_service: TokenService = Depends(get_token_service),
) -> UUID:
    try:
        return token_service.decode(token)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


def get_create_task_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> CreateTask:
    return CreateTask(repository)


def get_list_tasks_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> ListTasks:
    return ListTasks(repository)


def get_get_task_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> GetTask:
    return GetTask(repository)


def get_update_task_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> UpdateTask:
    return UpdateTask(repository)


def get_delete_task_use_case(
    repository: TaskRepository = Depends(get_task_repository),
) -> DeleteTask:
    return DeleteTask(repository)


def get_register_user_use_case(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> RegisterUser:
    return RegisterUser(repository, password_hasher)


def get_login_user_use_case(
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: TokenService = Depends(get_token_service),
) -> LoginUser:
    return LoginUser(repository, password_hasher, token_service)
