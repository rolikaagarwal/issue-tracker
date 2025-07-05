from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
import enum
from app.schemas.attachment import AttachmentRead

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

class IssueRead(BaseModel):
    id: int
    title: str
    description: str
    severity: SeverityEnum
    reporter_id: int
    attachment: Optional[AttachmentRead] = None  

    model_config = dict(from_attributes=True)
