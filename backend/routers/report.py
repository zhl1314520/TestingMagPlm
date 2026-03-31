from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from schemas.report import ReportResponse, ReportPageResponse, MetricsOverview, MetricsTrend
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
    db: AsyncSession = Depends(get_db)
):
    return await service.get_report_list(page, page_size, project_id, db)


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
