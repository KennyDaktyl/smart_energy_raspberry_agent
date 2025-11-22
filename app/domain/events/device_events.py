from pydantic import BaseModel
from enum import Enum
from typing import Optional, List


class EventType(str, Enum):
    DEVICE_CREATED = "DEVICE_CREATED"
    DEVICE_UPDATED = "DEVICE_UPDATED"
    POWER_READING = "POWER_READING"
    DEVICE_COMMAND = "DEVICE_COMMAND"
    UPDATE_REQUEST = "UPDATE_REQUEST"


class BaseEvent(BaseModel):
    event_type: EventType


class DeviceCreatedPayload(BaseModel):
    device_id: int
    device_number: int        # 1..3
    mode: str
    threshold_w: Optional[float] = None


class DeviceCreatedEvent(BaseEvent):
    payload: DeviceCreatedPayload


class DeviceUpdatedPayload(BaseModel):
    device_id: int
    mode: str
    threshold_w: Optional[float] = None


class DeviceUpdatedEvent(BaseEvent):
    payload: DeviceUpdatedPayload


class DeviceDeletePayload(BaseModel):
    device_id: int


class PowerReadingPayload(BaseModel):
    inverter_id: int
    power_w: float
    device_ids: List[int]


class PowerReadingEvent(BaseEvent):
    payload: PowerReadingPayload


class DeviceCommandPayload(BaseModel):
    device_id: int
    command: str
    is_on: bool


class DeviceCommandEvent(BaseEvent):
    payload: DeviceCommandPayload
