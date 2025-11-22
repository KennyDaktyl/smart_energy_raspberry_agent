# app/core/nats_client.py

import json
import logging
import nats
from nats.js.api import StreamConfig, RetentionPolicy

from app.core.config import settings

logger = logging.getLogger(__name__)


class NATSClient:
    def __init__(self):
        self.nc = None
        self.js = None

    async def connect(self):
        logger.info(f"Connecting to NATS: {settings.NATS_URL}")

        self.nc = await nats.connect(settings.NATS_URL)
        self.js = self.nc.jetstream()

        logger.info("Connected to NATS & JetStream")

        # tworzymy wszystkie streamy
        await self.ensure_streams()

    # ------------------------------------------------------

    async def ensure_streams(self):
        """
        Tworzy wszystkie wymagane streamy JetStream.
        """

        await self.ensure_stream(
            name="raspberry_events",
            subjects=[f"raspberry.{settings.RASPBERRY_UUID}.events"]
        )

        await self.ensure_stream(
            name="raspberry_heartbeat",
            subjects=[f"raspberry.{settings.RASPBERRY_UUID}.heartbeat"]
        )

        await self.ensure_stream(
            name="raspberry_gpio",
            subjects=[f"raspberry.{settings.RASPBERRY_UUID}.gpio_change"]
        )

    # ------------------------------------------------------

    async def ensure_stream(self, name: str, subjects: list[str]):
        """
        Tworzy stream, jeśli nie istnieje.
        """
        try:
            await self.js.stream_info(name)
            logger.info(f"Stream '{name}' already exists")
        except Exception:
            cfg = StreamConfig(
                name=name,
                subjects=subjects,
                retention=RetentionPolicy.LIMITS  # UŻYWAMY TWOJEJ WERSJI
            )
            await self.js.add_stream(cfg)
            logger.info(f"Created JetStream stream '{name}'")

    # ------------------------------------------------------

    async def publish(self, subject: str, payload):
        data = json.dumps(payload).encode()
        await self.js.publish(subject, data)

    async def subscribe_js(self, subject: str, handler):
        """
        Subskrypcja JetStream Durable Consumer.
        """
        durable = subject.replace(".", "_")

        sub = await self.js.subscribe(
            subject,
            durable=durable,
            cb=handler,
        )

        logger.info(f"Subscribed to JetStream subject: {subject}")
        return sub


nats_client = NATSClient()
