from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from core.security import get_current_user
from schemas.testcase import TestCaseCreate, TestCaseUpdate, TestCaseResponse, TestCasePageResponse
from services import testcase as service

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
    project_id: int = Query(None),
    module: str = Query(None),
    status: str = Query(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_testcase_list(page, page_size, project_id, module, status, current_user["user_id"], db)


@router.get("/{id}", response_model=TestCaseResponse)
async def get_testcase(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    from DAO import testcase as crud
    testcase = await crud.get_testcase_by_id(id, db)
    if not testcase:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="TESTCASE_NOT_FOUND")
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
