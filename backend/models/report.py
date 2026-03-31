from sqlalchemy import DateTime, func, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pass_rate: Mapped[float] = mapped_column(Float, nullable=False)
    fail_rate: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
