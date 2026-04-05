from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from schemas.execution import ExecutionCreate, ExecutionUpdate, ExecutionResponse, ExecutionPageResponse
from services import execution as service

router = APIRouter(
    prefix="/executions",
    tags=["测试执行"]
)


@router.post("", response_model=ExecutionResponse)
async def create_execution(
    execution_info: ExecutionCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_execution(execution_info, db)


@router.get("", response_model=ExecutionPageResponse)
async def get_execution_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    project_id: int = Query(None),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_execution_list(page, page_size, project_id, db)


@router.get("/{id}", response_model=ExecutionResponse)
async def get_execution_detail(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_execution_detail(id, db)


@router.put("/{id}", response_model=ExecutionResponse)
async def update_execution(
    id: int,
    execution_info: ExecutionUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await service.update_execution(id, execution_info, db)


@router.post("/{id}/run", response_model=ExecutionResponse)
async def run_execution(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.run_execution(id, db)


@router.delete("/{id}")
async def delete_execution(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_execution(id, db)
