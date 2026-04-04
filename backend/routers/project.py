from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from core.security import get_current_user
from schemas.project import ProjectCreate, ProjectUpdate, ProjectMemberCreate, ProjectResponse, ProjectPageResponse, ProjectMemberResponse
from services import project as service

router = APIRouter(
    prefix="/projects",
    tags=["项目管理"]
)


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_info: ProjectCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user["user_id"]
    return await service.create_project(project_info, db, user_id)


@router.get("", response_model=ProjectPageResponse)
async def get_project_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user["user_id"]
    return await service.get_project_list(page, page_size, user_id, db)


@router.delete("/{id}")
async def delete_project(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_project(id, db)


@router.post("/{id}/members", response_model=ProjectMemberResponse)
async def add_project_member(
    id: int,
    member_info: ProjectMemberCreate,
    db: AsyncSession = Depends(get_db)
):
    member_info.project_id = id
    return await service.add_project_member(member_info, db)


@router.get("/{id}/members")
async def get_project_members(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_project_members(id, db)


@router.delete("/members/{member_id}")
async def remove_project_member(
    member_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.remove_project_member(member_id, db)
