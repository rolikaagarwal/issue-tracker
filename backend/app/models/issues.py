import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.base_class import Base

class SeverityEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class StatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(SeverityEnum), default=SeverityEnum.LOW, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.OPEN, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reporter = relationship("User")
    attachments = relationship(
        "FileAttachment",
        back_populates="issue",
        cascade="all, delete-orphan",
    )
