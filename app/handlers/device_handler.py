# app/handlers/device_handler.py

import json
import logging
from app.gpio.controller import gpio_controller
from app.core.nats_client import nats_client
from app.core.config import settings

logger = logging.getLogger(__name__)

async def handle_device_command(msg):
    try:
        payload = json.loads(msg.data.decode())
        action = payload.get("action")
        data = payload.get("data", {})

        logger.info(f"📥 Received device command: {payload}")

        if action == "SET_DEVICE_STATE":
            gpio_pin = data["gpio_pin"]
            state = data["state"]

            logger.info(f"🔧 Executing SET_DEVICE_STATE on pin {gpio_pin}")

            success = gpio_controller.direct_pin_control(gpio_pin, state)

            ack_msg = {
                "device_id": data["device_id"],
                "ok": success,
                "state": state,
            }

            topic = f"raspberry.{settings.DEVICE_UUID}.ack"
            logger.info(f"📨 Sending ACK to {topic}: {ack_msg}")

            # NATS expects bytes, so encode JSON
            await nats_client.publish(
                topic,
                json.dumps(ack_msg).encode()
            )

            logger.info("✅ ACK sent successfully!")

        else:
            logger.warning(f"⚠️ Unknown action: {action}")

    except Exception as e:
        logger.exception(f"❌ Error while handling device command: {e}")
