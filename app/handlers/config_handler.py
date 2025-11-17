# app/handlers/config_handler.py
import json
import logging
from pathlib import Path

from app.core.config import settings
from app.gpio.schema import GPIOConfig
from app.core.nats_client import nats_client
from app.gpio.controller import gpio_controller  # <-- WAŻNE

logger = logging.getLogger(__name__)

CONFIG_PATH = Path("config.json")


async def handle_config_update(msg):
    """
    Handler dla wiadomości NATS:
    🔹 "raspberry.<uuid>.config"
    Aktualizuje lokalny plik konfiguracyjny Raspberry (np. przypisania pinów)
    i przeładowuje GPIOController.
    """
    try:
        # Dekodowanie danych
        data = json.loads(msg.data.decode())
        logger.info(f"📦 Otrzymano nową konfigurację: {data}")

        # Walidacja Pydantic
        config = GPIOConfig(**data)

        # Zapisujemy config.json
        with open(CONFIG_PATH, "w") as f:
            json.dump(config.model_dump(), f, indent=2)

        logger.info("💾 Konfiguracja zapisana lokalnie (config.json)")

        # Przeładowanie GPIOController
        gpio_controller.load_config()
        logger.info(f"🔁 GPIOController przeładowany, nowe piny: {gpio_controller.pin_map}")

        # ACK do backendu
        ack_msg = {
            "uuid": settings.DEVICE_UUID,
            "ok": True
        }
        await nats_client.publish(f"raspberry.{settings.DEVICE_UUID}.config_ack", ack_msg)

        logger.info("📨 Wysłano ACK konfiguracji do backendu")

    except Exception as e:
        logger.exception(f"❌ Błąd przy obsłudze konfiguracji: {e}")

        # NEGATIVE ACK
        ack_msg = {
            "uuid": settings.DEVICE_UUID,
            "ok": False,
            "error": str(e)
        }
        await nats_client.publish(f"raspberry.{settings.DEVICE_UUID}.config_ack", ack_msg)
