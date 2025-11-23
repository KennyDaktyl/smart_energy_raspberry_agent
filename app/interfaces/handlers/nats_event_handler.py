import json
import logging

from app.domain.events.device_events import (
    DeviceCreatedEvent,
    DeviceUpdatedEvent,
    PowerReadingEvent,
    DeviceCommandEvent,
    EventType
)
from app.core.config import settings
from app.application.event_service import event_service
from smart_energy_raspberry_agent.app.core.nats_client import NATSClient

logger = logging.getLogger(__name__)


nats_client = NATSClient()


async def nats_event_handler(msg):
    try:
        raw = json.loads(msg.data.decode())
        event_type = raw.get("event_type")

        logger.info(f"Received raw event: {raw}")

        match event_type:
            case EventType.DEVICE_CREATED:
                event = DeviceCreatedEvent(**raw)

            case EventType.DEVICE_UPDATED:
                event = DeviceUpdatedEvent(**raw)

            case EventType.POWER_READING:
                event = PowerReadingEvent(**raw)

            case EventType.DEVICE_COMMAND:
                event = DeviceCommandEvent(**raw)

            case _:
                logger.error(f"Unknown event type: {event_type}")
                return

        # wykonaj logikę
        await event_service.handle_event(event)

        # JetStream ACK
        await msg.ack()
        logger.info("JetStream ACK sent.")

        # ------------------------------------------------------
        # BACKEND ACK (TO JEST TO, CZEGO OCZEKUJE BACKEND)
        # ------------------------------------------------------
        ack_subject = f"raspberry.{settings.RASPBERRY_UUID}.events.ack"

        ack_payload = {
            "device_id": event.payload.device_id,
            "ok": True
        }

        await nats_client.nc.publish(ack_subject, json.dumps(ack_payload).encode())
        logger.info(f"✔ Backend ACK sent: {ack_payload}")

    except Exception as e:
        logger.exception(f"Error while handling event: {e}")
        return


