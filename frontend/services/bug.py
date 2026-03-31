from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from schemas.bug import BugCreate, BugUpdate, BugPageResponse
from models.bug import Bug
from DAO import bug as crud

logger = logging.getLogger(__name__)


async def create_bug(bug_data: BugCreate, db: AsyncSession):
    logger.info("创建缺陷: title=%s", bug_data.title)

    new_bug = Bug(
        project_id=bug_data.project_id,
        testcase_id=bug_data.testcase_id,
        title=bug_data.title,
        description=bug_data.description,
        status=bug_data.status,
        priority=bug_data.priority,
        assignee_id=bug_data.assignee_id
    )

    await crud.create_bug(new_bug, db)
    await db.commit()
    await db.refresh(new_bug)

    logger.info("缺陷创建成功: id=%s", new_bug.id)
    return new_bug


async def get_bug_list(page: int, page_size: int, project_id: int = None, status: str = None, priority: str = None, db: AsyncSession = None):
    total, items = await crud.get_bug_list(page, page_size, project_id, status, priority, db)
    return BugPageResponse(
        total=total,
        items=items
    )


async def delete_bug(bug_id: int, db: AsyncSession):
    bug = await crud.get_bug_by_id(bug_id, db)
    if not bug:
        raise HTTPException(
            status_code=404,
            detail="BUG_NOT_FOUND"
        )
    
    await crud.delete_bug(bug_id, db)
    await db.commit()
    return {
        "code": 200,
        "message": "删除成功"
    }


async def update_bug(bug_id: int, bug_data: BugUpdate, db: AsyncSession):
    bug = await crud.get_bug_by_id(bug_id, db)
    if not bug:
        raise HTTPException(
            status_code=404,
            detail="BUG_NOT_FOUND"
        )
    
    update_data = bug_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bug, field, value)
    
    await crud.update_bug(bug, db)
    await db.commit()
    await db.refresh(bug)
    
    return bug


async def update_bug_status(bug_id: int, status: str, db: AsyncSession):
    bug = await crud.get_bug_by_id(bug_id, db)
    if not bug:
        raise HTTPException(
            status_code=404,
            detail="BUG_NOT_FOUND"
        )
    
    bug.status = status
    await crud.update_bug(bug, db)
    await db.commit()
    await db.refresh(bug)
    
    return bug
