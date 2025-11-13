import sys
from pathlib import Path

# 🔧 Naprawa importów, gdy uruchamiasz "python app/main.py"
sys.path.append(str(Path(__file__).resolve().parent.parent))

import asyncio
import logging
from app.core.config import settings
from app.core.nats_client import nats_client
from app.handlers.device_handler import handle_device_command
from app.handlers.config_handler import handle_config_update
from app.core.heartbeat import send_heartbeat


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


async def main():
    await nats_client.connect()

    # Subskrypcje
    await nats_client.subscribe(f"raspberry.{settings.DEVICE_UUID}.command", handle_device_command)
    await nats_client.subscribe(f"raspberry.{settings.DEVICE_UUID}.config", handle_config_update)

    # Uruchom heartbeat
    asyncio.create_task(send_heartbeat())

    logging.info("🚀 Raspberry Agent started and listening for commands...")
    await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
