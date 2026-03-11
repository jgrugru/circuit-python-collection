import time

import analogio
import board

mic = analogio.AnalogIn(board.GP26_A0)
baseline = mic.value

print("raw,loud")
while True:
    v = mic.value
    baseline = int(baseline * 0.99 + v * 0.01)
    loud = abs(v - baseline)
    print(f"{v},{loud}")
    time.sleep(0.05)
