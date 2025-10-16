import time
from machine import Pin, I2C
import stts22h
i2c = I2C(1, sda=Pin(18), scl=Pin(19)) # Correct I2C pins for RP2040
# for XRP beta use 18 & 19 for sda and scl respectively
# for XRP use 2 and 3
time.sleep(1)

devices = i2c.scan()

if not devices:
    print("No I2C devices found. Check Qwiic cable and power.")
else:
    print("Found devices:", [hex(d) for d in devices])

stts = stts22h.STTS22H(i2c)
stts.output_data_rate = stts22h.ODR_25_HZ
# can change above to be ODR_50_HZ, ODR_100_HZ, and ODR_200_HZ
while True:
    for output_data_rate in stts22h.output_data_rate_values:
        print("Current Output data rate setting: ", stts.output_data_rate)
        for _ in range(10):
            print(f"Temperature: {stts.temperature:.1f}°F")
            time.sleep(0.5)
        stts.output_data_rate = output_data_rate