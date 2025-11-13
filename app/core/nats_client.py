# app/core/nats_client.py
import json
import logging
from nats.aio.client import Client as NATS
from app.core.config import settings

logger = logging.getLogger(__name__)

class NatsClient:
    def __init__(self):
        self.nc = NATS()

    async def connect(self):
        await self.nc.connect(settings.NATS_URL)
        logger.info(f"✅ Connected to NATS at {settings.NATS_URL}")

    async def subscribe(self, subject: str, callback):
        await self.nc.subscribe(subject, cb=callback)
        logger.info(f"📡 Subscribed to {subject}")

    async def publish(self, subject: str, message: dict):
        data = json.dumps(message).encode()
        await self.nc.publish(subject, data)
        logger.debug(f"📤 Published to {subject}: {message}")

nats_client = NatsClient()
