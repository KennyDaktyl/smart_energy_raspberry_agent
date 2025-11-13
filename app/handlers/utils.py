import logging
from app.core.nats_client import nats_client

logger = logging.getLogger(__name__)


async def safe_ack(subject: str, message: dict):
    """
    Wysyła bezpiecznie ACK do backendu.
    Nie przerywa programu w razie błędu sieci/NATS.
    """
    try:
        await nats_client.publish(subject, message)
        logger.debug(f"📤 ACK → {subject}: {message}")
    except Exception as e:
        logger.error(f"⚠️ Nie udało się wysłać ACK na {subject}: {e}")


def format_power(value: float) -> str:
    """Formatowanie mocy (dla logów)."""
    if value is None:
        return "—"
    if value < 1:
        return f"{value * 1000:.0f} W"
    return f"{value:.2f} kW"
