from sqlalchemy import String, DateTime, func, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Bug(Base):
    __tablename__ = "bugs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False)
    testcase_id: Mapped[int] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="new")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="p3")
    reporter_id: Mapped[int] = mapped_column(Integer, nullable=False)
    assignee_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


    # Debug
    def __repr__(self):
        return (f"<Bug(id={self.id}, title='{self.title}', status='{self.status}',"
                f" priority='{self.priority}')>")
