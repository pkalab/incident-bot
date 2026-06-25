from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Severity(str, Enum):
    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"


class IncidentStatus(str, Enum):
    INVESTIGATING = "Investigating"
    MITIGATING = "Mitigating"
    RESOLVED = "Resolved"


class PlaybookResult(BaseModel):
    playbook_name: str
    status: str
    summary: str
    details: str
    ran_at: datetime


class TimelineEvent(BaseModel):
    timestamp: datetime
    event: str
    actor: str


class Postmortem(BaseModel):
    summary: str
    timeline: list[TimelineEvent]
    root_causes: list[str]
    action_items: list[str]
    created_at: datetime = datetime.now()


class Incident(BaseModel):
    id: str
    title: str
    severity: Severity
    status: IncidentStatus
    channel_id: str
    declared_by: str
    declared_at: datetime
    resolved_at: Optional[datetime] = None
    playbook_results: list[PlaybookResult] = []
    postmortem: Optional[Postmortem] = None
