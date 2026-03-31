from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from routers import system
from routers.user import router, user_router
from routers import project, testcase, execution, bug, report

app = FastAPI()

# 全局日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# 打开 SQL 日志
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system.router)
app.include_router(router)
app.include_router(user_router)
app.include_router(project.router)
app.include_router(testcase.router)
app.include_router(execution.router)
app.include_router(bug.router)
app.include_router(report.router)
app.include_router(report.metrics_router)
