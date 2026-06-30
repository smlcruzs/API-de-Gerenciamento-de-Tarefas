from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from task_manager.adapters.api import auth, tasks
from task_manager.domain.exceptions import (
    InvalidCredentialsError,
    TaskNotFoundError,
    UserAlreadyExistsError,
)
from task_manager.infrastructure.database import engine
from task_manager.infrastructure.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Task Manager API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.exception_handler(TaskNotFoundError)
async def handle_task_not_found(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(UserAlreadyExistsError)
async def handle_user_already_exists(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(InvalidCredentialsError)
async def handle_invalid_credentials(
    request: Request, exc: InvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc)})
