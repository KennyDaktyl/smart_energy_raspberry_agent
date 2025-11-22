import json
import logging

from app.domain.events.device_events import (
    DeviceCreatedEvent,
    DeviceUpdatedEvent,
    PowerReadingEvent,
    DeviceCommandEvent,
    EventType
)

from app.application.event_service import event_service

logger = logging.getLogger(__name__)


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

        await event_service.handle_event(event)

        await msg.ack()
        logger.info("ACK sent after successful processing.")

    except Exception as e:
        logger.exception(f"Error while handling event: {e}")
        return

