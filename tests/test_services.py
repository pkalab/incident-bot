from datetime import datetime
from bot.models.incident import Incident, Severity, IncidentStatus


def test_incident_store_round_trip():
    inc = Incident(
        id="inc-20260624-002",
        title="Test",
        severity=Severity.SEV3,
        status=IncidentStatus.INVESTIGATING,
        channel_id="C456",
        declared_by="U456",
        declared_at=datetime.now(),
    )
    assert inc.id == "inc-20260624-002"
    assert inc.title == "Test"
    assert inc.severity == Severity.SEV3
