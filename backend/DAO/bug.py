from sqlalchemy import select, func, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from models.bug import Bug
from models.project import Project
from models.project_member import ProjectMember
from models.user import User
from typing import List


async def get_bug_by_id(bug_id: int, db: AsyncSession):
    Reporter = aliased(User)
    Assignee = aliased(User)
    
    stmt = (
        select(Bug, Project.name, Reporter.username, Assignee.username)
        .join(Project, Bug.project_id == Project.id)
        .outerjoin(Reporter, Bug.reporter_id == Reporter.id)
        .outerjoin(Assignee, Bug.assignee_id == Assignee.id)
        .where(Bug.id == bug_id)
    )
    result = await db.execute(stmt)
    row = result.first()
    if row:
        bug, project_name, reporter_name, assignee_name = row
        return bug, project_name, reporter_name, assignee_name
    return None, None, None, None


async def create_bug(bug: Bug, db: AsyncSession):
    db.add(bug)
    await db.flush()
    return bug


async def get_user_project_ids(db: AsyncSession, user_id: int) -> List[int]:
    stmt = select(ProjectMember.project_id).where(ProjectMember.user_id == user_id)
    result = await db.execute(stmt)
    return [row[0] for row in result.fetchall()]


async def get_bug_list_by_user(
    page: int, 
    page_size: int, 
    user_id: int,
    project_id: int = None, 
    status: str = None, 
    priority: str = None, 
    db: AsyncSession = None
):
    Reporter = aliased(User)
    Assignee = aliased(User)
    
    conditions = [Bug.reporter_id == user_id]
    
    if project_id:
        conditions.append(Bug.project_id == project_id)
    if status:
        conditions.append(Bug.status == status)
    if priority:
        conditions.append(Bug.priority == priority)
    
    count_stmt = select(func.count()).select_from(Bug).where(and_(*conditions))
    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(Bug, Project.name, Reporter.username, Assignee.username)
        .join(Project, Bug.project_id == Project.id)
        .outerjoin(Reporter, Bug.reporter_id == Reporter.id)
        .outerjoin(Assignee, Bug.assignee_id == Assignee.id)
        .where(and_(*conditions))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Bug.id.desc())
    )
    
    result = await db.execute(stmt)
    rows = result.all()
    items = []
    for row in rows:
        bug, project_name, reporter_name, assignee_name = row
        items.append((bug, project_name, reporter_name, assignee_name))

    return total, items


async def get_bug_list(page: int, page_size: int, project_id: int = None, status: str = None, priority: str = None, db: AsyncSession = None):
    Reporter = aliased(User)
    Assignee = aliased(User)
    
    count_stmt = select(func.count()).select_from(Bug)
    
    conditions = []
    if project_id:
        conditions.append(Bug.project_id == project_id)
    if status:
        conditions.append(Bug.status == status)
    if priority:
        conditions.append(Bug.priority == priority)
    
    if conditions:
        count_stmt = count_stmt.where(and_(*conditions))
    
    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(Bug, Project.name, Reporter.username, Assignee.username)
        .join(Project, Bug.project_id == Project.id)
        .outerjoin(Reporter, Bug.reporter_id == Reporter.id)
        .outerjoin(Assignee, Bug.assignee_id == Assignee.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Bug.id.desc())
    )
    
    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    result = await db.execute(stmt)
    rows = result.all()
    items = []
    for row in rows:
        bug, project_name, reporter_name, assignee_name = row
        items.append((bug, project_name, reporter_name, assignee_name))

    return total, items


async def delete_bug(bug_id: int, db: AsyncSession):
    stmt = delete(Bug).where(Bug.id == bug_id)
    await db.execute(stmt)


async def update_bug(bug: Bug, db: AsyncSession):
    await db.flush()
    return bug


async def is_user_in_project(db: AsyncSession, user_id: int, project_id: int) -> bool:
    stmt = select(ProjectMember).where(
        ProjectMember.user_id == user_id,
        ProjectMember.project_id == project_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None
