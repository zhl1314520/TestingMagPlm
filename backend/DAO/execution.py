from sqlalchemy import select, func, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.execution import Execution
from models.project import Project


async def get_execution_by_id(execution_id: int, db: AsyncSession):
    stmt = (
        select(Execution, Project.name)
        .join(Project, Execution.project_id == Project.id)
        .where(Execution.id == execution_id)
    )
    result = await db.execute(stmt)
    row = result.first()
    if row:
        execution, project_name = row
        return execution, project_name
    return None, None


async def create_execution(execution: Execution, db: AsyncSession):
    db.add(execution)
    await db.flush()
    return execution


async def get_execution_list(page: int, db: AsyncSession,
                             page_size: int, project_id: int = None, executed_by: int = None):
    # select(字段) ：直接查询，SQLAlchemy 自动推断 FROM 哪个表
    # select(字段).select_from(表) ：明确指定 FROM 哪个表，适用于聚合函数和复杂查询
    count_stmt = select(func.count()).select_from(Execution)
    
    conditions = []
    if project_id:
        conditions.append(Execution.project_id == project_id)
    if executed_by:
        conditions.append(Execution.executed_by == executed_by)
    
    if conditions:
        count_stmt = count_stmt.where(and_(*conditions))
    
    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(Execution, Project.name)
        .join(Project, Execution.project_id == Project.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Execution.id.desc())
    )
    
    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    result = await db.execute(stmt)
    rows = result.all()
    items = []
    for row in rows:
        execution, project_name = row
        items.append((execution, project_name))

    return total, items


async def delete_execution(execution_id: int, db: AsyncSession):
    stmt = delete(Execution).where(Execution.id == execution_id)
    await db.execute(stmt)
