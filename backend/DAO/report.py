from sqlalchemy import select, func, delete, case, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from models.report import Report
from models.project import Project
from models.testcase import TestCase
from models.bug import Bug
from models.execution import Execution
from models.project_member import ProjectMember


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


async def get_user_report_list(user_id: int, page: int, page_size: int, project_id: int = None, db: AsyncSession = None):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"get_user_report_list called with user_id={user_id}")
    
    count_stmt = select(func.count()).select_from(Report).where(Report.created_by == user_id)
    
    if project_id:
        count_stmt = count_stmt.where(Report.project_id == project_id)
    
    total = (await db.execute(count_stmt)).scalar()
    logger.info(f"Total reports for user_id={user_id}: {total}")

    stmt = (
        select(Report)
        .where(Report.created_by == user_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Report.id.desc())
    )
    
    if project_id:
        stmt = stmt.where(Report.project_id == project_id)
    
    result = await db.execute(stmt)
    items = result.scalars().all()
    logger.info(f"Reports returned: {[r.id for r in items]}")

    return total, items


async def get_metrics_overview(db: AsyncSession):
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)
    
    total_projects = (await db.execute(select(func.count()).select_from(Project))).scalar() or 0
    total_testcases = (await db.execute(select(func.count()).select_from(TestCase))).scalar() or 0
    total_bugs = (await db.execute(select(func.count()).select_from(Bug))).scalar() or 0
    total_executions = (await db.execute(select(func.count()).select_from(Execution))).scalar() or 0
    
    this_week_projects = (await db.execute(
        select(func.count()).select_from(Project).where(Project.created_at >= one_week_ago)
    )).scalar() or 0
    this_week_testcases = (await db.execute(
        select(func.count()).select_from(TestCase).where(TestCase.created_at >= one_week_ago)
    )).scalar() or 0
    this_week_bugs = (await db.execute(
        select(func.count()).select_from(Bug).where(Bug.created_at >= one_week_ago)
    )).scalar() or 0
    this_week_executions = (await db.execute(
        select(func.count()).select_from(Execution).where(Execution.created_at >= one_week_ago)
    )).scalar() or 0
    
    last_week_projects = (await db.execute(
        select(func.count()).select_from(Project).where(
            and_(Project.created_at >= two_weeks_ago, Project.created_at < one_week_ago)
        )
    )).scalar() or 0
    last_week_testcases = (await db.execute(
        select(func.count()).select_from(TestCase).where(
            and_(TestCase.created_at >= two_weeks_ago, TestCase.created_at < one_week_ago)
        )
    )).scalar() or 0
    last_week_bugs = (await db.execute(
        select(func.count()).select_from(Bug).where(
            and_(Bug.created_at >= two_weeks_ago, Bug.created_at < one_week_ago)
        )
    )).scalar() or 0
    last_week_executions = (await db.execute(
        select(func.count()).select_from(Execution).where(
            and_(Execution.created_at >= two_weeks_ago, Execution.created_at < one_week_ago)
        )
    )).scalar() or 0
    
    def calc_growth(current: int, previous: int) -> dict:
        if previous == 0:
            if current > 0:
                return {"value": 100, "is_positive": True}
            return {"value": 0, "is_positive": True}
        growth = round((current - previous) / previous * 100)
        return {"value": abs(growth), "is_positive": growth >= 0}
    
    projects_growth = calc_growth(this_week_projects, last_week_projects)
    testcases_growth = calc_growth(this_week_testcases, last_week_testcases)
    bugs_growth = calc_growth(this_week_bugs, last_week_bugs)
    executions_growth = calc_growth(this_week_executions, last_week_executions)
    
    return {
        "total_projects": total_projects,
        "total_testcases": total_testcases,
        "total_bugs": total_bugs,
        "total_executions": total_executions,
        "projects_growth": projects_growth["value"],
        "projects_growth_positive": projects_growth["is_positive"],
        "testcases_growth": testcases_growth["value"],
        "testcases_growth_positive": testcases_growth["is_positive"],
        "bugs_growth": bugs_growth["value"],
        "bugs_growth_positive": bugs_growth["is_positive"],
        "executions_growth": executions_growth["value"],
        "executions_growth_positive": executions_growth["is_positive"]
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


async def get_user_project_progress(user_id: int, db: AsyncSession):
    project_stmt = (
        select(Project.id, Project.name)
        .join(ProjectMember, ProjectMember.project_id == Project.id)
        .where(ProjectMember.user_id == user_id)
        .where(Project.deleted_at.is_(None))
    )
    project_result = await db.execute(project_stmt)
    projects = project_result.all()
    
    progress_list = []
    for project_id, project_name in projects:
        total_stmt = select(func.count()).select_from(TestCase).where(TestCase.project_id == project_id)
        total_testcases = (await db.execute(total_stmt)).scalar() or 0
        
        completed_stmt = (
            select(func.count())
            .select_from(TestCase)
            .where(TestCase.project_id == project_id)
            .where(TestCase.status != 'new')
        )
        completed_testcases = (await db.execute(completed_stmt)).scalar() or 0
        
        progress_percentage = (completed_testcases / total_testcases * 100) if total_testcases > 0 else 0
        
        module_stmt = (
            select(TestCase.module, func.count().label('total'))
            .where(TestCase.project_id == project_id)
            .group_by(TestCase.module)
        )
        module_result = await db.execute(module_stmt)
        modules_data = module_result.all()
        
        modules = []
        for module_name, module_total in modules_data:
            module_completed_stmt = (
                select(func.count())
                .select_from(TestCase)
                .where(TestCase.project_id == project_id)
                .where(TestCase.module == module_name)
                .where(TestCase.status != 'new')
            )
            module_completed = (await db.execute(module_completed_stmt)).scalar() or 0
            
            module_progress = (module_completed / module_total * 100) if module_total > 0 else 0
            
            modules.append({
                "module_name": module_name,
                "total_testcases": module_total,
                "completed_testcases": module_completed,
                "progress_percentage": round(module_progress, 1)
            })
        
        progress_list.append({
            "project_id": project_id,
            "project_name": project_name,
            "total_testcases": total_testcases,
            "completed_testcases": completed_testcases,
            "progress_percentage": round(progress_percentage, 1),
            "modules": modules
        })
    
    return progress_list
