from gpiozero import Button
from rpi_ws281x import Adafruit_NeoPixel as neopixel
from signal import pause
from datetime import datetime
import time
import sys
import logging


DATA_PIN_LEFT = 18
DATA_PIN_RIGHT = 19
NUM_LED_LEFT = 34
NUM_LED_RIGHT = 34
BRIGHTNESS = 1
BRIGHTNESS_WINNER = 50

LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename='plinko.log', level=logging.INFO)

class Plinko:

    def __init__(self):
        """Initialize."""
        self.winner_flag = False

        # set up the hardware
        self.winner_sensor = Button(pin=4, bounce_time=1)
        self.winner_button = Button(pin=2, bounce_time=1)

        # decide what to do
        self.winner_sensor.when_pressed = self.win_sensor_triggered
        self.winner_button.when_pressed = self.win_button_pressed
        self.winner_button.when_released = self.win_button_pressed

        print("Set up left LED strip")
        self.strip_left = neopixel(
            pin=DATA_PIN_LEFT, num=NUM_LED_LEFT, brightness=BRIGHTNESS
        )
        self.strip_left.begin()

        print("Set up right LED strip")
        self.strip_right = neopixel(
            pin=DATA_PIN_RIGHT, num=NUM_LED_RIGHT, brightness=BRIGHTNESS, channel=1
        )
        self.strip_right.begin()

        self.run()

    def run(self):
        """Run but catch keyboard"""
        try:
            self.startup()
            self._run()
        except KeyboardInterrupt:
            self.shutdown()
        sys.exit(0)


    def _run(self):
        """Run."""
        print(f"Plinko is ready at {datetime.now()}")
        for x in range(100000):
            while self.winner_flag:
                time.sleep(1)
            self.colorWipeMirrored(color=0xFF0000)
            self.colorWipeMirrored(color=0x00FF00)
            self.colorWipeMirrored(color=0x0000FF)

    def startup(self):
        """Startup sequence."""
        print("Start up sequence")
        self.blink(
            strip=self.strip_left, color=0xFFFFFF, wait_seconds=0.5, num_blinks=5
        )
        self.blink(
            strip=self.strip_right, color=0xFFFFFF, wait_seconds=0.5, num_blinks=5
        )

    def shutdown(self):
        """Stop everything"""
        print(f"Plinko is closing down at {datetime.now()}")
        self.strip_left.setBrightness(0)
        self.strip_left.show()
        self.strip_right.setBrightness(0)
        self.strip_right.show()


    def win_sensor_triggered(self):
        self.winner(False)

    def win_button_pressed(self):
        self.winner(True)

    def winner(self, override=False):
        """We have a winner."""
        self.winner_flag = True

        self.log_winner()

        for x in range(3):
            self.blink(self.strip_left, color=0xFF0000, wait_seconds=.3)
            self.blink(self.strip_right, color=0xFF0000, wait_seconds=.3)
            self.blink(self.strip_left, color=0x00FF00, wait_seconds=.3)
            self.blink(self.strip_right, color=0x00FF00, wait_seconds=.3)
            self.blink(self.strip_left, color=0x0000FF, wait_seconds=.3)
            self.blink(self.strip_right, color=0x0000FF, wait_seconds=.3)

        print("done with winner")
        self.winner_flag = False

    def log_winner(self):
        """Log a winner."""
        print(f"Winner at {datetime.now()}")
        LOGGER.info("Winner")


    def blink(self, strip, color, wait_seconds=1, num_blinks=1):
        for i in range(num_blinks):
            for pixel in range(strip.numPixels()):
                strip.setPixelColor(pixel, color)
                strip.show()
            time.sleep(wait_seconds)
            strip.setBrightness(0)
            strip.show()
            time.sleep(wait_seconds)
            strip.setBrightness(BRIGHTNESS)

    def colorWipe(self, strip, color, wait_ms=150):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)

    def colorWipeMirrored(self, color, wait_ms=150, brightness=BRIGHTNESS):
        """Wipe color across display a pixel at a time."""
        self.strip_left.setBrightness(brightness)
        self.strip_right.setBrightness(brightness)
        for i in range(self.strip_left.numPixels()):
            if self.winner_flag:
                break
            self.strip_left.setPixelColor(i, color)
            self.strip_left.show()
            self.strip_right.setPixelColor(i, color)
            self.strip_right.show()
            time.sleep(wait_ms / 1000.0)


plinko = Plinko()
# wait until ctrl-C is pressed
pause()
