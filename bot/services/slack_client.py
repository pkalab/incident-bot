import os
from typing import Optional

from slack_sdk import WebClient

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))


def create_war_room(channel_name: str, topic: str) -> Optional[str]:
    resp = client.conversations_create(name=channel_name, is_private=False)
    channel_id = resp["channel"]["id"]
    client.conversations_setTopic(channel=channel_id, topic=topic)
    return channel_id


def post_message(channel_id: str, text: str, thread_ts: Optional[str] = None) -> str:
    resp = client.chat_postMessage(channel=channel_id, text=text, thread_ts=thread_ts)
    return resp["ts"]


def update_topic(channel_id: str, topic: str) -> None:
    client.conversations_setTopic(channel=channel_id, topic=topic)
