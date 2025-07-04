from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Enum
from app.database.base_class import Base
from app.models.issues import StatusEnum

class DailyStats(Base):
    __tablename__ = "daily_stats"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    count = Column(Integer, nullable=False)
