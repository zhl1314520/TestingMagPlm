from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from schemas.project import ProjectCreate, ProjectUpdate, ProjectMemberCreate, ProjectPageResponse
from models.project import Project
from models.project_member import ProjectMember
from DAO import project as crud

logger = logging.getLogger(__name__)


async def create_project(project_data: ProjectCreate, db: AsyncSession):
    logger.info("创建项目请求: name=%s", project_data.name)

    existing = await crud.get_project_by_name(project_data.name, db)
    if existing:
        logger.warning("项目已存在: name=%s", project_data.name)
        raise HTTPException(
            status_code=400,
            detail="PROJECT_ALREADY_EXISTS"
        )

    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=project_data.owner_id
    )

    await crud.create_project(new_project, db)
    await db.commit()
    await db.refresh(new_project)

    logger.info("项目创建成功: id=%s", new_project.id)
    return new_project


async def get_project_list(page: int, page_size: int, db: AsyncSession):
    total, items = await crud.get_project_list(page, page_size, db)
    return ProjectPageResponse(
        total=total,
        items=items
    )


async def delete_project(project_id: int, db: AsyncSession):
    await crud.delete_project(project_id, db)
    await db.commit()
    return {
        "code": 200,
        "message": "删除成功"
    }


async def add_project_member(member_data: ProjectMemberCreate, db: AsyncSession):
    logger.info("添加项目成员: project_id=%s, user_id=%s", member_data.project_id, member_data.user_id)

    project = await crud.get_project_by_id(member_data.project_id, db)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="PROJECT_NOT_FOUND"
        )

    new_member = ProjectMember(
        project_id=member_data.project_id,
        user_id=member_data.user_id,
        role=member_data.role
    )

    await crud.create_project_member(new_member, db)
    await db.commit()
    await db.refresh(new_member)

    return new_member


async def get_project_members(project_id: int, db: AsyncSession):
    members = await crud.get_project_members(project_id, db)
    return members


async def remove_project_member(member_id: int, db: AsyncSession):
    await crud.delete_project_member(member_id, db)
    await db.commit()
    return {
        "code": 200,
        "message": "删除成功"
    }
