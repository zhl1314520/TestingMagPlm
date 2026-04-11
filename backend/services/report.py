from sqlalchemy.ext.asyncio import AsyncSession
import logging
from schemas.report import ReportResponse, ReportPageResponse, MetricsOverview, MetricsTrend, ProjectProgress, ProjectProgressList, ModuleProgress, RecentActivity, RecentActivityList
from models.report import Report
from DAO import report as crud

logger = logging.getLogger(__name__)


async def get_report_list(page: int, page_size: int, project_id: int = None, db: AsyncSession = None):
    total, items = await crud.get_report_list(page, page_size, project_id, db)
    
    report_list = []
    for report, created_by_name, project_name, execution_name in items:
        display_project_name = project_name or f"项目ID:{report.project_id}"
        display_creator_name = created_by_name or f"用户ID:{report.created_by}"
        if report.execution_id is None:
            display_execution = "暂未指定"
        else:
            display_execution = execution_name or f"执行ID:{report.execution_id}"
        display_updated_at = report.updated_at or report.created_at

        report_data = ReportResponse(
            id=report.id,
            project_id=report.project_id,
            project_name=display_project_name,
            execution_id=report.execution_id,
            execution_name=display_execution,
            title=report.title,
            pass_rate=report.pass_rate or 0.0,
            fail_rate=report.fail_rate or 0.0,
            total_cases=report.total_cases or 0,
            passed_cases=report.passed_cases or 0,
            failed_cases=report.failed_cases or 0,
            created_by=report.created_by,
            created_by_name=display_creator_name,
            created_at=report.created_at,
            updated_at=display_updated_at
        )
        report_list.append(report_data)
    
    return ReportPageResponse(
        total=total,
        items=report_list
    )


async def get_user_report_list(user_id: int, page: int, page_size: int, project_id: int = None, db: AsyncSession = None):
    total, items = await crud.get_user_report_list(user_id, page, page_size, project_id, db)
    
    report_list = []
    for report, created_by_name, project_name, execution_name in items:
        display_project_name = project_name or f"项目ID:{report.project_id}"
        display_creator_name = created_by_name or f"用户ID:{report.created_by}"
        if report.execution_id is None:
            display_execution = "暂未指定"
        else:
            display_execution = execution_name or f"执行ID:{report.execution_id}"
        display_updated_at = report.updated_at or report.created_at

        report_data = ReportResponse(
            id=report.id,
            project_id=report.project_id,
            project_name=display_project_name,
            execution_id=report.execution_id,
            execution_name=display_execution,
            title=report.title,
            pass_rate=report.pass_rate or 0.0,
            fail_rate=report.fail_rate or 0.0,
            total_cases=report.total_cases or 0,
            passed_cases=report.passed_cases or 0,
            failed_cases=report.failed_cases or 0,
            created_by=report.created_by,
            created_by_name=display_creator_name,
            created_at=report.created_at,
            updated_at=display_updated_at
        )
        report_list.append(report_data)
    
    return ReportPageResponse(
        total=total,
        items=report_list
    )


async def delete_all_reports(db: AsyncSession):
    deleted_count = await crud.delete_all_reports(db)
    return {"deleted_count": deleted_count}


async def get_metrics_overview(db: AsyncSession):
    metrics = await crud.get_metrics_overview(db)
    return MetricsOverview(**metrics)


async def get_metrics_trend(db: AsyncSession):
    trend_data = await crud.get_metrics_trend(db)
    return [MetricsTrend(**item) for item in trend_data]


async def get_user_project_progress(user_id: int, db: AsyncSession):
    progress_data = await crud.get_user_project_progress(user_id, db)
    projects = []
    for project_data in progress_data:
        modules = [
            ModuleProgress(**module) for module in project_data.get('modules', [])
        ]
        project = ProjectProgress(
            project_id=project_data['project_id'],
            project_name=project_data['project_name'],
            total_testcases=project_data['total_testcases'],
            completed_testcases=project_data['completed_testcases'],
            progress_percentage=project_data['progress_percentage'],
            modules=modules
        )
        projects.append(project)
    return ProjectProgressList(projects=projects)


async def get_user_recent_activities(user_id: int, db: AsyncSession, limit: int = 10):
    activities_data = await crud.get_recent_activities(user_id, db, limit)
    activities = [RecentActivity(**activity) for activity in activities_data]
    return RecentActivityList(activities=activities)
