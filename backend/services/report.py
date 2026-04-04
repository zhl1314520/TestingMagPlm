from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging
from schemas.report import ReportResponse, ReportPageResponse, MetricsOverview, MetricsTrend, ProjectProgress, ProjectProgressList, ModuleProgress
from models.report import Report
from DAO import report as crud

logger = logging.getLogger(__name__)


async def get_report_list(page: int, page_size: int, project_id: int = None, db: AsyncSession = None):
    total, items = await crud.get_report_list(page, page_size, project_id, db)
    return ReportPageResponse(
        total=total,
        items=items
    )


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
