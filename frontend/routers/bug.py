from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from schemas.bug import BugCreate, BugUpdate, BugResponse, BugPageResponse
from services import bug as service

router = APIRouter(
    prefix="/bugs",
    tags=["缺陷管理"]
)


@router.post("", response_model=BugResponse)
async def create_bug(
    bug_info: BugCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_bug(bug_info, db)


@router.get("", response_model=BugPageResponse)
async def get_bug_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    project_id: int = Query(None),
    status: str = Query(None),
    priority: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_bug_list(page, page_size, project_id, status, priority, db)


@router.get("/{id}", response_model=BugResponse)
async def get_bug(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    from DAO import bug as crud
    bug = await crud.get_bug_by_id(id, db)
    if not bug:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="BUG_NOT_FOUND")
    return bug


@router.put("/{id}", response_model=BugResponse)
async def update_bug(
    id: int,
    bug_info: BugUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await service.update_bug(id, bug_info, db)


@router.put("/{id}/status", response_model=BugResponse)
async def update_bug_status(
    id: int,
    status: str,
    db: AsyncSession = Depends(get_db)
):
    return await service.update_bug_status(id, status, db)


@router.delete("/{id}")
async def delete_bug(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_bug(id, db)
