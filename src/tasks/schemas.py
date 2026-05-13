from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Task_create(BaseModel):
    title: str
    description: str
    is_completed: bool


class Task_response(Task_create):
    id:int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TaskFilterParams(BaseModel):
    title: str | None = None
    completed: bool | None = None
    priority: int | None = None