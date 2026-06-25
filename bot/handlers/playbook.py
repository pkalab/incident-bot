from slack_bolt import Ack
from slack_bolt.context.respond import Respond

from bot.models.incident import IncidentStore
from bot.services.playbook_runner import list_playbooks, run_playbook
from bot.services.slack_client import post_message

store = IncidentStore()


def handle_playbook(ack: Ack, command: dict, respond: Respond) -> None:
    ack()
    name = command["text"].strip()

    if not name:
        available = ", ".join(list_playbooks())
        respond(f"Usage: `/playbook <name>`\nAvailable: {available}")
        return

    active = store.get_active_incidents()
    if not active:
        respond("No active incident. Declare one with `/incident` first.")
        return

    inc = active[0]
    respond(f":gear: Running `{name}` playbook...")

    result = run_playbook(name)
    if result is None:
        respond(f"Unknown playbook `{name}`. Available: {', '.join(list_playbooks())}")
        return

    icon = {":white_check_mark:": "pass", ":warning:": "warn", ":x:": "fail"}
    status_icon = [k for k, v in icon.items() if v == result.status][0]

    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": f"{status_icon} *Playbook:* {name}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Result:* {result.summary}"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"```{result.details}```"}},
    ]
    post_message(inc.channel_id, text="", blocks=blocks)

    inc.playbook_results.append(result)
    store.put_incident(inc)
