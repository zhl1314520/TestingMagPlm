from typing import List
from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: int
    project_id: int
    pass_rate: float
    fail_rate: float
    created_at: str

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
