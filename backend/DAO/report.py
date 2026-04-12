from sqlalchemy import select, func, delete, case, and_, desc, union_all, literal_column, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from datetime import datetime, timedelta
from models.report import Report
from models.project import Project
from models.testcase import TestCase
from models.bug import Bug
from models.execution import Execution
from models.project_member import ProjectMember
from models.user import User


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

    Executor = aliased(User)
    
    stmt = (
        select(Report, User.username, Project.name, Execution.name, Executor.username)
        .select_from(Report)
        .join(User, Report.created_by == User.id)
        .join(Project, Report.project_id == Project.id)
        .outerjoin(Execution, Report.execution_id == Execution.id)
        .outerjoin(Executor, Execution.executed_by == Executor.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Report.id.desc())
    )
    
    if project_id:
        stmt = stmt.where(Report.project_id == project_id)
    
    result = await db.execute(stmt)
    rows = result.all()
    items = []
    for row in rows:
        report, created_by_name, project_name, execution_name, executor_name = row
        items.append((report, created_by_name, project_name, execution_name, executor_name))

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

    Executor = aliased(User)

    stmt = (
        select(Report, User.username, Project.name, Execution.name, Executor.username)
        .select_from(Report)
        .join(User, Report.created_by == User.id)
        .join(Project, Report.project_id == Project.id)
        .outerjoin(Execution, Report.execution_id == Execution.id)
        .outerjoin(Executor, Execution.executed_by == Executor.id)
        .where(Report.created_by == user_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Report.id.desc())
    )
    
    if project_id:
        stmt = stmt.where(Report.project_id == project_id)
    
    result = await db.execute(stmt)
    rows = result.all()
    items = []
    for row in rows:
        report, created_by_name, project_name, execution_name, executor_name = row
        items.append((report, created_by_name, project_name, execution_name, executor_name))
    logger.info(f"Reports returned: {[r.id for r, _, _, _, _ in items]}")

    return total, items


async def delete_all_reports(db: AsyncSession):
    stmt = delete(Report)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount


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


async def get_recent_activities(user_id: int, db: AsyncSession, limit: int = 10):
    now = datetime.now()
    
    project_stmt = (
        select(Project.id)
        .join(ProjectMember, ProjectMember.project_id == Project.id)
        .where(ProjectMember.user_id == user_id)
        .where(Project.deleted_at.is_(None))
    )
    project_result = await db.execute(project_stmt)
    user_project_ids = [row[0] for row in project_result.all()]
    
    if not user_project_ids:
        return []
    
    activities = []
    
    execution_stmt = (
        select(
            Execution.id,
            Execution.name,
            Execution.status,
            Execution.pass_rate,
            Execution.created_at,
            literal_column("'execution'").label('activity_type')
        )
        .where(Execution.project_id.in_(user_project_ids))
        .order_by(desc(Execution.updated_at))
        .limit(limit)
    )
    execution_result = await db.execute(execution_stmt)
    for row in execution_result.all():
        time_diff = now - row.created_at
        time_str = _format_time_diff(time_diff)
        pass_rate = float(row.pass_rate) if row.pass_rate else 0
        status_map = {"已完成": "完成", "进行中": "进行中", "待执行": "待执行"}
        badge_text = status_map.get(row.status, row.status)
        activities.append({
            "type": "success" if row.status == "已完成" else "info",
            "badge": badge_text,
            "time": time_str,
            "title": f"测试执行: {row.name}",
            "description": f"状态: {row.status}，通过率 {pass_rate:.1f}%。",
            "sort_time": row.created_at
        })
    
    bug_stmt = (
        select(
            Bug.id,
            Bug.title,
            Bug.priority,
            Bug.status,
            Bug.created_at,
            literal_column("'bug'").label('activity_type')
        )
        .where(Bug.project_id.in_(user_project_ids))
        .order_by(desc(Bug.created_at))
        .limit(limit)
    )
    bug_result = await db.execute(bug_stmt)
    for row in bug_result.all():
        time_diff = now - row.created_at
        time_str = _format_time_diff(time_diff)
        priority_map = {"high": "高", "medium": "中", "low": "低"}
        priority_text = priority_map.get(row.priority, row.priority)
        activities.append({
            "type": "warning",
            "badge": "新增",
            "time": time_str,
            "title": f"发现新缺陷: {row.title}",
            "description": f"优先级: {priority_text}，状态: {row.status}。",
            "sort_time": row.created_at
        })
    
    project_create_stmt = (
        select(
            Project.id,
            Project.name,
            Project.created_at,
            literal_column("'project'").label('activity_type')
        )
        .where(Project.id.in_(user_project_ids))
        .where(Project.deleted_at.is_(None))
        .order_by(desc(Project.created_at))
        .limit(limit)
    )
    project_result = await db.execute(project_create_stmt)
    for row in project_result.all():
        time_diff = now - row.created_at
        time_str = _format_time_diff(time_diff)
        activities.append({
            "type": "info",
            "badge": "创建",
            "time": time_str,
            "title": f"项目创建: {row.name}",
            "description": "新项目已建立，团队开始补充基础测试用例。",
            "sort_time": row.created_at
        })
    
    testcase_stmt = (
        select(
            TestCase.id,
            TestCase.title,
            TestCase.module,
            TestCase.status,
            TestCase.created_at,
            literal_column("'testcase'").label('activity_type')
        )
        .where(TestCase.project_id.in_(user_project_ids))
        .order_by(desc(TestCase.created_at))
        .limit(limit)
    )
    testcase_result = await db.execute(testcase_stmt)
    for row in testcase_result.all():
        time_diff = now - row.created_at
        time_str = _format_time_diff(time_diff)
        activities.append({
            "type": "success",
            "badge": "更新",
            "time": time_str,
            "title": f"测试用例更新: {row.title}",
            "description": f"模块: {row.module}，状态: {row.status}。",
            "sort_time": row.created_at
        })
    
    activities.sort(key=lambda x: x["sort_time"], reverse=True)
    
    result = []
    for activity in activities[:limit]:
        result.append({
            "type": activity["type"],
            "badge": activity["badge"],
            "time": activity["time"],
            "title": activity["title"],
            "description": activity["description"]
        })
    
    return result


def _format_time_diff(time_diff: timedelta) -> str:
    total_seconds = int(time_diff.total_seconds())
    
    if total_seconds < 60:
        return "刚刚"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes} 分钟前"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours} 小时前"
    elif total_seconds < 604800:
        days = total_seconds // 86400
        return f"{days} 天前"
    else:
        weeks = total_seconds // 604800
        return f"{weeks} 周前"
