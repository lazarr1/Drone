import sys
import board
import busio

import smbus

addr = 0x1d
bus = smbus.SMBus(1)
bus.write_byte(addr, 0xFF)


i2c = busio.I2C(board.SCL, board.SDA)

print("Scan : ", [hex(i) for i in i2c.scan()])

MMAB452Q = 0x1d

if MMAB452Q not in i2c.scan():
    print("could not find imu")
    sys.exit()


def get_MMAB452Q_id():
    i2c.writeto(MMAB452Q, bytes([0x0E]), stop=False)
    result = bytearray(1)
    i2c.readfrom_into(MMAB452Q, result)
    print(result)
    print("ID: ", int.from_bytes(result, "big"))


get_MMAB452Q_id()
