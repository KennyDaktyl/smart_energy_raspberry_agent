# app/infrastructure/gpio/gpio_manager.py

import logging
from typing import Dict, Any, List
from app.infrastructure.gpio.gpio_controller import gpio_controller
from app.core.config import settings
from app.core.nats_client import nats_client

logger = logging.getLogger(__name__)


class GPIOManager:
    """
    Monitoruje stany pinów, wykrywa zmiany i wysyła eventy o zmianach.
    """

    def __init__(self):
        self.devices = {}          # device_id → GPIODevice
        self.previous_states = {}  # pin → last state

    # ----------------------------------------
    # Ładowanie urządzeń z listy domenowej
    # ----------------------------------------
    def load_devices(self, devices):
        self.devices = {str(d.device_id): d for d in devices}

        # reset poprzednich stanów
        self.previous_states = {
            d.pin_number: None for d in devices
        }

        logger.info(f"GPIOManager: loaded {len(devices)} devices")

    # ----------------------------------------
    # Odczyt stanów
    # ----------------------------------------
    def get_states(self) -> Dict[int, int]:
        states = {}
        for device in self.devices.values():
            pin = device.pin_number
            value = gpio_controller.read_pin(pin)
            states[pin] = value
        return states

    # ----------------------------------------
    # Dane do heartbeat
    # ----------------------------------------
    def get_devices_status(self) -> List[Dict[str, Any]]:
        states = self.get_states()

        return [
            {
                "device_id": d.device_id,
                "pin": d.pin_number,
                "is_on": states[d.pin_number] == 0,  # LOW = ON
                "mode": d.mode,
                "threshold": d.power_threshold_w,
            }
            for d in self.devices.values()
        ]

    # ----------------------------------------
    # Detekcja zmian
    # ----------------------------------------
    async def detect_changes(self):
        current = self.get_states()

        for pin, new_state in current.items():
            old_state = self.previous_states.get(pin)

            # pierwsze odczytanie – brak zmian
            if old_state is None:
                self.previous_states[pin] = new_state
                continue

            if new_state != old_state:
                logger.info(
                    f"GPIO change detected on pin {pin}: {old_state} → {new_state}"
                )
                await self.send_change_event(pin, new_state)

            self.previous_states[pin] = new_state

    # ----------------------------------------
    # Wysyłanie eventu zmiany
    # ----------------------------------------
    async def send_change_event(self, pin: int, value: int):
        payload = {
            "uuid": settings.RASPBERRY_UUID,
            "pin": pin,
            "state": bool(value == 0),  # LOW = ON
        }
        subject = f"raspberry.{settings.RASPBERRY_UUID}.gpio_change"

        await nats_client.publish(subject, payload)

        logger.info(f"Sent gpio_change event: {payload}")


gpio_manager = GPIOManager()
