from sqlalchemy import select, func, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.project import Project
from models.project_member import ProjectMember


async def get_project_by_name(name: str, db: AsyncSession):
    stmt = select(Project).where(Project.name == name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# update
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


async def get_project_list_by_user(page: int, page_size: int, user_id: int, db: AsyncSession):
    # 查出当前用户参与过的所有项目 ID（去重）
    # 权限过滤，确保用户只能看到自己参与的项目
    member_subquery = (
        select(ProjectMember.project_id)
        .where(ProjectMember.user_id == user_id)
        .distinct()
    )       # -> SELECT DISTINCT project_id FROM project_member WHERE user_id = ?;
    
    count_stmt = (
        select(func.count()).select_from(Project)   # 我要查询一个数字（SELECT count(*)），这个数字是从 Project 表算出来的 (select_from 理解为 “定位器”)
        .where(
            or_(
                Project.owner_id == user_id,        # 查询用户自己创建的项目
                Project.id.in_(member_subquery)     # 查询用户作为成员的项目
            )
        )
    )       # -> SELECT count(*) FROM project WHERE project.owner_id = user_id
            #    OR project.id IN (SELECT project_id FROM project_members WHERE user_id = user_id);
    # -> 查询出的count总和为“用户自己创建的项目” + “包含用户的项目“（去重后）

    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(Project)
        .where(
            or_(
                Project.owner_id == user_id,
                Project.id.in_(member_subquery)
            )
        )
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


async def update_project(project_id: int, update_data: dict, db: AsyncSession):
    project = await get_project_by_id(project_id, db)
    if not project:
        return None
    for key, value in update_data.items():
        if value is not None:
            setattr(project, key, value)        # 动态设置对象属性
    await db.flush()
    return project


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
