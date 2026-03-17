# Code for dev board
Use this script to run the animations with an ssd1306 oled. I'm running mine on a waveshare rp2040 zero.

```python
import busio
import board
import displayio
import time
import adafruit_ssd1306
import gc

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64 
BUFFER_SIZE = DISPLAY_WIDTH * DISPLAY_HEIGHT // 8  # 1024 bytes
buffer = bytearray(BUFFER_SIZE)  # all zeros


def fill_pixels_to_oled_from_file(filename: str, oled: adafruit_ssd1306.SSD1306_I2C) -> adafruit_ssd1306.SSD1306_I2C:
    with open(filename, "r") as f:
        for line in f:
            cleaned_line = line.strip()
            if cleaned_line != "":
                x_str, y_str = cleaned_line.split(",")
                x = int(x_str)
                y = int(y_str)
                oled.pixel(x, y, 1)

def setup_oled() -> adafruit_ssd1306.SSD1306_I2C:
    displayio.release_displays()

    i2c = busio.I2C(scl=board.GP15, sda=board.GP14, frequency=1_000_000)

    locked = False
    print(locked)
    while not locked:
        locked = i2c.try_lock()
        print(locked)

    print(i2c.scan())
    print([hex(x) for x in i2c.scan()])

    i2c.unlock()
    oled = adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c, addr=0x3c)
    oled.rotate(False)
    return oled, i2c

oled, i2c = setup_oled()
# oled.invert(True)

frames = [b"\x40" + open(f"/jeff_name/frame{n}.bin", "rb").read() for n in range(1, 6)]
print(gc.mem_free())

del DISPLAY_HEIGHT
del DISPLAY_WIDTH
del BUFFER_SIZE

while not i2c.try_lock():
    pass

while True:
    for frame in frames:
        i2c.writeto(0x3c, frame)
        time.sleep(0.35)
```