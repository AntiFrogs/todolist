from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskResponse(BaseModel):
    """
    Shape of a Task returned by the API.
    """
    id: str
    for_project: str
    name: str
    desc: Optional[str] = None
    status: str
    deadline: Optional[datetime] = None
    at_closed: Optional[datetime] = None

    class Config:
        from_attributes = True
