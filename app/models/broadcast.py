from datetime import datetime
from typing import Any

from beanie import Document, Indexed

from app.types.messages import Message
from app.models.base import TimestampedDocument


class Broadcast(TimestampedDocument, Document):
    machine_id: Indexed(str)  # type: ignore
    external_id: Indexed(str)  # type: ignore
    message: Message
    phones: list[str]
    status: str = "pending"
    use_click_tracking: bool
    triggers: list[Any] | None = None
    send_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    canceled_at: datetime | None = None

    paused_at: datetime | None = None
    paused_reason: str | None = None

    webhook_status_url: str | None = None
    delayed_message: int | None = None


__beanie_models__ = [Broadcast]
