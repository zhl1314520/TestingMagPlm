from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.report import Report
from models.project import Project
from models.testcase import TestCase
from models.bug import Bug
from models.execution import Execution


async def get_report_by_id(report_id: int, db: AsyncSession):
    stmt = select(Report).where(Report.id == report_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_report(report: Report, db: AsyncSession):
    db.add(report)
    await db.flush()
    return report


async def get_report_list(page: int, page_size: int, project_id: int = None, db: AsyncSession = None):
    count_stmt = select(func.count()).select_from(Report)
    
    if project_id:
        count_stmt = count_stmt.where(Report.project_id == project_id)
    
    total = (await db.execute(count_stmt)).scalar()

    stmt = (
        select(Report)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Report.id.desc())
    )
    
    if project_id:
        stmt = stmt.where(Report.project_id == project_id)
    
    result = await db.execute(stmt)
    items = result.scalars().all()

    return total, items


async def get_metrics_overview(db: AsyncSession):
    total_projects = (await db.execute(select(func.count()).select_from(Project))).scalar()
    total_testcases = (await db.execute(select(func.count()).select_from(TestCase))).scalar()
    total_bugs = (await db.execute(select(func.count()).select_from(Bug))).scalar()
    total_executions = (await db.execute(select(func.count()).select_from(Execution))).scalar()
    
    return {
        "total_projects": total_projects or 0,
        "total_testcases": total_testcases or 0,
        "total_bugs": total_bugs or 0,
        "total_executions": total_executions or 0
    }


async def get_metrics_trend(db: AsyncSession):
    stmt = (
        select(Report)
        .order_by(Report.created_at.desc())
        .limit(7)
    )
    result = await db.execute(stmt)
    reports = result.scalars().all()
    
    trend = []
    for report in reversed(reports):
        trend.append({
            "date": report.created_at.strftime("%Y-%m-%d"),
            "pass_rate": report.pass_rate,
            "fail_rate": report.fail_rate
        })
    
    return trend
