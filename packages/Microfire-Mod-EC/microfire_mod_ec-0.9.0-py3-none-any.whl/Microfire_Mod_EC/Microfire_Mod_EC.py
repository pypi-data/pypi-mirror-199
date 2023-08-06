import math
import struct
import time
import smbus  # pylint: disable=E0401

UFIRE_MOD_EC = 0x0a
MEASURE_EC_TASK = 80      # Command to start an EC measure 
MEASURE_TEMP_TASK = 40    # Command to measure temperature 
CALIBRATE_LOW_TASK = 20   # Command to calibrate the probe 
CALIBRATE_MID_TASK = 10   # Command to calibrate the probe 
CALIBRATE_HIGH_TASK = 8   # Command to calibrate the high point of the probe 
CALIBRATE_SINGLE_TASK = 4 # Command to calibrate the high point of the probe 
I2C_TASK = 2              # Command to change the i2c address 

EC_EC_MEASUREMENT_TIME = 750

HW_VERSION_REGISTER = 0               # hardware version register 
FW_VERSION_REGISTER = 1               # firmware version  register 
TASK_REGISTER = 2                     # task register 
STATUS_REGISTER = 3                   # status register 
MS_REGISTER = 4                       # mS register 
PSU_REGISTER = 8                      # PSU register 
TEMP_C_REGISTER = 12                  # temperature in C register 
CALIBRATE_REFLOW_REGISTER = 16        # reference low register 
CALIBRATE_READLOW_REGISTER = 20       # read high register 
CALIBRATE_REFMID_REGISTER = 24        # reference mid register 
CALIBRATE_READMID_REGISTER = 28       # reading mid register 
CALIBRATE_REFHIGH_REGISTER = 32       # reference high register 
CALIBRATE_READHIGH_REGISTER = 36      # reading high register 
CALIBRATE_SINGLE_OFFSET_REGISTER = 40 # calibration temperature register 
COEFFICIENT_REGISTER = 44             # temperature coefficient register 
CONSTANT_REGISTER = 48                # temperature constant register 
K_REGISTER = 52                       # Probe cell constant register 
KPA_REGISTER = 56                     # kPa register 
DENSITY_REGISTER = 60                 # density register 

def exception_catch(func):
    def func_wrapper(*args, **kwargs):
        try:
           return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return func_wrapper

