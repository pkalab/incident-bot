import os
from datetime import datetime

from jinja2 import Template
from slack_bolt import Ack
from slack_bolt.context.respond import Respond

from bot.models.incident import IncidentStore, Postmortem, TimelineEvent
from bot.services.slack_client import post_message

store = IncidentStore()

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "templates", "postmortem.md")


def handle_postmortem(ack: Ack, command: dict, respond: Respond) -> None:
    ack()
    active = store.get_active_incidents()
    resolved = [i for i in active if i.status.value == "Resolved"]

    if not resolved:
        respond("No resolved incidents found. Resolve one with `/incident resolve` first.")
        return

    inc = resolved[0]
    text = command["text"].strip()
    parts = text.split("|")
    summary = parts[0].strip() if parts else "No summary provided"

    pm = Postmortem(
        summary=summary,
        timeline=[TimelineEvent(timestamp=inc.declared_at, event="Incident declared", actor=inc.declared_by)],
        root_causes=["TBD — investigate further"],
        action_items=["TBD — add action items"],
        created_at=datetime.now(),
    )

    with open(TEMPLATE_PATH) as f:
        template = Template(f.read())

    duration = ""
    if inc.resolved_at:
        delta = inc.resolved_at - inc.declared_at
        duration = f"{delta.total_seconds() / 60:.0f} minutes"

    rendered = template.render(
        incident_id=inc.id,
        title=inc.title,
        severity=inc.severity.value,
        declared_at=inc.declared_at.isoformat(),
        duration=duration,
        summary=summary,
        timeline=[e.model_dump() for e in pm.timeline],
        root_causes=pm.root_causes,
        action_items=pm.action_items,
    )

    post_message(
        inc.channel_id,
        f":memo: *Postmortem: {inc.id}*\n```{rendered}```",
    )

    inc.postmortem = pm
    store.put_incident(inc)
    respond("Postmortem created and posted to war room.")
