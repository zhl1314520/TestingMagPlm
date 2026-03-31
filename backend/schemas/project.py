from typing import List
from pydantic import BaseModel, Field


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: str

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None
    owner_id: int


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
