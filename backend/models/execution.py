from sqlalchemy import String, DateTime, func, Integer, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Execution(Base):
    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="手动执行")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="等待中")
    result: Mapped[str] = mapped_column(Text, nullable=False, default="")
    total_cases: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    passed_cases: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    failed_cases: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    pass_rate: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True, default=0.00)
    executed_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
