from gpiozero import Button
from rpi_ws281x import Adafruit_NeoPixel as neopixel
from signal import pause
import time

DATA_PIN_LEFT = 18
DATA_PIN_RIGHT = 19
NUM_LED_LEFT = 34
NUM_LED_RIGHT = 34
BRIGHTNESS = 10
BRIGHTNESS_WINNER = 50

def startup(light_string):
    blink(light_string,0xffffff,1,5)

def blink(strip, color, wait_seconds, num_blinks):
    for i in range(num_blinks):
        for pixel in range(strip.numPixels()):
            strip.setPixelColor(pixel,color)
            strip.show()
        time.sleep(wait_seconds)
        strip.setBrightness(0)
        strip.show()
        time.sleep(wait_seconds)
        strip.setBrightness(BRIGHTNESS)


def colorWipe(strip, color, wait_ms=150):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def colorWipeMirrored(strip1, strip2, color, wait_ms=150, brightness=BRIGHTNESS):
    """Wipe color across display a pixel at a time."""
    strip1.setBrightness(brightness)
    strip2.setBrightness(brightness)
    for i in range(strip1.numPixels()):
        strip1.setPixelColor(i, color)
        strip1.show()
        strip2.setPixelColor(i, color)
        strip2.show()
        time.sleep(wait_ms/1000.0)
    strip1.setBrightness(BRIGHTNESS)
    strip2.setBrightness(BRIGHTNESS)


def win_sensor_triggered():
    winner(False)

def win_button_pressed():
    winner(True)


def winner(override=False):
    '''We have a winner.'''
    background = False
    if override:
        print("winner by override")
    else:
        print("winner by sensor")

    # TODO: log it with time

    for x in range(10):
        colorWipeMirrored(strip_left, strip_right, color=0xff0000, wait_ms=0, brightness=BRIGHTNESS_WINNER)
        time.sleep(.5)
        colorWipeMirrored(strip_left, strip_right, color=0x00FF00, wait_ms=0, brightness=BRIGHTNESS_WINNER)
        time.sleep(.5)
        colorWipeMirrored(strip_left, strip_right, color=0x0000ff, wait_ms=0, brightness=BRIGHTNESS_WINNER)
        time.sleep(.5)

    background = True


print("Starting Plinko")
background = True

# set up the hardware
winner_sensor = Button(pin=4, bounce_time=1)
winner_button = Button(pin=2, bounce_time=1)


# decide what to do
winner_sensor.when_pressed = win_sensor_triggered
winner_button.when_pressed = win_button_pressed
winner_button.when_released = win_button_pressed

print("Set up left LED strip")
strip_left = neopixel(pin=DATA_PIN_LEFT,num=NUM_LED_LEFT, brightness=BRIGHTNESS)
strip_left.begin()

print("Set up right LED strip")
strip_right = neopixel(pin=DATA_PIN_RIGHT,num=NUM_LED_RIGHT, brightness=BRIGHTNESS, channel=1)
strip_right.begin()

startup(strip_left)
startup(strip_right)

for x in range(100):
    if background:
        colorWipeMirrored(strip_left, strip_right, color=0xff0000)
        colorWipeMirrored(strip_left, strip_right, color=0x00ff00)
        colorWipeMirrored(strip_left, strip_right, color=0x0000ff)

# wait until ctrl-C is pressed
print("Plinko is ready and waiting....")
pause()
