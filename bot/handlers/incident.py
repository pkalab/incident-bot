import re
from datetime import datetime

from slack_bolt import Ack
from slack_bolt.context.say import Say
from slack_bolt.context.respond import Respond

from bot.models.incident import Incident, IncidentStatus, Severity
from bot.services.dynamo import IncidentStore
from bot.services.slack_client import create_war_room, post_message, update_topic

store = IncidentStore()


def get_next_id() -> str:
    today = datetime.now().strftime("%Y%m%d")
    existing = store.get_active_incidents()
    count = len([i for i in existing if i.id.startswith(f"inc-{today}")]) + 1
    return f"inc-{today}-{count:03d}"


def parse_severity(text: str) -> Severity:
    match = re.search(r"(SEV[123])", text.upper())
    return Severity(match.group(1)) if match else Severity.SEV2


def handle_incident(ack: Ack, command: dict, say: Say, respond: Respond) -> None:
    ack()
    text = command["text"].strip()
    user_id = command["user_id"]
    user_name = command.get("user_name", user_id)

    if text.lower() == "resolve":
        active = store.get_active_incidents()
        if not active:
            respond("No active incidents to resolve.")
            return
        inc = active[0]
        store.update_status(inc.id, IncidentStatus.RESOLVED)
        update_topic(inc.channel_id, f"[RESOLVED] {inc.title}")
        post_message(inc.channel_id, f":white_check_mark: Incident resolved by @{user_name}")
        respond(f"Incident {inc.id} resolved. Run `/postmortem` to document.")
        return

    incident_id = get_next_id()
    severity = parse_severity(text)
    title = re.sub(r"\s*\(?SEV[123]\)?", "", text, flags=re.IGNORECASE).strip()

    channel_name = f"inc-{incident_id.split('-', 1)[1]}"
    channel_id = create_war_room(
        channel_name=channel_name,
        topic=f"[{severity.value}] {title} — Investigating",
    )

    inc = Incident(
        id=incident_id,
        title=title,
        severity=severity,
        status=IncidentStatus.INVESTIGATING,
        channel_id=channel_id,
        declared_by=user_id,
        declared_at=datetime.now(),
    )
    store.put_incident(inc)

    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f":rotating_light: {title}"}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*ID:*\n{incident_id}"},
            {"type": "mrkdwn", "text": f"*Severity:*\n{severity.value}"},
            {"type": "mrkdwn", "text": f"*Declared by:*\n<@{user_id}>"},
            {"type": "mrkdwn", "text": "*Status:*\nInvestigating"},
        ]},
        {"type": "section", "text": {"type": "mrkdwn", "text": ":clipboard: *Next steps:*\n• Run `/playbook` to diagnose\n• Update `/status`\n• Resolve with `/incident resolve`"}},
    ]
    post_message(channel_id, text="", blocks=blocks)
    respond(f":tada: War room created: <#{channel_id}>")
