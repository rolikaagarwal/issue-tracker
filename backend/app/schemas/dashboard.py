from pydantic import BaseModel, ConfigDict
from app.models.issues import StatusEnum
from datetime import datetime

class DailyStat(BaseModel):
    timestamp: datetime
    status: StatusEnum
    count: int

    model_config = ConfigDict(from_attributes=True)
