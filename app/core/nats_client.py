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
        logger.info(f"🐭 Connected to NATS at {settings.NATS_URL}")

    async def subscribe(self, subject: str, callback):
        async def wrapper(msg):
            await callback(msg)

        await self.nc.subscribe(subject, cb=wrapper)
        logger.info(f"📡 Subscribed to {subject}")

    async def publish(self, subject: str, message):
        """
        Accepts:
        - dict -> JSON convert
        - bytes -> send raw
        """
        if isinstance(message, bytes):
            data = message
        else:
            data = json.dumps(message).encode()

        await self.nc.publish(subject, data)
        logger.info(f"📤 Published to {subject}: {message}")

nats_client = NatsClient()
