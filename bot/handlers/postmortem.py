from datetime import datetime

from slack_bolt import Ack
from slack_bolt.context.respond import Respond

from bot.models.incident import IncidentStore, Postmortem, TimelineEvent
from bot.services.slack_client import post_message

store = IncidentStore()


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

    duration = ""
    if inc.resolved_at:
        delta = inc.resolved_at - inc.declared_at
        duration = f"{delta.total_seconds() / 60:.0f} minutes"

    timeline_lines = "\n".join(
        f"- **{e.timestamp}** — {e.event} (by {e.actor})" for e in pm.timeline
    )
    causes_lines = "\n".join(f"- {c}" for c in pm.root_causes)
    items_lines = "\n".join(f"- [ ] {i}" for i in pm.action_items)

    rendered = f"""# Postmortem: {inc.id}

**Title:** {inc.title}
**Severity:** {inc.severity.value}
**Date:** {inc.declared_at.isoformat()}
**Duration:** {duration}

## Summary

{summary}

## Timeline

{timeline_lines}

## Root Causes (5 Whys)

{causes_lines}

## Action Items

{items_lines}
"""

    post_message(
        inc.channel_id,
        f":memo: *Postmortem: {inc.id}*\n```{rendered}```",
    )

    inc.postmortem = pm
    store.put_incident(inc)
    respond("Postmortem created and posted to war room.")
