# app/handlers/device_handler.py

import json
import logging
from app.gpio.controller import gpio_controller
from app.core.nats_client import nats_client
from app.core.config import settings

logger = logging.getLogger(__name__)

async def handle_device_command(msg):
    """
    Obsługuje polecenia sterowania GPIO:
    {
        "action": "SET_DEVICE_STATE",
        "data": {
            "device_id": 2,
            "gpio_pin": 17,
            "state": true
        }
    }
    """
    try:
        payload = json.loads(msg.data.decode())
        action = payload.get("action")
        data = payload.get("data", {})

        logger.info(f"📥 Received device command: {payload}")

        if action == "SET_DEVICE_STATE":
            gpio_pin = data["gpio_pin"]
            state = data["state"]

            # 🔥 BEZ CONFIG.JSON — od razu sterujemy pinem z backendu
            success = gpio_controller.direct_pin_control(gpio_pin, state)

            # wyślij ACK
            ack_msg = {
                "device_id": data["device_id"],
                "ok": success,
                "state": state
            }

            await nats_client.publish(
                f"raspberry.{settings.DEVICE_UUID}.command_ack",
                ack_msg
            )
            return

        logger.warning(f"⚠️ Unknown action: {action}")

    except Exception as e:
        logger.exception(f"❌ Error while handling device command: {e}")
