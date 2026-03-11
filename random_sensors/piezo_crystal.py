import time

import board
import pwmio

# GP0 goes to the (+) pin on the piezo crystal
buzzer = pwmio.PWMOut(board.GP0, frequency=1000, duty_cycle=0)

while True:
    buzzer.duty_cycle = 50000
    time.sleep(0.1)
    buzzer.duty_cycle = 0
    time.sleep(10)
