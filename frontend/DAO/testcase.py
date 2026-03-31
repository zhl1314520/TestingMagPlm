from sqlalchemy import select, func, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.testcase import TestCase


async def get_testcase_by_id(testcase_id: int, db: AsyncSession):
    stmt = select(TestCase).where(TestCase.id == testcase_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_testcase(testcase: TestCase, db: AsyncSession):
    db.add(testcase)
    await db.flush()
    return testcase


async def get_testcase_list(page: int, page_size: int, project_id: int = None, module: str = None, status: str = None, db: AsyncSession = None):
    count_stmt = select(func.count()).select_from(TestCase)
    
    conditions = []
    if project_id:
        conditions.append(TestCase.project_id == project_id)
    if module:
        conditions.append(TestCase.module == module)
    if status:
        conditions.append(TestCase.status == status)
    
    if conditions:
        count_stmt = count_stmt.where(and_(*conditions))
    
    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(TestCase)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(TestCase.id.desc())
    )
    
    if conditions:
        stmt = stmt.where(and_(*conditions))
    
    result = await db.execute(stmt)
    items = result.scalars().all()

    return total, items


async def delete_testcase(testcase_id: int, db: AsyncSession):
    stmt = delete(TestCase).where(TestCase.id == testcase_id)
    await db.execute(stmt)


async def update_testcase(testcase: TestCase, db: AsyncSession):
    await db.flush()
    return testcase
