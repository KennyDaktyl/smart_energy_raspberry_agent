# app/gpio/controller.py

import json
import logging
from pathlib import Path

# -------------------------------------------------------------------
#  GPIO or Mock (na PC lub Docker)
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
        def setwarnings(flag):
            print(f"[MOCK GPIO] setwarnings({flag})")

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
    """
    Kontroler GPIO dla Raspberry Pi z logiką LOW = ON, HIGH = OFF,
    kompatybilny z modułami przekaźników low-trigger.
    """

    def __init__(self):
        self.pin_map = {}  # optional: device_id → gpio_pin

        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
        except Exception as e:
            logger.error(f"⚠️ GPIO init error: {e}")

        logger.info("🔌 GPIOController initialized (LOW=ON, HIGH=OFF)")

    # ---------------------------------------------------------------
    # Optional: load config.json (jeśli backend wyśle)
    # ---------------------------------------------------------------
    def load_config(self):
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
                GPIO.output(pin, GPIO.HIGH)   # domyślnie OFF

            logger.info(f"🔌 GPIO config loaded: {self.pin_map}")

        except Exception as e:
            logger.exception(f"❌ Error loading config.json: {e}")

    # ---------------------------------------------------------------
    # ⭐ NEW — BEZPOŚREDNIE STEROWANIE PINEM (z backendu)
    # ---------------------------------------------------------------
    def direct_pin_control(self, gpio_pin: int, state: bool):
        """
        Steruje bezpośrednio pinem GPIO:
        - LOW  = ON
        - HIGH = OFF

        Idealne do przekaźników low-trigger.
        """
        try:
            GPIO.setup(gpio_pin, GPIO.OUT)

            # 🔥 Najważniejsza część — stara logika twojego systemu!
            gpio_state = GPIO.LOW if state else GPIO.HIGH

            GPIO.output(gpio_pin, gpio_state)

            logger.info(
                f"⚡ Direct GPIO control pin={gpio_pin} → "
                f"{'ON (LOW)' if state else 'OFF (HIGH)'}"
            )
            return True

        except Exception as e:
            logger.exception(f"❌ GPIO error on pin {gpio_pin}: {e}")
            return False

    # ---------------------------------------------------------------
    # Optional OLD method — jeśli ktoś użyje device_id
    # ---------------------------------------------------------------
    def set_state(self, device_id: int, state: bool):
        """
        Sterowanie wg config.json (device_id → pin).
        """
        pin = self.pin_map.get(str(device_id))
        if pin is None:
            logger.error(f"❌ No pin mapped for device_id={device_id}")
            return False

        try:
            gpio_state = GPIO.LOW if state else GPIO.HIGH
            GPIO.output(pin, gpio_state)

            logger.info(
                f"🟢 GPIO mapped control device_id={device_id}, pin={pin} → "
                f"{'ON' if state else 'OFF'}"
            )

            return True

        except Exception as e:
            logger.exception(f"❌ GPIO error on mapped pin {pin}: {e}")
            return False


# -------------------------------------------------------------------
#  GLOBAL SINGLETON — używany przez device_handler
# -------------------------------------------------------------------
gpio_controller = GPIOController()
