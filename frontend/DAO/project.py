from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.project import Project
from models.project_member import ProjectMember


async def get_project_by_name(name: str, db: AsyncSession):
    stmt = select(Project).where(Project.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_project_by_id(project_id: int, db: AsyncSession):
    stmt = select(Project).where(Project.id == project_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_project(project: Project, db: AsyncSession):
    db.add(project)
    await db.flush()
    return project


async def get_project_list(page: int, page_size: int, db: AsyncSession):
    count_stmt = select(func.count()).select_from(Project)
    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(Project)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Project.id.desc())
    )
    result = await db.execute(stmt)
    items = result.scalars().all()

    return total, items


async def delete_project(project_id: int, db: AsyncSession):
    stmt = delete(Project).where(Project.id == project_id)
    await db.execute(stmt)


async def create_project_member(member: ProjectMember, db: AsyncSession):
    db.add(member)
    await db.flush()
    return member


async def get_project_members(project_id: int, db: AsyncSession):
    stmt = select(ProjectMember).where(ProjectMember.project_id == project_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def delete_project_member(member_id: int, db: AsyncSession):
    stmt = delete(ProjectMember).where(ProjectMember.id == member_id)
    await db.execute(stmt)
