# app/core/heartbeat.py
import asyncio
import logging
from app.core.nats_client import nats_client
from app.core.config import settings

logger = logging.getLogger(__name__)

async def send_heartbeat():
    while True:
        payload = {
            "uuid": settings.DEVICE_UUID,
            "status": "online",
            "timestamp": asyncio.get_event_loop().time()
        }
        await nats_client.publish("raspberry.heartbeat", payload)
        logger.info(f"Heartbeat sent. Payload: {payload}")
        await asyncio.sleep(settings.HEARTBEAT_INTERVAL)
 