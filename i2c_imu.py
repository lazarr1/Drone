import sys
import board
import busio


i2c = busio.I2C(board.SCL, board.SDA)


print("Scan : " , [hex(i) for i in i2c.scan()])

MMAB452Q = 0x1d

if not MMAB452Q in i2c.scan():
    print("could not find imu")
    sys.exit()


def get_MMAB452Q_id():

    for i in range(255):

        # hex_int = int(hex(i), base=16)
        # new_int = hex_int + 0x200

        # print(hex_int)

        i2c.writeto(MMAB452Q,  bytes([i]), stop = False) 
        result = bytearray(1)
        i2c.readfrom_into(MMAB452Q, result)

        print("ID: ", int.from_bytes(result, "big"))

get_MMAB452Q_id()