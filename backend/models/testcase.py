from sqlalchemy import String, DateTime, func, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
    module: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    steps: Mapped[str] = mapped_column(Text, nullable=False)
    expected: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="有效")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="p3")
    created_by: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    deleted_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
        comment="软删除时间"
    )

    # Debug
    def __repr__(self):
        return (
            f"<TestCase id={self.id} "
            f"title='{self.title}' "
            f"module='{self.module}' "
            f"status='{self.status}' "
            f"priority='{self.priority}'>"
        )