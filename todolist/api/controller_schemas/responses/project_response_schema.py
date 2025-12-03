from pydantic import BaseModel
from typing import Optional


class ProjectResponse(BaseModel):
    """
    Shape of a Project returned by the API.
    """
    id: str
    name: str
    desc: Optional[str] = None

    class Config:
        from_attributes = True
