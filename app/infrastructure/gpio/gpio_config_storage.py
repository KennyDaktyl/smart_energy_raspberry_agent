# app/infrastructure/gpio/gpio_config_storage.py

import json
from pathlib import Path
from typing import List
from app.domain.gpio.entities import GPIODevice


class GPIOConfigStorage:
    CONFIG_PATH = Path("config.json")

    def load(self) -> List[GPIODevice]:
        """Wczytuje konfigurację z pliku config.json → modele GPIODevice."""
        if not self.CONFIG_PATH.exists():
            return []

        with open(self.CONFIG_PATH) as f:
            data = json.load(f)

        pins = data.get("pins", [])
        return [GPIODevice(**p) for p in pins]

    def save(self, devices: List[GPIODevice]):
        """Zapisuje listę GPIODevice do config.json."""
        content = {
            "pins": [device.model_dump() for device in devices]
        }

        with open(self.CONFIG_PATH, "w") as f:
            json.dump(content, f, indent=2)


gpio_config_storage = GPIOConfigStorage()
