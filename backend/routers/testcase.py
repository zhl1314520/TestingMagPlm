from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from core.security import get_current_user
from schemas.testcase import TestCaseCreate, TestCaseUpdate, TestCaseResponse, TestCasePageResponse
from services import testcase as service
from DAO import testcase as crud
from fastapi import HTTPException

router = APIRouter(
    prefix="/testcases",
    tags=["测试用例管理"]
)


@router.post("", response_model=TestCaseResponse)
async def create_testcase(
    testcase_info: TestCaseCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.create_testcase(testcase_info, current_user["user_id"], db)


@router.get("", response_model=TestCasePageResponse)
async def get_testcase_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    # 在 Python 的函数参数定义中， 没有默认值的参数被视为位置参数，必须放在有默认值的参数之前。
    # 下面的 3 个是过滤参数，用于搜索
    project_id: int = Query(None),      # 可选的过滤参数
    module: str = Query(None),          # 可选的过滤参数
    status: str = Query(None),          # 可选的过滤参数
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_testcase_list(db, current_user["user_id"], page, page_size, project_id, module, status)


@router.get("/{id}", response_model=TestCaseResponse)
async def get_testcase(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    testcase = await crud.get_testcase_by_id(id, db)        # 简单查询不用 service 层了，直接调用 DAO 层的函数
    if not testcase:
        raise HTTPException(status_code=404, detail="此用例不存在")
    return testcase


@router.put("/{id}", response_model=TestCaseResponse)
async def update_testcase(
    id: int,
    testcase_info: TestCaseUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await service.update_testcase(id, testcase_info, db)


@router.delete("/{id}")
async def delete_testcase(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_testcase(id, db)
