from pydantic import BaseModel
from typing import Optional

from app.domain.gpio.enums import DeviceMode


class Device(BaseModel):
    """
    Główny model urządzenia znany backendowi.
    Raspberry Agent widzi dane wyłącznie przez eventy NATS.
    """

    id: int
    name: str
    user_id: int               
    device_number: int
    mode: DeviceMode = DeviceMode.MANUAL
    power_threshold_w: Optional[float] = None
    inverter_id: Optional[int] = None
    raspberry_uuid: Optional[str] = None

    class Config:
        from_attributes = True
