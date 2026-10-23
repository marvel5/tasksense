from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import TaskStatus


class TaskCreate(BaseModel):
    """Request body for creating a task (like a Laravel FormRequest)."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    due_date: date | None = None


class TaskUpdate(BaseModel):
    """Partial update: only the fields sent by the client are applied."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus | None = None
    due_date: date | None = None


class TaskRead(BaseModel):
    """Response shape (like a Laravel API Resource)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    due_date: date | None
    created_at: datetime
