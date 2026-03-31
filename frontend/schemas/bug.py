from typing import List
from pydantic import BaseModel, Field


class BugResponse(BaseModel):
    id: int
    project_id: int
    testcase_id: int | None
    title: str
    description: str
    status: str
    priority: str
    assignee_id: int | None
    created_at: str

    class Config:
        from_attributes = True


class BugCreate(BaseModel):
    project_id: int
    testcase_id: int | None = None
    title: str = Field(..., max_length=255)
    description: str
    status: str = Field("new", max_length=20)
    priority: str = Field("medium", max_length=20)
    assignee_id: int | None = None


class BugUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee_id: int | None = None


class BugPageResponse(BaseModel):
    total: int
    items: List[BugResponse]
