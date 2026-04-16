from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class ExecutionResponse(BaseModel):
    id: int
    project_id: int
    project_name: str
    name: str
    type: str
    status: str
    result: str
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float
    executed_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExecutionCreate(BaseModel):
    project_id: int
    name: str = Field(..., max_length=200)
    type: str = Field(default="手动执行", max_length=20)
    status: str = Field(default="等待中", max_length=20)
    result: str = Field(..., max_length=2000)


class ExecutionUpdate(BaseModel):
    # 可以不更新
    name: str | None = Field(None, max_length=200)
    type: str | None = Field(None, max_length=20)
    status: str | None = Field(None, max_length=20)
    result: str | None = Field(None, max_length=2000)


class ExecutionPageResponse(BaseModel):
    total: int
    items: List[ExecutionResponse]
