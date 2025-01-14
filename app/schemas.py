from typing import Optional
from pydantic import BaseModel
from enum import Enum


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskInDB(TaskBase):
    id: int

    class Config:
        from_attributes = True
