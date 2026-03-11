import machine
import time

led = machine.Pin(16, machine.Pin.OUT)

while True:
    led.value(True)  # Turn on the LED
    time.sleep(0.5)  # Wait for 0.5 seconds
    led.value(False)  # Turn off the LED
    time.sleep(0.5)  # Wait for 0.5 seconds
