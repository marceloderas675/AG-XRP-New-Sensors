import qwiic_veml6030
import sys
import time
from machine import Pin, I2C
import stts22h
import qwiic_oled
import qwiic_bme280
import qwiic_ens160
import qwiic_scd4x
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

#set up bme
bme_sensor = qwiic_bme280.QwiicBme280()

if bme_sensor.connected == False:
    print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
        file=sys.stderr)

bme_sensor.begin()

#set up ens
myEns = qwiic_ens160.QwiicENS160()

if myEns.is_connected() == False:
    print("The device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
myEns.begin()
myEns.set_operating_mode(myEns.kOpModeReset)
myEns.set_operating_mode(myEns.kOpModeStandard)
ensStatus = myEns.get_flags()

#set up oled
myOLED = qwiic_oled.QwiicMicroOled()
# 
if not myOLED.connected:
    print("The Qwiic Micro OLED device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
myOLED.begin()
myOLED.clear(myOLED.ALL)

#co2 and stuff sensor set up
mySCD4x = qwiic_scd4x.QwiicSCD4x() 

# Check if it's connected
if mySCD4x.is_connected() == False:
    print("The device isn't connected to the system. Please check your connection", file=sys.stderr)

# Initialize the device
if mySCD4x.begin() == False:
    print("Error while initializing device", file=sys.stderr)

# can change above to be ODR_50_HZ, ODR_100_HZ, and ODR_200_HZ
while True:
    
    ambient_light = light_sensor.read_light()
    print(f"Temperature: {stts.temperature:.1f}°F")
    print("Lux:\t%.1f" % ambient_light)
    myOLED.set_cursor(0,0)
    myOLED.print(f"Temp: {stts.temperature:.1f}°F")
    myOLED.set_cursor(0,10)
    myOLED.print("Lux:\t%.1f" % ambient_light)
    #myOLED.print(_)
    myOLED.display()
    print("Humidity:\t%.3f" % bme_sensor.humidity)
    print("Pressure:\t%.3f" % bme_sensor.pressure)
    print("Altitude:\t%.3f" % bme_sensor.altitude_feet)
    print("Temperature:\t%.2f" % bme_sensor.temperature_fahrenheit)
    if myEns.check_data_status():
        print("Air Quality Index (1-5) : ", myEns.get_aqi())
        print("Total Volatile Organic Compounds (ppb): ", myEns.get_tvoc())
        print("CO2 concentration (ppm): ", myEns.get_eco2())
        print("Gas Sensor Status Flag (0 - Standard, 1 - Warm up, 2 - Initial Start Up): ", myEns.get_flags())
    if mySCD4x.read_measurement(): # This must be called to get new data. It will return false until new data is available 
        print("\nCO2(ppm):", mySCD4x.get_co2())
        print("Temperature(C):", mySCD4x.get_temperature())
        print("Humidity(%RH):", mySCD4x.get_humidity())
    time.sleep(1)
    myOLED.clear(myOLED.ALL)
    myOLED.clear(myOLED.PAGE)

