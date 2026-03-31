from typing import List
from pydantic import BaseModel, Field


class ExecutionResponse(BaseModel):
    id: int
    project_id: int
    type: str
    status: str
    result: str | None
    created_at: str

    class Config:
        from_attributes = True


class ExecutionCreate(BaseModel):
    project_id: int
    type: str = Field(..., max_length=20)
    env: str = Field(..., max_length=50)


class ExecutionPageResponse(BaseModel):
    total: int
    items: List[ExecutionResponse]
