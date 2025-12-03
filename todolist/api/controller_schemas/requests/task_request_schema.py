from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreateRequest(BaseModel):
    """
    Data to create a task inside a project.
    """
    name: str = Field(..., min_length=1, max_length=100)
    desc: Optional[str] = Field(default=None, max_length=5000)
    status: Optional[str] = Field(default="todo")
    deadline: Optional[datetime] = None


class TaskUpdateRequest(BaseModel):
    """
    Data to update a task.
    """
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    desc: Optional[str] = Field(default=None, max_length=5000)
    status: Optional[str] = None
    deadline: Optional[datetime] = None
