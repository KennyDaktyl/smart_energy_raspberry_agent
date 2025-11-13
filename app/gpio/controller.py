import logging
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
            pass

        @staticmethod
        def setup(pin, mode):
            pass

        @staticmethod
        def output(pin, state):
            pass

    GPIO = MockGPIO  # fallback

logger = logging.getLogger(__name__)


class GPIOController:
    def __init__(self, pin_map: dict):
        self.pin_map = pin_map
        GPIO.setmode(GPIO.BCM)
        for pin in self.pin_map.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        logger.info(f"🔌 GPIO initialized: {self.pin_map}")

    def set_state(self, device_id: int, state: bool):
        pin = self.pin_map.get(str(device_id))
        if pin is None:
            logger.error(f"No GPIO pin for device {device_id}")
            return False
        GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
        logger.info(f"GPIO pin {pin} set to {'ON' if state else 'OFF'}")
        return True

gpio_controller = GPIOController(pin_map={})
