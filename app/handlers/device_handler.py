import json
import logging
from app.gpio.controller import gpio_controller
from app.core.config import settings
from app.core.nats_client import nats_client
from app.handlers.utils import safe_ack

logger = logging.getLogger(__name__)


async def handle_device_command(msg):
    """
    Handler dla wiadomości:
    🔹 "raspberry.<uuid>.command"
    """
    try:
        data = json.loads(msg.data.decode())
        action = data.get("action")
        payload = data.get("data", {})
        logger.info(f"⚡ Otrzymano komendę: {action} → {payload}")

        if action == "SET_DEVICE_STATE":
            device_id = payload.get("device_id")
            state = payload.get("state", False)

            # ok = gpio_controller.set_state(device_id, state)
            ok = 1
            await safe_ack(
                subject=f"raspberry.{settings.DEVICE_UUID}.ack",
                message={"device_id": device_id, "ok": ok, "state": state},
            )

        elif action == "PING":
            await safe_ack(
                subject=f"raspberry.{settings.DEVICE_UUID}.ack",
                message={"type": "PING", "ok": True},
            )

        else:
            logger.warning(f"⚠️ Nieznana komenda: {action}")
            await safe_ack(
                subject=f"raspberry.{settings.DEVICE_UUID}.ack",
                message={"ok": False, "error": f"Unknown action: {action}"},
            )

    except Exception as e:
        logger.exception(f"❌ Błąd w obsłudze komendy urządzenia: {e}")
        await safe_ack(
            subject=f"raspberry.{settings.DEVICE_UUID}.ack",
            message={"ok": False, "error": str(e)},
        )
