import qwiic_i2c
import time

#data sheet used:https://cdn.sparkfun.com/assets/3/0/b/7/6/STTS22h-Datasheet.pdf

_AVAILABLE_I2C_ADDRESS = 0x3C
#addresses are 60 (default)
_DEFAULT_NAME = "Qwiic STTS22H"

WHOAMI = 0x01
TEMP_H_LIMIT = 0x02
TEMP_L_LIMIT = 0x03
CTRL = 0x04
STATUS = 0x05
TEMP_L_OUT = 0x06
TEMP_H_OUT = 0x07

class QwiicSTTS22H(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS
def __init__(self, address=None, i2c_driver=None):
        """!
        Constructor

        @param int, optional address: The I2C address to use for the device
            If not provided, the default address is used
        @param I2CDriver, optional i2c_driver: An existing i2c driver object
            If not provided, a driver object is created
        """

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

        #self._doingPeriodicMeasurement = False

        # Set by read_measurement
        self._temperature = 0
        
def is_connected(self):
        """!
        Determines if this device is connected

        @return **bool** `True` if connected, otherwise `False`
        """
        # Check if connected by seeing if an ACK is received
        return self._i2c.isDeviceConnected(self.address)
    
def begin(self, LOW_ODR_START = 1):
    """!
    Initializes this device with default parameters

    @return **bool** Returns `True` if successful, otherwise `False`
    """
    # Confirm device is connected before doing anything
    if not self.is_connected():
        return False

#def checkStatus(self):

def readTemperature(self):
    bytesreadTHO = self._i2c.readBlock(self.TEMP_H_OUT, None, 8)
    bytesreadTHO = self._i2c.readBlock(self.TEMP_L_OUT, None, 8)

def operatingDataRate(self):        
        bytesreadCTRL = self._i2c.readBlock(self.CTRL, None, 7)
        #above means to read 7 bits on CTRL register
        FREERUN = bytesreadCTRL[4]
        ONE_SHOT = bytesreadCTRL[6]
        LOW_ODR_START = bytesreadCTRL[0]
        
        if (not LOW_ODR_START) and (not FREERUN):
            frequency = 1
            #1Hz
        elif ONE_SHOT:
            frequency = 1
            #1Hz
        elif FREERUN & AVG[1:0] == 0:
            frequency = 25
            #25Hz
        elif FREERUN & AVG[1:0] == 1:
            frequency = 50
            #50Hz
        elif FREERUN & AVG[1:0] == 2:
            frequency = 100
            #100Hz
        elif FREERUN & AVG[1:0] == 3:
            frequency = 200
            #200Hz
        else:
            frequency = 1

        return frequency
    #define frequency earlier


"""interrupt settings"""

def getInterruptHighC(self):
    #gets higher temperature threshold
    int32_t = retVal
    uint8_t = tempC
    
    retVal = 0
