from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class ExecutionResponse(BaseModel):
    id: int
    project_id: int
    project_name: str | None = None
    name: str
    type: str
    status: str
    result: str
    total_cases: int | None
    passed_cases: int | None
    failed_cases: int | None
    pass_rate: float | None
    executed_by: int | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class ExecutionCreate(BaseModel):
    project_id: int
    name: str = Field(..., max_length=200)
    type: str = Field(default="手动执行", max_length=20)
    status: str = Field(default="等待中", max_length=20)
    result: str = Field(..., max_length=2000)


class ExecutionUpdate(BaseModel):
    name: str | None = Field(None, max_length=200)
    type: str | None = Field(None, max_length=20)
    status: str | None = Field(None, max_length=20)
    result: str | None = Field(None, max_length=2000)


class ExecutionPageResponse(BaseModel):
    total: int
    items: List[ExecutionResponse]
