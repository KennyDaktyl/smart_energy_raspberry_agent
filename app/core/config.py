from pathlib import Path
import json
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Konfiguracja agenta Raspberry — ładowana z .env oraz config.json.
    """

    # 🔹 Kluczowe parametry identyfikujące urządzenie
    DEVICE_UUID: str = Field(..., description="Unikalny identyfikator Raspberry (UUID)")
    SECRET_KEY: str = Field(..., description="Sekretny klucz do autoryzacji z backendem")

    # 🔹 Komunikacja i serwis NATS
    NATS_URL: str = Field("nats://localhost:4222", env="NATS_URL")
    HEARTBEAT_INTERVAL: int = Field(30, env="HEARTBEAT_INTERVAL")

    # 🔹 GPIO i logowanie
    GPIO_PINS: dict = Field(default_factory=dict)
    LOG_DIR: str = Field("logs", env="LOG_DIR")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_gpio_config() -> dict:
    """
    Wczytuje konfigurację pinów GPIO z pliku config.json.
    """
    config_file = Path("config.json")
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                data = json.load(f)
                return data.get("gpio_pins", {})
        except json.JSONDecodeError:
            print("⚠️ Błąd: nieprawidłowy format pliku config.json")
    return {}


# 🔹 Inicjalizacja konfiguracji globalnej
settings = Settings()

# 🔹 Wczytanie konfiguracji pinów z pliku JSON
settings.GPIO_PINS = load_gpio_config()
