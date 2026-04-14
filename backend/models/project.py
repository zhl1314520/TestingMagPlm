"""
项目模型模块

对应数据库表：projects
描述：存储测试项目信息
"""
from sqlalchemy import String, DateTime, func, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Project(Base):
    """
    项目模型类
    
    对应数据库表：projects
    
    Attributes:
        id: 项目 ID（主键，自增）
        name: 项目名称（最多 100 字符）
        description: 项目描述（文本）
        owner_id: 项目负责人 ID（外键，关联 users.id）
        created_at: 创建时间（自动填充）
        updated_at: 更新时间（自动更新）
        deleted_at: 软删除时间（可选）
    """
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True, 
        comment="项目 ID"
    )
    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False, 
        comment="项目名称"
    )
    description: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        comment="项目描述"
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        comment="项目所属人 ID"
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        comment="创建时间"
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now(), 
        comment="更新时间"
    )
    deleted_at: Mapped[DateTime] = mapped_column(
        DateTime, 
        nullable=True,
        default=None,
        comment="软删除时间"
    )


    # Debug
    def __repr__(self):
        return (
            f"<Project id={self.id} "
            f"name='{self.name}' "
            f"owner_id={self.owner_id}>"
        )
