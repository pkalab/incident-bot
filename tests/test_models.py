from datetime import datetime
from bot.models.incident import Incident, Severity, IncidentStatus


def test_incident_creation():
    inc = Incident(
        id="inc-20260624-001",
        title="API latency spike",
        severity=Severity.SEV2,
        status=IncidentStatus.INVESTIGATING,
        channel_id="C123",
        declared_by="U123",
        declared_at=datetime.now(),
    )
    assert inc.id == "inc-20260624-001"
    assert inc.status == IncidentStatus.INVESTIGATING
    assert inc.severity == Severity.SEV2
    assert inc.playbook_results == []
    assert inc.postmortem is None


def test_severity_values():
    assert Severity.SEV1.value == "SEV1"
    assert Severity.SEV2.value == "SEV2"
    assert Severity.SEV3.value == "SEV3"


def test_incident_status_values():
    assert IncidentStatus.INVESTIGATING.value == "Investigating"
    assert IncidentStatus.MITIGATING.value == "Mitigating"
    assert IncidentStatus.RESOLVED.value == "Resolved"
