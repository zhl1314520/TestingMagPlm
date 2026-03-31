from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.execution import Execution


async def get_execution_by_id(execution_id: int, db: AsyncSession):
    stmt = select(Execution).where(Execution.id == execution_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_execution(execution: Execution, db: AsyncSession):
    db.add(execution)
    await db.flush()
    return execution


async def get_execution_list(page: int, page_size: int, project_id: int = None, db: AsyncSession = None):
    count_stmt = select(func.count()).select_from(Execution)
    
    if project_id:
        count_stmt = count_stmt.where(Execution.project_id == project_id)
    
    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(Execution)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Execution.id.desc())
    )
    
    if project_id:
        stmt = stmt.where(Execution.project_id == project_id)
    
    result = await db.execute(stmt)
    items = result.scalars().all()

    return total, items


async def delete_execution(execution_id: int, db: AsyncSession):
    stmt = delete(Execution).where(Execution.id == execution_id)
    await db.execute(stmt)
