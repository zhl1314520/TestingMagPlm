from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProjectMemberBase(BaseModel):
    project_id: int
    user_id: int
    role: Optional[str] = None


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMemberResponse(ProjectMemberBase):
    id: int
    joined_at: datetime

    class Config:
        from_attributes = True
