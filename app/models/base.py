from datetime import datetime
from uuid import uuid4

from beanie import Replace, before_event
from beanie.odm.utils.parsing import merge_models
from pydantic import BaseModel, Field, PositiveFloat

Timestamp = PositiveFloat


class BaseDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    @property
    def _id(self):
        return self.id

    async def sync(self):
        result = await self.find_one({"_id": self.id})
        merge_models(self, result)
        return self

    class Settings:
        validate_on_save = True
        use_revision = True
        use_state_management = True


class TimestampedDocument(BaseDocument):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @before_event(Replace)
    def updated_at_change(self):
        self.updated_at = datetime.utcnow()