class i2c(object):
    S = 0
    mS = 0
    uS = 0
    PSU = 0
    density = 0
    PPM_500 = 0
    PPM_640 = 0
    PPM_700 = 0
    calibrationLowReading = 0
    calibrationLowReference = 0
    calibrationMidReading = 0
    calibrationMidReference = 0
    calibrationHighReading = 0
    calibrationHighReference = 0
    calibrationSingleOffset = 0
    hwVersion = 0
    fwVersion = 0
    status = 0
    _address = 0
    _i2cPort = 0
    status_string = ["no error", "no probe or outside range", "system error", "config error"]

    @exception_catch
    def begin(self, i2c_bus=1, address=UFIRE_MOD_EC):
        self._address = address
        self._i2cPort = smbus.SMBus(i2c_bus)

        return self.connected()

    @exception_catch
    def connected(self):
        try:
            self._i2cPort.write_quick(self._address)
            return True
        except IOError:
            return False

    @exception_catch
    def calibrateSingle(self, solutionEC, tempC = 25.0, tempCoef = 0.019, tempConst = 25.0, k = 1.0, blocking = True):
        self._write_4_bytes(MS_REGISTER, solutionEC)
        self._write_4_bytes(TEMP_C_REGISTER, tempC)
        self._write_4_bytes(CONSTANT_REGISTER, tempConst)
        self._write_4_bytes(COEFFICIENT_REGISTER, tempCoef)
        self._write_4_bytes(K_REGISTER, k)

        self._send_command(CALIBRATE_SINGLE_TASK)
        if (blocking):
            time.sleep(EC_EC_MEASUREMENT_TIME / 1000.0)

        self.getDeviceInfo()
        return self.status

    @exception_catch
    def calibrateHigh(self, solutionEC, tempC = 25.0, tempCoef = 0.019, tempConst = 25.0, k = 1.0, blocking = True):
        self._write_4_bytes(MS_REGISTER, solutionEC)
        self._write_4_bytes(TEMP_C_REGISTER, tempC)
        self._write_4_bytes(CONSTANT_REGISTER, tempConst)
        self._write_4_bytes(COEFFICIENT_REGISTER, tempCoef)
        self._write_4_bytes(K_REGISTER, k)

        self._send_command(CALIBRATE_HIGH_TASK)
        if (blocking):
            time.sleep(EC_EC_MEASUREMENT_TIME / 1000.0)

        self.getDeviceInfo()
        return self.status

    @exception_catch
    def calibrateMid(self, solutionEC, tempC = 25.0, tempCoef = 0.019, tempConst = 25.0, k = 1.0, blocking = True):
        self._write_4_bytes(MS_REGISTER, solutionEC)
        self._write_4_bytes(TEMP_C_REGISTER, tempC)
        self._write_4_bytes(CONSTANT_REGISTER, tempConst)
        self._write_4_bytes(COEFFICIENT_REGISTER, tempCoef)
        self._write_4_bytes(K_REGISTER, k)

        self._send_command(CALIBRATE_MID_TASK)
        if (blocking):
            time.sleep(EC_EC_MEASUREMENT_TIME / 1000.0)

        self.getDeviceInfo()
        return self.status

    @exception_catch
    def calibrateLow(self, solutionEC, tempC = 25.0, tempCoef = 0.019, tempConst = 25.0, k = 1.0, blocking = True):
        self._write_4_bytes(MS_REGISTER, solutionEC)
        self._write_4_bytes(TEMP_C_REGISTER, tempC)
        self._write_4_bytes(CONSTANT_REGISTER, tempConst)
        self._write_4_bytes(COEFFICIENT_REGISTER, tempCoef)
        self._write_4_bytes(K_REGISTER, k)

        self._send_command(CALIBRATE_LOW_TASK)
        if (blocking):
            time.sleep(EC_EC_MEASUREMENT_TIME / 1000.0)

        self.getDeviceInfo()
        return self.status

    @exception_catch
    def getDeviceInfo(self):
        self.calibrationLowReading = self._read_4_bytes(CALIBRATE_READLOW_REGISTER)
        self.calibrationLowReference = self._read_4_bytes(CALIBRATE_REFLOW_REGISTER)
        self.calibrationMidReading = self._read_4_bytes(CALIBRATE_READMID_REGISTER)
        self.calibrationMidReference = self._read_4_bytes(CALIBRATE_REFMID_REGISTER)
        self.calibrationHighReading = self._read_4_bytes(CALIBRATE_READHIGH_REGISTER)
        self.calibrationHighReference = self._read_4_bytes(CALIBRATE_REFHIGH_REGISTER)
        self.calibrationSingleOffset = self._read_4_bytes(CALIBRATE_SINGLE_OFFSET_REGISTER)
        self.hwVersion = self._read_byte(HW_VERSION_REGISTER)
        self.fwVersion = self._read_byte(FW_VERSION_REGISTER)
        self.status = self._read_byte(STATUS_REGISTER)

    @exception_catch
    def measureEC(self, tempC = 25.0, tempCoef = 0.019, tempConst = 25.0, k = 1.0, kPa = 0, blocking = True):
        self._write_4_bytes(TEMP_C_REGISTER, tempC)
        self._write_4_bytes(CONSTANT_REGISTER, tempConst)
        self._write_4_bytes(COEFFICIENT_REGISTER, tempCoef)
        self._write_4_bytes(K_REGISTER, k)
        self._write_4_bytes(KPA_REGISTER, kPa)

        self._send_command(MEASURE_EC_TASK)
        if (blocking):
            time.sleep(EC_EC_MEASUREMENT_TIME / 1000.0)

        self._updateRegisters()

        return self.mS

    @exception_catch
    def reset(self):
        NAN = float('nan')
        self._write_4_bytes(CALIBRATE_REFHIGH_REGISTER, NAN)
        self._write_4_bytes(CALIBRATE_REFLOW_REGISTER, NAN)
        self._write_4_bytes(CALIBRATE_READMID_REGISTER, NAN)
        self._write_4_bytes(CALIBRATE_REFMID_REGISTER, NAN)
        self._write_4_bytes(CALIBRATE_READHIGH_REGISTER, NAN)
        self._write_4_bytes(CALIBRATE_READLOW_REGISTER, NAN)
        self._write_4_bytes(CALIBRATE_SINGLE_OFFSET_REGISTER, NAN)

    @exception_catch
    def setDeviceInfo(self, calibrationLowReading, calibrationLowReference, calibrationMidReading, calibrationMidReference, calibrationHighReading, calibrationHighReference, calibrationSingleOffset):
        self._write_4_bytes(CALIBRATE_REFHIGH_REGISTER, calibrationHighReference)
        self._write_4_bytes(CALIBRATE_REFLOW_REGISTER, calibrationLowReference)
        self._write_4_bytes(CALIBRATE_READMID_REGISTER, calibrationMidReading)
        self._write_4_bytes(CALIBRATE_REFMID_REGISTER, calibrationMidReference)
        self._write_4_bytes(CALIBRATE_READHIGH_REGISTER, calibrationHighReading)
        self._write_4_bytes(CALIBRATE_READLOW_REGISTER, calibrationLowReading)
        self._write_4_bytes(CALIBRATE_SINGLE_OFFSET_REGISTER, calibrationSingleOffset)

    @exception_catch
    def setI2CAddress(self, i2cAddress):
        self._write_4_bytes(MS_REGISTER, i2cAddress)
        self._send_command(I2C_TASK)
        self._address = i2cAddress

    @exception_catch
    def update(self):
        self._updateRegisters()

        return self.mS

    @exception_catch
    def _updateRegisters(self):
        self.status = self._read_byte(STATUS_REGISTER)
        self.mS = self._read_4_bytes(MS_REGISTER)
        self.PSU = self._read_4_bytes(PSU_REGISTER)
        self.density = self._read_4_bytes(DENSITY_REGISTER)

        if (self.status == 0):
            self.PPM_500 = self.mS * 500
            self.PPM_640 = self.mS * 640
            self.PPM_700 = self.mS * 700
            self.uS = self.mS * 1000
            self.S = self.mS / 1000
            self.getDeviceInfo()
        else:
            self.mS = 0
            self.PPM_500 = 0
            self.PPM_640 = 0
            self.PPM_700 = 0
            self.uS = 0
            self.S = 0
            self.PSU = 0

    @exception_catch
    def _send_command(self, command):
        self._i2cPort.write_byte_data(self._address, TASK_REGISTER, command)
        time.sleep(10 / 1000.0)

    @exception_catch
    def _write_4_bytes(self, reg, f):
        fd = bytearray(struct.pack("f", f))
        data = [0, 0, 0, 0]
        data[0] = fd[0]
        data[1] = fd[1]
        data[2] = fd[2]
        data[3] = fd[3]
        self._i2cPort.write_i2c_block_data(self._address, reg, data)

    @exception_catch
    def _read_4_bytes(self, reg):
        data = [0, 0, 0, 0]
        self._i2cPort.write_byte(self._address, reg)
        data = self._i2cPort.read_i2c_block_data(self._address, reg, 4)
        ba = bytearray(data)
        f = struct.unpack('f', ba)[0]
        return f

    @exception_catch
    def _write_byte(self, reg, val):
        self._i2cPort.write_byte_data(self._address, reg, val)

    @exception_catch
    def _read_byte(self, reg):
        self._i2cPort.write_byte(self._address, reg)
        return self._i2cPort.read_byte(self._address)
