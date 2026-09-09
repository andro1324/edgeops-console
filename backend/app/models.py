from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

Severity = Literal['low', 'medium', 'high', 'critical']
IncidentStatus = Literal['investigating', 'monitoring', 'resolved']

class IncidentCreate(BaseModel):
    title: str = Field(min_length=4, max_length=120)
    summary: str = Field(min_length=8, max_length=600)
    severity: Severity
    region: str = Field(min_length=2, max_length=32)

class Incident(IncidentCreate):
    id: int
    status: IncidentStatus
    owner: str
    started_at: datetime
