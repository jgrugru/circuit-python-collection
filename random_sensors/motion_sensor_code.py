import time

import board
import digitalio
import neopixel

# PIR on GP0
pir = digitalio.DigitalInOut(board.GP0)
pir.direction = digitalio.Direction.INPUT
pir.pull = digitalio.Pull.DOWN

# Onboard NeoPixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2, auto_write=True)

old = pir.value
pixel[0] = (0, 0, 0)  # off

while True:
    v = pir.value
    if v != old:
        if v:
            print("Motion detected!")
            pixel[0] = (0, 255, 0)  # green
        else:
            print("Motion ended!")
            pixel[0] = (0, 0, 0)  # off
        old = v
    time.sleep(0.05)
