import time
import board
import busio
import adafruit_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.extensions import Extension
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.potentiometer import PotentiometerHandler
from kmk.keys import KC


# --- No physical keyboard matrix ---
class NoMatrix:
    coord_mapping = []
    def scan_for_changes(self):
        return None


# --- OLED extension ---
class OledVolume(Extension):
    def __init__(self):
        self.oled = None
        self.last_draw = 0
        self.level = 0
        self.steps = 30
        self.pos = 0

    def during_bootup(self, keyboard):
        i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        self.draw(force=True)

    def set(self, level, steps, pos):
        self.level = level
        self.steps = steps
        self.pos = pos

    def draw(self, force=False):
        if self.oled is None:
            return

        now = time.monotonic()
        # limit refresh rate (I2C + OLED is slow)
        if not force and (now - self.last_draw) < 0.1:
            return
        self.last_draw = now

        pct = int((self.level / self.steps) * 100) if self.steps else 0

        self.oled.fill(0)
        self.oled.text("Volume", 0, 0, 1)
        self.oled.text(f"{self.level:02d}/{self.steps}", 0, 18, 1)
        self.oled.text(f"{pct:3d}%", 0, 36, 1)
        # optional: show raw pot position (0..127)
        self.oled.text(f"pot {self.pos:3d}", 0, 54, 1)
        self.oled.show()

    # KMK calls these regularly; we’ll refresh here too
    def before_matrix_scan(self, keyboard):
        self.draw()
        return None

    # no-op required hooks
    def on_runtime_enable(self, keyboard): pass
    def on_runtime_disable(self, keyboard): pass
    def after_matrix_scan(self, keyboard): return None
    def before_hid_send(self, keyboard): pass
    def after_hid_send(self, keyboard): pass
    def on_powersave_enable(self, keyboard): pass
    def on_powersave_disable(self, keyboard): pass


keyboard = KMKKeyboard()
keyboard.matrix = NoMatrix()
keyboard.coord_mapping = []
keyboard.keymap = [[]]

keyboard.extensions.append(MediaKeys())

# OLED
oled_ext = OledVolume()
keyboard.extensions.append(oled_ext)

# Pot -> volume
VOL_STEPS = 30        # change feel: higher = more sensitive
MAX_TAPS_PER_UPDATE = 4
last_step = None

def pot_volume_handler(state):
    global last_step

    pos = state.position          # 0..127
    step = int((pos * VOL_STEPS) / 127)

    # update OLED with the knob level immediately
    oled_ext.set(step, VOL_STEPS, pos)

    if last_step is None:
        last_step = step
        return

    diff = step - last_step
    if diff == 0:
        return

    key = KC.VOLU if diff > 0 else KC.VOLD
    taps = min(abs(diff), MAX_TAPS_PER_UPDATE)
    for _ in range(taps):
        keyboard.tap_key(key)

    last_step = step


pots = PotentiometerHandler()
pots.pins = (
    (board.GP26, pot_volume_handler, False),  # wiper on GP26, ends to 3V3/GND
)
keyboard.modules.append(pots)

if __name__ == "__main__":
    keyboard.go()
