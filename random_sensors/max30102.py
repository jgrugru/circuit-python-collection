from random_sensors.max30102 import MAX30102
from machine import SoftI2C, Pin

my_SDA_pin = 21  # I2C SDA pin number here!
my_SCL_pin = 22  # I2C SCL pin number here!
my_i2c_freq = 400000  # I2C frequency (Hz) here!

i2c = SoftI2C(sda=Pin(my_SDA_pin),
              scl=Pin(my_SCL_pin),
              freq=my_i2c_freq)

sensor = MAX30102(i2c=i2c)