import board
import busio
import displayio
from kmk.extensions import Extension
from greentree.logger import Logger
import time

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
BUFFER_SIZE = DISPLAY_WIDTH * DISPLAY_HEIGHT // 8  # 1024 bytes
buffer = bytearray(BUFFER_SIZE)  # all zeros
frames = [
    b"\x40" + open(f"/completed_animations/logo/frame{n}.bin", "rb").read()
    for n in range(1, 5)
]


class OLED(Extension):
    """
    byte commands to ssd1306 over i2c
    0xAE,       # display off
    0xA1,       # horizontal flip
    0xC8,       # vertical flip
    0xAF        # display on
    """

    def __init__(
        self,
        startup_animation: list[str],
        logger: callable = None,
    ):
        self.is_initialized = False
        self.i2c = None
        self.oled = None
        if logger is not None:
            self.logger = logger
        else:
            self.logger = Logger()

    def on_runtime_enable(self, keyboard):
        pass

    def on_runtime_disable(self, keyboard):
        pass

    def during_bootup(self, keyboard):
        print(self.is_initialized)
        if not self.is_initialized:
            print("*" * 100)
            displayio.release_displays()
            i2c = busio.I2C(scl=board.GP29, sda=board.GP28, frequency=400_000)
            i2c.unlock()

            locked = False
            while not locked:
                locked = i2c.try_lock()

            for frame in frames:
                i2c.writeto(0x3C, frame)
                time.sleep(0.7)
            i2c.writeto(0x3C, b"\x40" + b"\xff" * 1024)  # fills the screen
            i2c.unlock()
            # oled = adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c, addr=0x3c)
            # oled.fill(0)
            # oled.rotate(False)

            # self.oled = oled
            self.i2c = i2c
            self.is_initialized = True

    def before_matrix_scan(self, keyboard):
        """
        Return value will be injected as an extra matrix update
        """
        pass

    def after_matrix_scan(self, keyboard):
        """
        Return value will be replace matrix update if supplied
        """
        pass

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass


# endregion
