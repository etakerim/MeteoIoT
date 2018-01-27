import smbus
import ctypes
import collections

CHIP_ID   = 0xD0
RESET     = 0xE0
STATUS    = 0xF3
CTRL_MEAS = 0xF4
CONFIG    = 0xF5
PRESS_MSB = 0xF7   # (0xF7, 0xF8, 0xF9)
TEMP_MSB  = 0xFA   # (0xFA, 0xFB, 0xFC)

DATA_BASE = 0xF7
DATA_END  = 0xFD
DATA_LEN  = DATA_END - DATA_BASE

CALIB_BASE = 0x88
CALIB_END  = 0xA0
CALIB_LEN  = CALIB_END - CALIB_BASE

OSRS_P     = 2
OSRS_T     = 5
IIR_FILTER = 2
T_SB       = 5

Filter = collections.namedtuple('Filter', ['p', 't', 'iir'])


class Mode:
    SLEEP = 0 
    FORCED = 2
    NORMAL = 3


class Sampling:
    ULTRA_LOW_POWER = Filter(p=1, t=1, iir=0)
    LOW_POWER = Filter(p=2, t=1, iir=0)
    STANDARD_RES = Filter(p=3, t=1, iir=4)
    HIGH_RES = Filter(p=4, t=1, iir=4)
    ULTRA_HIGH_RES = Filter(p=5, t=2, iir=4)


class StandbyTime:
    (MS_HALF, MS_62, MS_125, MS_250, MS_500,
     MS_1000, MS_2000, MS_4000) = range(8)


class BMP280:
    def __init__(self, mode=Mode.NORMAL, oversample=Sampling.STANDARD_RES,
                 altitude=0, t_standby=0, address=0x76):
        self.i2caddr = address
        self.i2cbus = smbus.SMBus(1)

        self.mode = mode
        self.t_standby = t_standby
        self.osrs = oversample
        # User accessible properties of current temperature and pressure
        self.temperature = None
        self.pressure = None

        self.id = self.i2cbus.read_byte_data(self.i2caddr, CHIP_ID)
        self.setup()
        self.read_calibration()

    def setup(self):
        config = (self.t_standby << T_SB) | (self.osrs.iir << IIR_FILTER)
        osrs = ((self.osrs.t << OSRS_T) |
                (self.osrs.p << OSRS_P) | self.mode)

        self.i2cbus.write_byte_data(self.i2caddr, CONFIG, config)
        self.i2cbus.write_byte_data(self.i2caddr, CTRL_MEAS, osrs)

    def int16(self, data, index):
        return ctypes.c_short((data[index + 1] << 8) | data[index]).value
 
    def uint16(self, data, index):
        return (data[index + 1] << 8) | data[index]
    
    def bytes_concat(self, x):
        msb, lsb, xsb = x
        return ((msb << 16) | (lsb << 8) | (xsb & 0xf0)) >> 4 

    def read_calibration(self):
        cal = self.i2cbus.read_i2c_block_data(self.i2caddr, CALIB_BASE, CALIB_LEN)
        self.dig_T1 = self.uint16(cal, 0)
        self.dig_T2 = self.int16(cal, 2)
        self.dig_T3 = self.int16(cal, 4)
        self.dig_P1 = self.uint16(cal, 6)
        self.dig_P2 = self.int16(cal, 8)
        self.dig_P3 = self.int16(cal, 10)
        self.dig_P4 = self.int16(cal, 12)
        self.dig_P5 = self.int16(cal, 14)
        self.dig_P6 = self.int16(cal, 16)
        self.dig_P7 = self.int16(cal, 18)
        self.dig_P8 = self.int16(cal, 20)
        self.dig_P9 = self.int16(cal, 22)

    def dev_reset(self):
        self.i2cbus.write_byte_data(self.i2caddr, RESET, 0xB6)
        self.setup()

    def mslp_pressure(self, altitude):
        return self.pressure / ((1 - (altitude / 44330)) ** 5.255)

    def measure(self):
        # Bus readout from addressed device 
        if self.mode == Mode.FORCED:
            self.setup()
        data = self.i2cbus.read_i2c_block_data(self.i2caddr, DATA_BASE, DATA_LEN)
        p = self.bytes_concat(data[0: 3])
        t = self.bytes_concat(data[3: 6])

        # Temperature compensation formula
        a = (t / 16384 - self.dig_T1 / 1024) * self.dig_T2
        b = ((t / 131072 - self.dig_T1 / 8192) ** 2) * self.dig_T3
        t_fine = a + b

        # Pressure compensation formula
        a = (t_fine / 2) - 64000
        b = a * a * self.dig_P6 / 32768
        b = b + a * self.dig_P5 * 2
        b = (b / 4) + (self.dig_P4 * 65536)
        a = (self.dig_P3 * a * a / 524288 + self.dig_P2 * a) / 524288
        a = (1 + a / 32768) * self.dig_P1
        
        p = 1048576 - p
        p = (p - (b / 4096)) * 6250 / a
        a = self.dig_P9 * p * p / 2147483648
        b = p * self.dig_P8 / 32768
        
        self.temperature = t_fine / 5120
        self.pressure = (p + (a + b + self.dig_P7) / 16) / 100

if __name__ == '__main__':
    sensor = BMP280()
    print(hex(sensor.id))
    sensor.measure()
    print('{:.2f} °C'.format(sensor.temperature))
    print('{:.2f} Pa'.format(sensor.pressure))
    print('{:.2f} Pa'.format(sensor.mslp_pressure(150)))
