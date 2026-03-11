import board
import busio
import adafruit_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.extensions import Extension


# --- Dummy matrix scanner: no keys, no scanning ---
class NoMatrix:
    coord_mapping = []

    def scan_for_changes(self):
        return None


# --- OLED extension: draw "123" once on boot ---
class OledTest(Extension):
    def __init__(self):
        self.oled = None

    def during_bootup(self, keyboard):
        i2c = busio.I2C(board.GP15, board.GP14)  # SCL, SDA
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

        self.oled.fill(0)
        self.oled.text("123", 0, 0, 1)
        self.oled.show()

    # --- required no-op methods ---
    def on_runtime_enable(self, keyboard): pass
    def on_runtime_disable(self, keyboard): pass
    def before_matrix_scan(self, keyboard): return None
    def after_matrix_scan(self, keyboard): return None
    def before_hid_send(self, keyboard): pass
    def after_hid_send(self, keyboard): pass
    def on_powersave_enable(self, keyboard): pass
    def on_powersave_disable(self, keyboard): pass


keyboard = KMKKeyboard()

# Prevent KMK from trying to init a real key matrix
keyboard.matrix = NoMatrix()
keyboard.coord_mapping = []
keyboard.keymap = [[]]

keyboard.extensions.append(OledTest())

if __name__ == "__main__":
    keyboard.go()
