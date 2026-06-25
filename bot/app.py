import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from bot.handlers.incident import handle_incident
from bot.handlers.playbook import handle_playbook
from bot.handlers.postmortem import handle_postmortem
from bot.handlers.status import handle_status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)

app.command("/incident")(handle_incident)
app.command("/playbook")(handle_playbook)
app.command("/postmortem")(handle_postmortem)
app.command("/status")(handle_status)


def main():
    logger.info("Starting Incident Response Bot...")
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()


if __name__ == "__main__":
    main()
