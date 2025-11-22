from enum import Enum
from pydantic import BaseModel
from typing import Optional


class EventType(str, Enum):
    DEVICE_CREATED = "DEVICE_CREATED"
    DEVICE_UPDATED = "DEVICE_UPDATED"
    POWER_READING = "POWER_READING"
    CONFIG_UPDATED = "CONFIG_UPDATED"
    DEVICE_COMMAND = "DEVICE_COMMAND"
