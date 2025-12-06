from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.domain.events.enums import EventType


class InverterProductionPayload(BaseModel):
    inverter_id: int
    serial_number: str
    active_power: Optional[float] = None
    status: str
    timestamp: datetime
    error_message: Optional[str] = None


class InverterProductionEvent(BaseModel):
    event_type: EventType
    payload: InverterProductionPayload
