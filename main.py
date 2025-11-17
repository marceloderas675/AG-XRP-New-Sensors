import qwiic_veml6030
import sys
import time
from machine import Pin, I2C
import stts22h
import qwiic_oled
i2c = I2C(1, sda=Pin(18), scl=Pin(19)) # Correct I2C pins for RP2040
# for XRP beta use 18 & 19 for sda and scl respectively
# for XRP use 2 and 3
time.sleep(1)

devices = i2c.scan()

if not devices:
    print("No I2C devices found. Check Qwiic cable and power.")
else:
    print("Found devices:", [hex(d) for d in devices])

#set up temp
stts = stts22h.STTS22H(i2c)
stts.output_data_rate = stts22h.ODR_25_HZ

#set up light
light_sensor = qwiic_veml6030.QwiicVEML6030(address=0x48)
# Check if it's connected
if light_sensor.is_connected() == False:
     print("The device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
light_sensor.begin()

#set up oled
myOLED = qwiic_oled.QwiicMicroOled()
# 
if not myOLED.connected:
    print("The Qwiic Micro OLED device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
myOLED.begin()
myOLED.clear(myOLED.ALL)


# can change above to be ODR_50_HZ, ODR_100_HZ, and ODR_200_HZ
while True:
    
    ambient_light = light_sensor.read_light()
    for output_data_rate in stts22h.output_data_rate_values:
        print(f"Temperature: {stts.temperature:.1f}°F")
        print("Lux:\t%.1f" % ambient_light)
        myOLED.set_cursor(0,0)
        myOLED.print(f"Temp: {stts.temperature:.1f}°F")
        myOLED.set_cursor(0,10)
        myOLED.print("Lux:\t%.1f" % ambient_light)
        #myOLED.print(_)
        myOLED.display()
        myOLED.clear(myOLED.ALL)
        myOLED.clear(myOLED.PAGE)
        stts.output_data_rate = output_data_rate

