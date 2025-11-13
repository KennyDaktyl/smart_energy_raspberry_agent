from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class DeviceMode(str, Enum):
    """Tryby pracy urządzenia przypisanego do GPIO."""
    MANUAL = "MANUAL"           # Sterowanie ręczne (ON/OFF)
    AUTO_POWER = "AUTO_POWER"   # Automatyczne na podstawie mocy PV
    SCHEDULE = "SCHEDULE"       # Harmonogram czasowy


class GPIODirection(str, Enum):
    """Kierunek pinu GPIO."""
    OUT = "OUT"
    IN = "IN"


class GPIOState(str, Enum):
    """Stan logiczny pinu."""
    HIGH = "HIGH"
    LOW = "LOW"


class GPIOPinConfig(BaseModel):
    """
    Konfiguracja pojedynczego pinu GPIO.
    """
    device_id: int = Field(..., description="ID urządzenia z backendu")
    pin_number: int = Field(..., description="Numer pinu GPIO (BCM)")
    direction: GPIODirection = Field(default=GPIODirection.OUT)
    mode: DeviceMode = Field(default=DeviceMode.MANUAL)
    default_state: GPIOState = Field(default=GPIOState.LOW)
    power_threshold_w: Optional[float] = Field(
        None, description="Próg mocy PV (dla AUTO_POWER)"
    )
    name: Optional[str] = Field(None, description="Przyjazna nazwa urządzenia")


class GPIOConfig(BaseModel):
    """
    Główna konfiguracja wszystkich pinów na Raspberry Pi.
    """
    device_uuid: str = Field(..., description="Unikalny UUID urządzenia Raspberry")
    pins: list[GPIOPinConfig] = Field(default_factory=list)
