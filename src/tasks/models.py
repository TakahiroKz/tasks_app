from datetime import datetime

from src.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String,nullable=False)
    is_completed =  Column(Boolean, default=False)
    created_at = Column(DateTime,default=datetime.utcnow)
