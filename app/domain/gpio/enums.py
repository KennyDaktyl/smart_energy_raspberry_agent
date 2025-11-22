# app/domain/gpio/enums.py

from enum import Enum


class DeviceMode(str, Enum):
    MANUAL = "MANUAL"        # Sterowanie ręczne
    AUTO_POWER = "AUTO_POWER"  # Na podstawie produkcji energii
    SCHEDULE = "SCHEDULE"    # Harmonogram czasowy


class GPIODirection(str, Enum):
    OUT = "OUT"
    IN = "IN"


class GPIOState(str, Enum):
    HIGH = "HIGH"   # OFF dla przekaźników low-trigger
    LOW = "LOW"     # ON
