from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User


async def get_user_by_email(email: str, db: AsyncSession):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(user_id: int, db: AsyncSession):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(user: User, db: AsyncSession):
    db.add(user)
    await db.flush()
    return user


async def get_user_list(page: int, page_size: int, db: AsyncSession):
    count_stmt = select(func.count()).select_from(User)
    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(User)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(User.id.desc())
    )
    result = await db.execute(stmt)
    items = result.scalars().all()

    return total, items


async def delete_user(user_id: int, db: AsyncSession):
    stmt = delete(User).where(User.id == user_id)
    await db.execute(stmt)
