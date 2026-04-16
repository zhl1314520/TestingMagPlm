from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from schemas.testcase import TestCaseCreate, TestCaseUpdate, TestCasePageResponse
from models.testcase import TestCase
from DAO import testcase as crud

logger = logging.getLogger(__name__)


async def create_testcase(testcase_data: TestCaseCreate, user_id: int, db: AsyncSession):
    logger.info("创建测试用例: data=%s, user_id=%s", testcase_data.model_dump(), user_id)

    try:
        new_testcase = TestCase(
            project_id=testcase_data.project_id,
            module=testcase_data.module,
            title=testcase_data.title,
            steps=testcase_data.steps,
            expected=testcase_data.expected,
            status=testcase_data.status,
            created_by=user_id
        )

        await crud.create_testcase(new_testcase, db)
        await db.commit()
        await db.refresh(new_testcase)

        logger.info("测试用例创建成功: id=%s", new_testcase.id)
        return new_testcase
    except Exception as e:
        await db.rollback()
        logger.error("创建测试用例失败: %s", str(e))
        raise HTTPException(status_code=400, detail=f"创建测试用例失败: {str(e)}")


async def get_testcase_list(db: AsyncSession, created_by: int, page: int, page_size: int, project_id: int = None,
                            module: str = None, status: str = None):
    total, items = await crud.get_testcase_list(db, created_by, page, page_size, project_id, module, status)
    return TestCasePageResponse(
        total=total,
        items=items
    )


async def delete_testcase(testcase_id: int, db: AsyncSession):
    testcase = await crud.get_testcase_by_id(testcase_id, db)
    if not testcase:
        raise HTTPException(
            status_code=404,
            detail="测试用例不存在"
        )
    
    await crud.delete_testcase(testcase_id, db)
    await db.commit()
    return {
        "code": 200,
        "message": "删除成功"
    }


async def update_testcase(testcase_id: int, testcase_data: TestCaseUpdate, db: AsyncSession):
    testcase = await crud.get_testcase_by_id(testcase_id, db)
    if not testcase:
        raise HTTPException(
            status_code=404,
            detail="该用例不存在"
        )
    
    update_data = testcase_data.model_dump(exclude_unset=True)  # 模型对象 -> dict
    for field, value in update_data.items():
        setattr(testcase, field, value) # 动态设置属性值
    
    await crud.update_testcase(testcase, db)
    await db.commit()
    await db.refresh(testcase)
    
    return testcase
