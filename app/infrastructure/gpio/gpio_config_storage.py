import json
from pathlib import Path
from typing import List
from app.domain.gpio.entities import GPIODevice


class GPIOConfigStorage:
    CONFIG_PATH = Path("config.json")

    def load_raw(self) -> dict:
        """Wczytuje pełny config jako dict."""
        if not self.CONFIG_PATH.exists():
            return {}
        try:
            with open(self.CONFIG_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def load(self) -> List[GPIODevice]:
        """Wczytuje tylko listę pins."""
        data = self.load_raw()
        pins = data.get("pins", [])
        return [GPIODevice(**p) for p in pins]

    def save(self, devices: List[GPIODevice]):
        """
        Zapisuje tylko sekcję 'pins', zachowując resztę konfiguracji.
        """
        data = self.load_raw()

        data["pins"] = [device.model_dump() for device in devices]

        with open(self.CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=2)


gpio_config_storage = GPIOConfigStorage()
