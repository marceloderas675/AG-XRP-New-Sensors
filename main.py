from machine import Pin
from XRPLib.encoded_motor import EncodedMotor
from moisture import MoistureSensor
import time



LED = Pin("LED", Pin.OUT)

# LED.value(1)
# 
motor = EncodedMotor.get_default_encoded_motor(4)
motor.set_effort(-1)
time.sleep(15)
motor.set_effort(0)
# 
# LED.value(0)

# s = MoistureSensor.get_default_moisture_sensor()
# 
# for i in range(100):
#     print(s.read())