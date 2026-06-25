from slack_bolt import Ack
from slack_bolt.context.respond import Respond

from bot.models.incident import IncidentStatus, IncidentStore
from bot.services.slack_client import post_message, update_topic

store = IncidentStore()

VALID_STATUSES = {s.value.lower(): s for s in IncidentStatus}


def handle_status(ack: Ack, command: dict, respond: Respond) -> None:
    ack()
    text = command["text"].strip().lower()

    active = store.get_active_incidents()
    if not active:
        respond("No active incident.")
        return

    inc = active[0]

    if not text:
        respond(f"Current status: *{inc.status.value}*\nValid values: Investigating, Mitigating, Resolved")
        return

    new_status = VALID_STATUSES.get(text)
    if not new_status:
        respond(f"Invalid status `{text}`. Valid: Investigating, Mitigating, Resolved")
        return

    store.update_status(inc.id, new_status)
    topic = f"[{inc.severity.value}] {inc.title} — {new_status.value}"
    update_topic(inc.channel_id, topic)
    post_message(inc.channel_id, f":arrow_right: Status updated to *{new_status.value}*")
    respond(f"Status updated to *{new_status.value}*")
