from pydantic import BaseModel
from typing import Optional
from app.domain.gpio.enums import DeviceMode


class GPIODevice(BaseModel):
    """
    Lokalna reprezentacja urządzenia na Raspberry.
    Przechowuje WYŁĄCZNIE to, czego potrzebuje RPi.
    """

    device_id: int
    pin_number: int
    mode: DeviceMode
    power_threshold_w: Optional[float]
