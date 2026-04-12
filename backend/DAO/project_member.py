from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.project_member import ProjectMember
from schemas.project import ProjectMemberCreate
from typing import Optional, List


async def get_project_member(db: AsyncSession, project_id: int, user_id: int) -> Optional[ProjectMember]:
    """获取项目成员"""
    result = await db.execute(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def get_project_members_by_project(db: AsyncSession, project_id: int) -> List[ProjectMember]:
    """根据项目 ID 获取成员列表"""
    result = await db.execute(
        select(ProjectMember).where(ProjectMember.project_id == project_id)
    )
    return result.scalars().all()


async def get_projects_by_user(db: AsyncSession, user_id: int) -> List[ProjectMember]:
    """根据用户 ID 获取参与的项目"""
    result = await db.execute(
        select(ProjectMember).where(ProjectMember.user_id == user_id)
    )
    return result.scalars().all()


async def add_project_member(db: AsyncSession, member: ProjectMemberCreate) -> ProjectMember:
    """添加项目成员"""
    db_member = ProjectMember(**member.model_dump())
    db.add(db_member)
    await db.commit()
    await db.refresh(db_member)
    return db_member


async def remove_project_member(db: AsyncSession, project_id: int, user_id: int) -> bool:
    """移除项目成员"""
    db_member = await get_project_member(db, project_id, user_id)
    if db_member:
        await db.delete(db_member)
        await db.commit()
        return True
    return False


async def update_project_member_role(
    db: AsyncSession, 
    project_id: int, 
    user_id: int, 
    role: str
) -> Optional[ProjectMember]:
    """更新成员角色"""
    db_member = await get_project_member(db, project_id, user_id)
    if db_member:
        db_member.role = role
        await db.commit()
        await db.refresh(db_member)
    return db_member
