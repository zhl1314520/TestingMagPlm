from sqlalchemy import select, func, delete, case
from sqlalchemy.ext.asyncio import AsyncSession
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
