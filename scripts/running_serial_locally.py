import serial

PORT = "/dev/tty.usbmodem3101"  # change this
ser = serial.Serial(PORT, 115200, timeout=1)
ser.reset_input_buffer()

while True:
    line = ser.readline()
    if line:
        print(line.decode("utf-8", errors="ignore").rstrip())


# import time
# import serial
# from serial.tools import list_ports

# ports = [p.device for p in list_ports.comports() if "usbmodem" in p.device]

# print("Found ports:", ports)

# for dev in ports:
#     try:
#         print("Trying:", dev)
#         with serial.Serial(dev, 115200, timeout=1) as ser:
#             ser.write(b"Hello from macOS!\n")
#             ser.flush()
#         print("Sent to:", dev)
#     except Exception as e:
#         print("Failed:", dev, e)

# print("Done. If your keyboard is listening on usb_cdc.data, one of those should show on OLED.")
# time.sleep(1)
