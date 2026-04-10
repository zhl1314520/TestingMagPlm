from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class TestCaseResponse(BaseModel):
    id: int
    project_id: int
    project_name: str = ""
    module: str
    title: str
    steps: str
    expected: str
    status: str
    priority: str
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TestCaseCreate(BaseModel):
    project_id: int
    module: str = Field(..., max_length=100)
    title: str = Field(..., max_length=255)
    steps: str
    expected: str
    status: str = Field("有效", max_length=20)
    priority: str = Field("p3", max_length=20)


class TestCaseUpdate(BaseModel):
    module: str | None = None
    title: str | None = None
    steps: str | None = None
    expected: str | None = None
    status: str | None = None
    priority: str | None = None


class TestCasePageResponse(BaseModel):
    total: int
    items: List[TestCaseResponse]
