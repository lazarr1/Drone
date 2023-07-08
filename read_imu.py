import board
import busio
import time
from enum import Enum


class MMA8452Q_Registers(Enum):
    STATUS = 0x00
    OUT_X_MSB = 0x01
    OUT_X_LSB = 0x02
    OUT_Y_MSB = 0x03
    OUT_Y_LSB = 0x04
    OUT_Z_MSB = 0x05
    OUT_Z_LSB = 0x06
    SYSMOD = 0x0B
    INT_SOURCE = 0x0C
    WHO_AM_I = 0x0D
    XYZ_DATA_CFG = 0x0E
    HP_FILTER_CUTOFF = 0x0F
    PL_STATUS = 0x10
    PL_CFG = 0x11
    PL_COUNT = 0x12
    PL_BF_ZCOMP = 0x13
    P_L_THS_REG = 0x14
    FF_MT_CFG = 0x15
    FF_MT_SRC = 0x16
    FF_MT_THS = 0x17
    FF_MT_COUNT = 0x18
    TRANSIENT_CFG = 0x1D
    TRANSIENT_SRC = 0x1E
    TRANSIENT_THS = 0x1F
    TRANSIENT_COUNT = 0x20
    PULSE_CFG = 0x21
    PULSE_SRC = 0x22
    PULSE_THSX = 0x23
    PULSE_THSY = 0x24
    PULSE_THSZ = 0x25
    PULSE_TMLT = 0x26
    PULSE_LTCY = 0x27
    PULSE_WIND = 0x28
    ASLP_COUNT = 0x29
    CTRL_REG1 = 0x2A
    CTRL_REG2 = 0x2B
    CTRL_REG3 = 0x2C
    CTRL_REG4 = 0x2D
    CTRL_REG5 = 0x2E
    OFF_X = 0x2F
    OFF_Y = 0x30
    OFF_Z = 0x31


class MMA8452Q_Scale(Enum):
    SCALE_2G = 2
    SCALE_4G = 4
    SCALE_8G = 8


class MMA8452Q_ODR(Enum):
    ODR_800 = 0
    ODR_400 = 1
    ODR_200 = 2
    ODR_100 = 3
    ODR_50 = 4
    ODR_12 = 5
    ODR_6 = 6
    ODR_1 = 7


class MMA8452Q:

    def __init__(self):
        self.addr = 0x1d

    def init(self, scale: MMA8452Q_Scale = MMA8452Q_Scale.SCALE_2G,
             odr: MMA8452Q_ODR = MMA8452Q_ODR.ODR_800, bus: busio.I2C = None) -> int:

        if bus is None:
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.i2c.init(board.SCL, board.SDA, frequency=400000)
        else:
            self.i2c = bus

        result = bytearray([MMA8452Q_Registers.WHO_AM_I.value])
        self.i2c.writeto_then_readfrom(self.addr, result, result)

        if result[0] != 0x2A:
            print("WHO_AM_I Failed")
            return 0

        self.standby()
        self.__setScale(scale)
        self.__setOdr(odr)
        self.active()

        return 1

    def read(self) -> list[float]:
        rawData = bytearray(6)

        self.readRegistersInto(MMA8452Q_Registers.OUT_X_MSB, rawData, 6)

        x = ((rawData[0] << 8 | rawData[1])) >> 4
        y = ((rawData[2] << 8 | rawData[3])) >> 4
        z = ((rawData[4] << 8 | rawData[5])) >> 4

        cx = float(x/float(1 << 11) * float(self.scale))
        cy = float(y/float(1 << 11) * float(self.scale))
        cz = float(z/float(1 << 11) * float(self.scale))

        print([cx, cy, cz])
        return [cx, cy, cz]

    def readRegistersInto(self, reg: MMA8452Q_Registers,
                          output: bytearray, length: int) -> None:
        for i in range(length):
            output[i] = self.readRawRegister(reg.value + i)

    def readRawRegister(self, reg: MMA8452Q_Registers) -> bytes:
        res = bytearray([reg])
        self.i2c.writeto_then_readfrom(self.addr, res, res)
        return res[0]

    def readRegister(self, reg: MMA8452Q_Registers) -> bytes:
        res = bytearray([reg.value])
        self.i2c.writeto_then_readfrom(self.addr, res, res)
        return res[0]

    # CHECK IF NEW DATA IS AVAILABLE
    # This function checks the status of the MMA8452Q
    # to see if new data is availble.
    # returns 0 if no new data is present, or a 1 if new data is available.
    def __available(self) -> bool:
        return (self.readRegister(MMA8452Q_Registers.STATUS) & 0x08) >> 3

    # Set IMU to standby mode to change register settings
    def standby(self) -> None:
        c = self.readRegister(MMA8452Q_Registers.CTRL_REG1)

        # clear only the standby bit
        self.i2c.writeto(self.addr, bytearray([MMA8452Q_Registers.CTRL_REG1.value, c | (~ (0x01) & 0xFF)]))

    def active(self) -> None:
        c = self.readRegister(MMA8452Q_Registers.CTRL_REG1)

        # set only the standby bit
        self.i2c.writeto(self.addr, bytearray([MMA8452Q_Registers.CTRL_REG1.value, c | (0x01)]))

    # SET THE OUTPUT DATA RATE
    # This function sets the output data rate of the MMA8452Q.
    # Possible values for the odr parameter are: ODR_800, ODR_400, ODR_200,
    # ODR_100, ODR_50, ODR_12, ODR_6, or ODR_1
    def __setOdr(self, odr: MMA8452Q_ODR) -> None:
        self.odr = odr.value

        ctrl_1 = self.readRegister(MMA8452Q_Registers.CTRL_REG1)

        ctrl_1 &= 0xCF  # mask out data rate bits
        ctrl_1 |= (self.odr << 3)

        self.i2c.writeto(self.addr, bytearray([MMA8452Q_Registers.CTRL_REG1.value, ctrl_1]))

    def __setScale(self, scale: MMA8452Q_Scale) -> None:
        self.scale = scale.value
        cfg = self.readRegister(MMA8452Q_Registers.XYZ_DATA_CFG)
        cfg &= 0xFC  # mask out scale bits
        cfg |= (self.scale >> 2)

        self.i2c.writeto(self.addr, bytearray([MMA8452Q_Registers.XYZ_DATA_CFG.value, cfg]))


if __name__ == "__main__":
    imu = MMA8452Q()
    imu.init()
    while 1:
        imu.read()
        time.sleep(0.5)
