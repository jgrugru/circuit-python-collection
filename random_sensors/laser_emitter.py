import time

import board
import digitalio

# Initialize the laser pin (e.g., D10) as an output
laser_pin = digitalio.DigitalInOut(board.GP0)
laser_pin.direction = digitalio.Direction.OUTPUT

print("Starting laser test...")

while True:
    laser_pin.value = True  # Turn laser ON (HIGH)
    print("Laser ON")
    time.sleep(1)
    laser_pin.value = False  # Turn laser OFF (LOW)
    print("Laser OFF")
    time.sleep(1)
