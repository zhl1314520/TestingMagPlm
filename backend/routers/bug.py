from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from core.security import get_current_user
from schemas.bug import BugCreate, BugUpdate, BugResponse, BugPageResponse
from services import bug as service
from DAO import bug as crud

router = APIRouter(
    prefix="/bugs",
    tags=["缺陷管理"]
)


@router.post("", response_model=BugResponse)
async def create_bug(
    bug_info: BugCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.create_bug(bug_info, current_user["user_id"], db)


@router.get("", response_model=BugPageResponse)
async def get_bug_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    project_id: int = Query(None),
    status: str = Query(None),
    priority: str = Query(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_bug_list_by_user(
        page, page_size, current_user["user_id"], project_id, status, priority, db
    )


@router.get("/{id}", response_model=BugResponse)
async def get_bug(
    id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    bug, project_name = await crud.get_bug_by_id(id, db)
    if not bug:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="BUG_NOT_FOUND")
    
    bug_dict = {
        "id": bug.id,
        "project_id": bug.project_id,
        "project_name": project_name,
        "testcase_id": bug.testcase_id,
        "title": bug.title,
        "description": bug.description,
        "status": bug.status,
        "priority": bug.priority,
        "reporter_id": bug.reporter_id,
        "assignee_id": bug.assignee_id,
        "created_at": bug.created_at,
        "updated_at": bug.updated_at
    }
    
    return bug_dict


@router.put("/{id}", response_model=BugResponse)
async def update_bug(
    id: int,
    bug_info: BugUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.update_bug(id, bug_info, db)


@router.put("/{id}/status", response_model=BugResponse)
async def update_bug_status(
    id: int,
    status: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.update_bug_status(id, status, db)


@router.delete("/{id}")
async def delete_bug(
    id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_bug(id, db)
