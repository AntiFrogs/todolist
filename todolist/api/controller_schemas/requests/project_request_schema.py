from pydantic import BaseModel, Field
from typing import Optional


class ProjectCreateRequest(BaseModel):
    """
    Data the client must send to create a project.
    """
    name: str = Field(..., min_length=1, max_length=100)
    desc: Optional[str] = Field(default=None, max_length=5000)


class ProjectUpdateRequest(BaseModel):
    """
    Data the client can send to update a project.
    """
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    desc: Optional[str] = Field(default=None, max_length=5000)