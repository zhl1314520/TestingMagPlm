from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str

    class Config:
        from_attributes = True


class ProjectMemberCreate(BaseModel):
    project_id: int
    user_id: int
    role: str


class ProjectPageResponse(BaseModel):
    total: int
    items: List[ProjectResponse]
