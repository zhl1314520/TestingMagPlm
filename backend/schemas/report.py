from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: int
    project_id: int
    execution_id: Optional[int] = None
    title: str
    pass_rate: float
    fail_rate: float
    total_cases: int
    passed_cases: int
    failed_cases: int
    created_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReportPageResponse(BaseModel):
    total: int
    items: List[ReportResponse]


class MetricsOverview(BaseModel):
    total_projects: int
    total_testcases: int
    total_bugs: int
    total_executions: int
    projects_growth: int
    projects_growth_positive: bool
    testcases_growth: int
    testcases_growth_positive: bool
    bugs_growth: int
    bugs_growth_positive: bool
    executions_growth: int
    executions_growth_positive: bool


class MetricsTrend(BaseModel):
    date: str
    pass_rate: float
    fail_rate: float


class ModuleProgress(BaseModel):
    module_name: str
    total_testcases: int
    completed_testcases: int
    progress_percentage: float


class ProjectProgress(BaseModel):
    project_id: int
    project_name: str
    total_testcases: int
    completed_testcases: int
    progress_percentage: float
    modules: List[ModuleProgress] = []


class ProjectProgressList(BaseModel):
    projects: List[ProjectProgress]


class RecentActivity(BaseModel):
    type: str
    badge: str
    time: str
    title: str
    description: str


class RecentActivityList(BaseModel):
    activities: List[RecentActivity]
