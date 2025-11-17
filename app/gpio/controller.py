# app/gpio/controller.py

import json
import logging
from pathlib import Path

# -------------------------------------------------------------------
#  GPIO or Mock
# -------------------------------------------------------------------
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    class MockGPIO:
        BCM = "BCM"
        OUT = "OUT"
        LOW = "LOW"
        HIGH = "HIGH"

        @staticmethod
        def setmode(mode):
            print(f"[MOCK GPIO] setmode({mode})")

        @staticmethod
        def setup(pin, mode):
            print(f"[MOCK GPIO] setup(pin={pin}, mode={mode})")

        @staticmethod
        def output(pin, state):
            print(f"[MOCK GPIO] output(pin={pin}, state={state})")

    GPIO = MockGPIO()

logger = logging.getLogger(__name__)

CONFIG_PATH = Path("config.json")


# -------------------------------------------------------------------
#  GPIO Controller
# -------------------------------------------------------------------
class GPIOController:
    def __init__(self):
        self.pin_map = {}  # device_id → gpio_pin
        GPIO.setmode(GPIO.BCM)
        logger.info("🔌 GPIOController initialized")

    # ---------------------------------------------------------------
    #  Optional config.json loading (NOT REQUIRED)
    # ---------------------------------------------------------------
    def load_config(self):
        """Wczytuje config.json jeśli istnieje (mapowanie device_id → pin)."""
        if not CONFIG_PATH.exists():
            logger.warning("⚠️ config.json not found — no pin mapping loaded")
            return

        try:
            with open(CONFIG_PATH) as f:
                data = json.load(f)

            self.pin_map = {str(d["device_id"]): d["gpio_pin"] for d in data["pins"]}

            # inicjalizacja pinów
            for pin in self.pin_map.values():
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)

            logger.info(f"🔌 GPIO config loaded: {self.pin_map}")

        except Exception as e:
            logger.exception(f"❌ Error loading config.json: {e}")

    # ---------------------------------------------------------------
    #  NEW — direct pin control (backend sends gpio_pin)
    # ---------------------------------------------------------------
    def direct_pin_control(self, gpio_pin: int, state: bool):
        """
        Sterowanie bezpośrednio pinek GPIO wysłanym przez backend.
        """
        try:
            GPIO.setup(gpio_pin, GPIO.OUT)
            GPIO.output(gpio_pin, GPIO.HIGH if state else GPIO.LOW)

            logger.info(
                f"⚡ Direct GPIO control pin={gpio_pin} → {'ON' if state else 'OFF'}"
            )
            return True

        except Exception as e:
            logger.exception(f"❌ GPIO error on pin {gpio_pin}: {e}")
            return False

    # ---------------------------------------------------------------
    # Optional OLD method — only if using config.json
    # ---------------------------------------------------------------
    def set_state(self, device_id: int, state: bool):
        """
        Sterowanie na podstawie device_id → pin_map (tylko gdy config.json istnieje).
        """
        pin = self.pin_map.get(str(device_id))
        if pin is None:
            logger.error(f"❌ No pin mapped for device_id={device_id}")
            return False

        try:
            GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
            logger.info(
                f"🟢 GPIO mapped control device_id={device_id}, pin={pin} → {'ON' if state else 'OFF'}"
            )
            return True

        except Exception as e:
            logger.exception(f"❌ GPIO error on mapped pin {pin}: {e}")
            return False


# -------------------------------------------------------------------
#  Singleton instance
# -------------------------------------------------------------------
gpio_controller = GPIOController()
