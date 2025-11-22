# app/core/heartbeat.py

import asyncio
import logging
from typing import Any, Dict, List

from app.core.config import settings
from app.core.nats_client import nats_client
from app.infrastructure.gpio.gpio_manager import gpio_manager

logger = logging.getLogger(__name__)


async def send_heartbeat() -> None:
    """
    Wysyła heartbeat do backendu wraz ze stanem GPIO i urządzeń.
    """

    # dajemy czas na inicjalizację GPIO/NATS
    await asyncio.sleep(1)

    while True:
        try:
            # Odczyt stanów GPIO
            gpio_states: Dict[int, int] = gpio_manager.get_states()

            # Status urządzeń (dane domenowe)
            device_status: List[Dict[str, Any]] = gpio_manager.get_devices_status()

            payload = {
                "uuid": settings.RASPBERRY_UUID,
                "status": "online",
                "timestamp": asyncio.get_event_loop().time(),
                "gpio": gpio_states,
                "devices": device_status,
            }

            subject = f"raspberry.{settings.RASPBERRY_UUID}.heartbeat"
            await nats_client.publish(subject, payload)

            logger.info(f"Heartbeat sent: {payload}")

        except Exception as e:
            logger.exception(f"Heartbeat error: {e}")

        await asyncio.sleep(settings.HEARTBEAT_INTERVAL)
