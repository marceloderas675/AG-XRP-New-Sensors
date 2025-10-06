from XRPLib.encoded_motor import EncodedMotor
from XRPLib.pid import PID
from XRPLib.timeout import Timeout
import time
import math

from pump import Pump
from moisture import MoistureSensor

class AgBot():
    @classmethod
    def get_default_agbot(cls):
        pump = Pump.get_default_pump()
        moisture = MoistureSensor.get_default_moisture_sensor()
        return AgBot(pump, moisture)
    
    def __init__(self, pump, moisture):
        self.pump = pump
        self.sensor = moisture

        self.stop()

    def stop(self):
        self.pump.stop()

    async def read(self):
        reading = self.sensor.read()
        return reading
    
    async def water(self, ml):
        await self.pump.water(ml)
        
if __name__ == "__main__":
    
    bot = AgBot.get_default_agbot()
    
    # encMotor1 = EncodedMotor.get_default_encoded_motor(1)
    # encMotor2 = EncodedMotor.get_default_encoded_motor(2)    
    # encMotor3 = EncodedMotor.get_default_encoded_motor(3)
    # encMotor4 = EncodedMotor.get_default_encoded_motor(4)
    
    # xy = XY(encMotor1, encMotor2, 385, 265)
    # z = Z(encMotor4)
    # pump = Pump(encMotor3)
    # ms = MoistureSensor()
    
    # gantry = AgBot.get_default_agbot(x_size = 385, y_size = 265)
    # gantry.manual()
