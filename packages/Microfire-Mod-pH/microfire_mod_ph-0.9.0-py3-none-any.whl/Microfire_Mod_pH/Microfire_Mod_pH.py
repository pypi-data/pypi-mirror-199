import math
import struct
import time
import smbus  # pylint: disable=E0401

UFIRE_MOD_PH = 0x0b
MEASURE_PH_TASK = 80      # Command to start a pH measure 
MEASURE_TEMP_TASK = 40    # Command to measure temperature 
CALIBRATE_LOW_TASK = 20   # Command to calibrate the probe 
CALIBRATE_MID_TASK = 10   # Command to calibrate the low point of the probe 
CALIBRATE_HIGH_TASK = 8   # Command to calibrate the high point of the probe 
CALIBRATE_SINGLE_TASK = 4 # Command to calibrate the high point of the probe 
I2C_TASK = 2              # Command to change the i2c address 

HW_VERSION_REGISTER = 0               # hardware version register 
FW_VERSION_REGISTER = 1               # firmware version  register 
TASK_REGISTER = 2                     # task register 
STATUS_REGISTER = 3                   # status register 
PH_REGISTER = 4                       # pH register 
TEMP_C_REGISTER = 8                   # temperature in C register 
MV_REGISTER = 12                      # mV register 
CALIBRATE_REFLOW_REGISTER = 16        # reference low register 
CALIBRATE_READLOW_REGISTER = 20       # reference high register 
CALIBRATE_REFMID_REGISTER = 24        # reading low register 
CALIBRATE_READMID_REGISTER = 28       # reading high register 
CALIBRATE_REFHIGH_REGISTER = 32       # reading low register 
CALIBRATE_READHIGH_REGISTER = 36      # reading high register 
CALIBRATE_SINGLE_OFFSET_REGISTER = 40 # calibration temperature register 
CALIBRATE_TEMPERATURE_REGISTER = 44   # calibration temperature register 

PH_PH_MEASUREMENT_TIME = 750
PH_TEMP_MEASURE_TIME = 750

def exception_catch(func):
    def func_wrapper(*args, **kwargs):
        try:
           return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return func_wrapper

class i2c(object):
    pH = 0
    mV = 0
    PPM_700 = 0
    tempC = 0
    tempF = 0
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
    status_string = ["no error", "outside lower range", "outside upper range", "system error"]

    @exception_catch
    def begin(self, i2c_bus=1, address=UFIRE_MOD_PH):
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
    def calibrateSingle(self, solution_pH, tempC = 25.0, blocking = True):
        self._write_4_bytes(PH_REGISTER, solution_pH);
        self._write_4_bytes(CALIBRATE_TEMPERATURE_REGISTER, tempC);

        self._send_command(CALIBRATE_SINGLE_TASK);
        if (blocking):
            time.sleep(PH_PH_MEASUREMENT_TIME / 1000.0)

        self.getDeviceInfo();
        return self.status;

    @exception_catch
    def calibrateHigh(self, solution_pH, tempC = 25.0, blocking = True):
        self._write_4_bytes(PH_REGISTER, solution_pH);
        self._write_4_bytes(CALIBRATE_TEMPERATURE_REGISTER, tempC);

        self._send_command(CALIBRATE_HIGH_TASK);
        if (blocking):
            time.sleep(PH_PH_MEASUREMENT_TIME / 1000.0)

        self.getDeviceInfo();
        return self.status;

    @exception_catch
    def calibrateMid(self, solution_pH, tempC = 25.0, blocking = True):
        self._write_4_bytes(PH_REGISTER, solution_pH);
        self._write_4_bytes(CALIBRATE_TEMPERATURE_REGISTER, tempC);

        self._send_command(CALIBRATE_MID_TASK);
        if (blocking):
            time.sleep(PH_PH_MEASUREMENT_TIME / 1000.0)

        self.getDeviceInfo();
        return self.status;

    @exception_catch
    def calibrateLow(self, solution_pH, tempC = 25.0, blocking = True):
        self._write_4_bytes(PH_REGISTER, solution_pH);
        self._write_4_bytes(CALIBRATE_TEMPERATURE_REGISTER, tempC);

        self._send_command(CALIBRATE_LOW_TASK);
        if (blocking):
            time.sleep(PH_PH_MEASUREMENT_TIME / 1000.0)

        self.getDeviceInfo();
        return self.status;

    @exception_catch
    def getDeviceInfo(self):
        self.calibrationLowReading = self._read_4_bytes(CALIBRATE_READLOW_REGISTER);
        self.calibrationLowReference = self._read_4_bytes(CALIBRATE_REFLOW_REGISTER);
        self.calibrationMidReading = self._read_4_bytes(CALIBRATE_READMID_REGISTER);
        self.calibrationMidReference = self._read_4_bytes(CALIBRATE_REFMID_REGISTER);
        self.calibrationHighReading = self._read_4_bytes(CALIBRATE_READHIGH_REGISTER);
        self.calibrationHighReference = self._read_4_bytes(CALIBRATE_REFHIGH_REGISTER);
        self.calibrationSingleOffset = self._read_4_bytes(CALIBRATE_SINGLE_OFFSET_REGISTER);
        self.calibrationTemperature = self._read_4_bytes(CALIBRATE_TEMPERATURE_REGISTER);
        self.hwVersion = self._read_byte(HW_VERSION_REGISTER);
        self.fwVersion = self._read_byte(FW_VERSION_REGISTER);
        self.status = self._read_byte(STATUS_REGISTER);

    @exception_catch
    def measurepH(self, tempC = 25.0, blocking = True):
        self._write_4_bytes(TEMP_C_REGISTER, tempC);
        self._send_command(MEASURE_PH_TASK);
        if (blocking):
            time.sleep(PH_PH_MEASUREMENT_TIME / 1000.0)

        self._updateRegisters();

        return self.pH

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
        self._write_4_bytes(CALIBRATE_TEMPERATURE_REGISTER, NAN);

    @exception_catch
    def setDeviceInfo(self, calibrationLowReading, calibrationLowReference, calibrationMidReading, calibrationMidReference, calibrationHighReading, calibrationHighReference, calibrationSingleOffset, calibrationTemperature):
        self._write_4_bytes(CALIBRATE_REFHIGH_REGISTER, calibrationHighReference)
        self._write_4_bytes(CALIBRATE_REFLOW_REGISTER, calibrationLowReference)
        self._write_4_bytes(CALIBRATE_READMID_REGISTER, calibrationMidReading)
        self._write_4_bytes(CALIBRATE_REFMID_REGISTER, calibrationMidReference)
        self._write_4_bytes(CALIBRATE_READHIGH_REGISTER, calibrationHighReading)
        self._write_4_bytes(CALIBRATE_READLOW_REGISTER, calibrationLowReading)
        self._write_4_bytes(CALIBRATE_SINGLE_OFFSET_REGISTER, calibrationSingleOffset)
        self._write_4_bytes(CALIBRATE_TEMPERATURE_REGISTER, calibrationTemperature)

    @exception_catch
    def setI2CAddress(self, i2cAddress):
        self._write_4_bytes(PH_REGISTER, i2cAddress)
        self._send_command(I2C_TASK)
        self._address = i2cAddress

    @exception_catch
    def update(self):
        self._updateRegisters()

    @exception_catch
    def _updateRegisters(self):
        self.status = self._read_byte(STATUS_REGISTER);
        self.pH = self._read_4_bytes(PH_REGISTER);

        if (self.status != 0):

            self.pH = 0;
            self.mV = 0;

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