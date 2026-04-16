from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
import json
import random
from schemas.execution import ExecutionCreate, ExecutionUpdate, ExecutionPageResponse
from models.execution import Execution
from DAO import execution as crud
from DAO import testcase as testcase_crud

logger = logging.getLogger(__name__)


async def create_execution(execution_data: ExecutionCreate, user_id: int, db: AsyncSession):
    logger.info("创建测试执行: project_id=%s, name=%s, type=%s, user_id=%s", 
                execution_data.project_id, execution_data.name, execution_data.type, user_id)

    new_execution = Execution(
        project_id=execution_data.project_id,
        name=execution_data.name,
        type=execution_data.type,
        status=execution_data.status,
        result=execution_data.result,
        total_cases=0,
        passed_cases=0,
        failed_cases=0,
        pass_rate=0.00,
        executed_by=user_id
    )

    await crud.create_execution(new_execution, db)
    await db.commit()
    await db.refresh(new_execution)

    logger.info("测试执行创建成功: id=%s", new_execution.id)
    return new_execution


async def get_execution_list(page: int, db: AsyncSession, page_size: int,
                             project_id: int = None, executed_by: int = None):
    total, items = await crud.get_execution_list(page, db, page_size, project_id, executed_by)
    
    execution_list = []
    for execution, project_name in items:
        execution_dict = {
            "id": execution.id,
            "project_id": execution.project_id,
            "project_name": project_name,
            "name": execution.name,
            "type": execution.type,
            "status": execution.status,
            "result": execution.result,
            "total_cases": execution.total_cases,
            "passed_cases": execution.passed_cases,
            "failed_cases": execution.failed_cases,
            "pass_rate": execution.pass_rate,
            "executed_by": execution.executed_by,
            "created_at": execution.created_at,
            "updated_at": execution.updated_at
        }
        execution_list.append(execution_dict)
    
    return ExecutionPageResponse(
        total=total,
        items=execution_list
    )


async def get_execution_detail(execution_id: int, db: AsyncSession):
    execution, project_name = await crud.get_execution_by_id(execution_id, db)
    if not execution:
        raise HTTPException(
            status_code=404,
            detail="执行不存在"
        )
    
    execution_dict = {
        "id": execution.id,
        "project_id": execution.project_id,
        "project_name": project_name,
        "name": execution.name,
        "type": execution.type,
        "status": execution.status,
        "result": execution.result,
        "total_cases": execution.total_cases,
        "passed_cases": execution.passed_cases,
        "failed_cases": execution.failed_cases,
        "pass_rate": execution.pass_rate,
        "executed_by": execution.executed_by,
        "created_at": execution.created_at,
        "updated_at": execution.updated_at
    }
    
    return execution_dict


async def update_execution(execution_id: int, execution_data: ExecutionUpdate, db: AsyncSession):
    execution = await crud.get_execution_by_id(execution_id, db)
    if not execution:
        raise HTTPException(
            status_code=404,
            detail="执行不存在"
        )
    
    if execution_data.name is not None:
        execution.name = execution_data.name
    if execution_data.type is not None:
        execution.type = execution_data.type
    if execution_data.status is not None:
        execution.status = execution_data.status
    if execution_data.result is not None:
        execution.result = execution_data.result
    
    execution.updated_at = datetime.now()
    
    await db.commit()
    await db.refresh(execution)
    
    logger.info("更新测试执行成功: id=%s", execution_id)
    return execution


async def delete_execution(execution_id: int, db: AsyncSession):
    execution = await crud.get_execution_by_id(execution_id, db)
    if not execution:
        raise HTTPException(
            status_code=404,
            detail="执行不存在"
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
    
    if execution.status == "执行中":
        raise HTTPException(
            status_code=400,
            detail="EXECUTION_ALREADY_RUNNING"
        )
    
    execution.status = "执行中"
    execution.updated_at = datetime.now()
    await db.commit()
    
    logger.info("开始执行测试: execution_id=%s, project_id=%s", execution_id, execution.project_id)
    
    try:
        total_testcases, testcases = await testcase_crud.get_testcase_list(
            page=1,
            page_size=1000,
            project_id=execution.project_id,
            status="有效",
            db=db
        )
        
        total = len(testcases)
        if total == 0:
            execution.total_cases = 0
            execution.passed_cases = 0
            execution.failed_cases = 0
            execution.pass_rate = 0.00
            result = {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "pass_rate": 0,
                "message": "该项目没有有效的测试用例"
            }
        else:
            passed = 0
            failed = 0
            skipped = 0
            
            for testcase in testcases:
                rand = random.random()
                if rand < 0.75:
                    passed += 1
                elif rand < 0.95:
                    failed += 1
                else:
                    skipped += 1
            
            pass_rate = round(passed / total, 2) if total > 0 else 0
            
            execution.total_cases = total
            execution.passed_cases = passed
            execution.failed_cases = failed
            execution.pass_rate = pass_rate
            
            result = {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "pass_rate": pass_rate,
                "execution_type": execution.type
            }
        
        execution.status = "已完成"
        execution.result = json.dumps(result, ensure_ascii=False)
        execution.updated_at = datetime.now()
        await db.commit()
        await db.refresh(execution)
        
        logger.info("测试执行完成: execution_id=%s, result=%s", execution_id, result)
        
    except Exception as e:
        logger.error("测试执行失败: execution_id=%s, error=%s", execution_id, str(e))
        execution.status = "失败"
        execution.result = json.dumps({"error": str(e)}, ensure_ascii=False)
        execution.updated_at = datetime.now()
        await db.commit()
        await db.refresh(execution)
        raise HTTPException(
            status_code=500,
            detail=f"测试执行失败: {str(e)}"
        )
    
    return execution
