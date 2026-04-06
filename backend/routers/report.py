from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from core.security import get_current_user
from schemas.report import ReportResponse, ReportPageResponse, MetricsOverview, MetricsTrend, ProjectProgressList, RecentActivityList
from services import report as service

router = APIRouter(
    prefix="/reports",
    tags=["报告管理"]
)


@router.get("", response_model=ReportPageResponse)
async def get_report_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    project_id: int = Query(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_user_report_list(current_user["user_id"], page, page_size, project_id, db)


metrics_router = APIRouter(
    prefix="/metrics",
    tags=["数据统计"]
)


@metrics_router.get("/overview", response_model=MetricsOverview)
async def get_metrics_overview(
    db: AsyncSession = Depends(get_db)
):
    return await service.get_metrics_overview(db)


@metrics_router.get("/trend")
async def get_metrics_trend(
    db: AsyncSession = Depends(get_db)
):
    return await service.get_metrics_trend(db)


@metrics_router.get("/project-progress", response_model=ProjectProgressList)
async def get_project_progress(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_user_project_progress(current_user["user_id"], db)


@metrics_router.get("/recent-activities", response_model=RecentActivityList)
async def get_recent_activities(
    limit: int = Query(10, ge=1, le=50),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_user_recent_activities(current_user["user_id"], db, limit)
