import os
from datetime import datetime
from typing import Optional

import boto3
from boto3.dynamodb.conditions import Key

from bot.models.incident import Incident, IncidentStatus

TABLE_NAME = os.getenv("DYNAMODB_TABLE", "incidents")


class IncidentStore:
    def __init__(self):
        self.table = boto3.resource("dynamodb").Table(TABLE_NAME)

    def put_incident(self, incident: Incident) -> None:
        self.table.put_item(Item=incident.model_dump())

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        resp = self.table.get_item(Key={"incident_id": incident_id})
        item = resp.get("Item")
        return Incident(**item) if item else None

    def get_active_incidents(self) -> list[Incident]:
        resp = self.table.query(
            IndexName="status-index",
            KeyConditionExpression=Key("status").eq(IncidentStatus.INVESTIGATING.value),
        )
        return [Incident(**item) for item in resp.get("Items", [])]

    def update_status(self, incident_id: str, status: IncidentStatus) -> None:
        self.table.update_item(
            Key={"incident_id": incident_id},
            UpdateExpression="SET #s = :s, resolved_at = :r",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":s": status.value,
                ":r": datetime.now().isoformat() if status == IncidentStatus.RESOLVED else None,
            },
        )
