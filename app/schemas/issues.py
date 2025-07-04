from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
import enum

class SeverityEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class StatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    TRIAGED = "TRIAGED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class IssueBase(BaseModel):
    title: str
    description: str
    severity: SeverityEnum = SeverityEnum.LOW

class IssueCreate(IssueBase):
    pass

class IssueUpdate(BaseModel):
    status: Optional[StatusEnum]

class IssueRead(IssueBase):
    id: int
    status: StatusEnum
    created_at: datetime
    updated_at: datetime
    reporter_id: int

    model_config = ConfigDict(from_attributes=True)
