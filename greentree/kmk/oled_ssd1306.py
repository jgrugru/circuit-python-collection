import busio
import displayio
from kmk.extensions import Extension
import time
import microcontroller

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
BUFFER_SIZE = DISPLAY_WIDTH * DISPLAY_HEIGHT // 8


class OLED(Extension):
    def __init__(
        self,
        scl: microcontroller.Pin,
        sda: microcontroller.Pin,
        startup_animation: list[str],
        button_press_animation: list[str],
        layer_1_filepath: str,
        frequency: int = 400_000,
    ):
        # initialize all attributes to None
        self.scl = None
        self.sda = None
        self.frequency = None

        self.startup_animation = None
        self.layer_1_filepath = None

        self.is_initialized = None
        self.i2c = None
        self.oled = None

        # assign actual values
        self.scl = scl
        self.sda = sda
        self.frequency = frequency

        self.startup_animation = startup_animation
        self.button_press_animation = button_press_animation
        self.layer_1_filepath = layer_1_filepath

        self.is_initialized = False

    def on_runtime_enable(self, keyboard):
        pass

    def on_runtime_disable(self, keyboard):
        pass

    def during_bootup(self, keyboard):
        if not self.is_initialized:
            displayio.release_displays()

            i2c = busio.I2C(scl=self.scl, sda=self.sda, frequency=self.frequency)

            while not i2c.try_lock():
                pass

            print([hex(x) for x in i2c.scan()])

            addr = 0x3C

            def cmd(c):
                i2c.writeto(addr, bytes([0x00, c]))

            cmd(0xAE)
            cmd(0x20)
            cmd(0x00)
            cmd(0xB0)
            cmd(0xC8)
            cmd(0x00)
            cmd(0x10)
            cmd(0x40)
            cmd(0x81)
            cmd(0x7F)
            cmd(0xA1)
            cmd(0xA6)
            cmd(0xA8)
            cmd(0x3F)
            cmd(0xA4)
            cmd(0xD3)
            cmd(0x00)
            cmd(0xD5)
            cmd(0x80)
            cmd(0xD9)
            cmd(0xF1)
            cmd(0xDA)
            cmd(0x12)
            cmd(0xDB)
            cmd(0x40)
            cmd(0x8D)
            cmd(0x14)
            cmd(0xAF)

            cmd(0xA0)
            cmd(0xC0)

            buffer = b"\xff" * 1024
            i2c.writeto(addr, b"\x40" + buffer)

            time.sleep(1)

            for frame in self.startup_animation:
                i2c.writeto(addr, frame)
                time.sleep(0.7)

            i2c.writeto(addr, self.layer_1_filepath)

            self.i2c = i2c
            self.is_initialized = True

    def before_matrix_scan(self, keyboard):
        pass

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update is not None:
            for frame in self.button_press_animation:
                self.i2c.writeto(0x3C, frame)
            self.i2c.writeto(0x3C, self.layer_1_filepath)
            # time.sleep(0.7)

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass
