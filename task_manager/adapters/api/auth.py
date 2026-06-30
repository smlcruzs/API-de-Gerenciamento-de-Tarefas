from __future__ import annotations

from fastapi import APIRouter, Depends, status

from task_manager.adapters.api.dependencies import (
    get_login_user_use_case,
    get_register_user_use_case,
)
from task_manager.adapters.schemas.user_schema import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from task_manager.application.use_cases.login_user import LoginUser
from task_manager.application.use_cases.register_user import RegisterUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(
    payload: RegisterRequest,
    use_case: RegisterUser = Depends(get_register_user_use_case),
) -> UserResponse:
    user = use_case.execute(
        email=payload.email, password=payload.password, name=payload.name
    )
    return UserResponse.from_entity(user)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    use_case: LoginUser = Depends(get_login_user_use_case),
) -> TokenResponse:
    token = use_case.execute(email=payload.email, password=payload.password)
    return TokenResponse(access_token=token)
