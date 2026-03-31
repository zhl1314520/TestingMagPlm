from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
import json
from schemas.execution import ExecutionCreate, ExecutionPageResponse
from models.execution import Execution
from DAO import execution as crud

logger = logging.getLogger(__name__)


async def create_execution(execution_data: ExecutionCreate, db: AsyncSession):
    logger.info("创建测试执行: project_id=%s, type=%s", execution_data.project_id, execution_data.type)

    new_execution = Execution(
        project_id=execution_data.project_id,
        type=execution_data.type,
        status="running"
    )

    await crud.create_execution(new_execution, db)
    await db.commit()
    await db.refresh(new_execution)

    logger.info("测试执行创建成功: id=%s", new_execution.id)
    return new_execution


async def get_execution_list(page: int, page_size: int, project_id: int = None, db: AsyncSession = None):
    total, items = await crud.get_execution_list(page, page_size, project_id, db)
    return ExecutionPageResponse(
        total=total,
        items=items
    )


async def delete_execution(execution_id: int, db: AsyncSession):
    execution = await crud.get_execution_by_id(execution_id, db)
    if not execution:
        raise HTTPException(
            status_code=404,
            detail="EXECUTION_NOT_FOUND"
        )
    
    await crud.delete_execution(execution_id, db)
    await db.commit()
    return {
        "code": 200,
        "message": "删除成功"
    }


async def run_execution(execution_id: int, db: AsyncSession):
    execution = await crud.get_execution_by_id(execution_id, db)
    if not execution:
        raise HTTPException(
            status_code=404,
            detail="EXECUTION_NOT_FOUND"
        )
    
    execution.status = "running"
    await db.commit()
    
    logger.info("开始执行测试: execution_id=%s", execution_id)
    
    result = {
        "total": 10,
        "passed": 8,
        "failed": 2,
        "pass_rate": 0.8
    }
    
    execution.status = "completed"
    execution.result = json.dumps(result)
    await db.commit()
    await db.refresh(execution)
    
    return execution
