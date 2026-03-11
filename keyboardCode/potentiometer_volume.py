
import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.potentiometer import PotentiometerHandler
from kmk.keys import KC


# --- Dummy matrix scanner: no keys, no events ---
class NoMatrix:
    coord_mapping = []

    def scan_for_changes(self):
        return None


keyboard = KMKKeyboard()
keyboard.matrix = NoMatrix()   # <- prevents KMK from trying to init a real matrix
keyboard.coord_mapping = []    # no keys
keyboard.keymap = [[]]         # KMK requires a keymap to exist

keyboard.extensions.append(MediaKeys())

VOL_STEPS = 30   # tweak: higher = more sensitive, lower = less spammy
last_step = None

def pot_volume_handler(state):
    global last_step

    # PotentiometerHandler provides 0..127
    pos = state.position
    step = int((pos * VOL_STEPS) / 127)

    if last_step is None:
        last_step = step
        return

    diff = step - last_step
    if diff == 0:
        return

    key = KC.VOLU if diff > 0 else KC.VOLD

    # Cap taps per update so it doesn’t flood if you spin fast
    taps = min(abs(diff), 4)
    for _ in range(taps):
        keyboard.tap_key(key)

    last_step = step


pots = PotentiometerHandler()
pots.pins = (
    (board.GP8, pot_volume_handler, False),  # (analog pin, callback, invert)
)
keyboard.modules.append(pots)


if __name__ == "__main__":
    keyboard.go()
