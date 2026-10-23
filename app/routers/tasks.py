from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from app.database import SessionDep
from app.models import Task, TaskStatus
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_or_404(session: SessionDep, task_id: int) -> Task:
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    return task


@router.get("", response_model=list[TaskRead])
def list_tasks(
    session: SessionDep,
    status_filter: Annotated[TaskStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Task]:
    query = select(Task).order_by(Task.id).limit(limit).offset(offset)
    if status_filter is not None:
        query = query.where(Task.status == status_filter)
    return list(session.scalars(query))


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, session: SessionDep) -> Task:
    task = Task(**payload.model_dump())
    session.add(task)
    session.commit()
    return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: SessionDep) -> Task:
    return get_task_or_404(session, task_id)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, session: SessionDep) -> Task:
    task = get_task_or_404(session, task_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    session.commit()
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: SessionDep) -> None:
    session.delete(get_task_or_404(session, task_id))
    session.commit()
