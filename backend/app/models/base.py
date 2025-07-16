from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

from app.core.database import Base


class BaseModel(Base):
    __abstract__ = True  # 抽象基类，不创建表

    id = Column(Integer, primary_key=True, index=True, comment="主键ID")
    created_at = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment="更新时间")
