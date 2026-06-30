from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from task_manager.adapters.api.dependencies import (
    get_create_task_use_case,
    get_current_user_id,
    get_delete_task_use_case,
    get_get_task_use_case,
    get_list_tasks_use_case,
    get_update_task_use_case,
)
from task_manager.adapters.schemas.task_schema import (
    TaskCreateRequest,
    TaskResponse,
    TaskStatusUpdateRequest,
    TaskUpdateRequest,
)
from task_manager.application.use_cases.create_task import CreateTask
from task_manager.application.use_cases.delete_task import DeleteTask
from task_manager.application.use_cases.get_task import GetTask
from task_manager.application.use_cases.list_tasks import ListTasks
from task_manager.application.use_cases.update_task import UpdateTask
from task_manager.domain.entities.task import TaskPriority, TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    status_filter: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    limit: int = 20,
    offset: int = 0,
    user_id: UUID = Depends(get_current_user_id),
    use_case: ListTasks = Depends(get_list_tasks_use_case),
) -> list[TaskResponse]:
    tasks = use_case.execute(
        user_id=user_id,
        status=status_filter,
        priority=priority,
        limit=limit,
        offset=offset,
    )
    return [TaskResponse.from_entity(task) for task in tasks]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: CreateTask = Depends(get_create_task_use_case),
) -> TaskResponse:
    task = use_case.execute(
        user_id=user_id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        due_date=payload.due_date,
    )
    return TaskResponse.from_entity(task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: GetTask = Depends(get_get_task_use_case),
) -> TaskResponse:
    task = use_case.execute(task_id=task_id, user_id=user_id)
    return TaskResponse.from_entity(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: UUID,
    payload: TaskUpdateRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: UpdateTask = Depends(get_update_task_use_case),
) -> TaskResponse:
    task = use_case.execute(
        task_id=task_id,
        user_id=user_id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        due_date=payload.due_date,
    )
    return TaskResponse.from_entity(task)


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: UUID,
    payload: TaskStatusUpdateRequest,
    user_id: UUID = Depends(get_current_user_id),
    use_case: UpdateTask = Depends(get_update_task_use_case),
) -> TaskResponse:
    task = use_case.execute(task_id=task_id, user_id=user_id, status=payload.status)
    return TaskResponse.from_entity(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_task(
    task_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    use_case: DeleteTask = Depends(get_delete_task_use_case),
) -> None:
    use_case.execute(task_id=task_id, user_id=user_id)
