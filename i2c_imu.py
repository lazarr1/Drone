import sys
import board
import busio
import time
import smbus

addr = 0x1d

i2c = busio.I2C(board.SCL, board.SDA)
i2c.init(board.SCL, board.SDA, frequency = 400000)

print("Scan : ", [hex(i) for i in i2c.scan()])

MMAB452Q = 0x1d

if MMAB452Q not in i2c.scan():
    print("could not find imu")
    sys.exit()


def get_MMAB452Q_id():
    result = bytearray([0x0D])
    i2c.writeto_then_readfrom(addr,result,result); 
    return result

get_MMAB452Q_id()

result = bytearray([0x2A, 0x2A | 0x01])
i2c.writeto(addr,result); 

while(1):
    result = bytearray([0x04])
    i2c.writeto_then_readfrom(addr,result,result); 

    print(hex(result[0]))
    time.sleep(0.1)
