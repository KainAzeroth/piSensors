# Raspberry Pi temperature and Humidity sensor using adafruit breakout boards MCP9808 and SHT31-D.
# Code based on files from Adafruit mostly and cobbled together by me

import time
import board
import busio
import adafruit_mcp9808
import adafruit_sht31d

# This example shows how to get the temperature from a MCP9808 board
i2c_bus = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c_bus, 0x1b)
sht = adafruit_sht31d.SHT31D(i2c_bus, 0x44)

maxPoints = 5000 #Max data points to keep in the file. Really badly done. Restarts the file at this number instead of removing a line and adding a new one
sleepTimer = 2 #This is the number of seconds between checking the sensor. Kinda like a polling rate in seconds. Values between 1 and 3600 seconds
count = 0
loopcount  = 0

while True:
    #checking to make sure the sleepTimer isn't set to something stupid
    if sleepTimer < 1: #if less than 1 set to 1. Minimum is 1 second.
        sleepTimer = 1
    elif sleepTimer > 3600: #if more than 3600 set to 3600. This is 1 hour in seconds. More than that seems silly. 
        sleepTimer = 3600

    currentDT = time.strftime('%X %x %Z')

    mcpTempC = mcp.temperature
    mcpTempF = mcpTempC * 1.8 + 32
    mcpTempCR = round(mcpTempC,3)
    mcpTempFR = round(mcpTempF,3)

    shtTempC = sht.temperature
    shtTempF = shtTempC * 1.8 + 32
    shtTempCR = round(shtTempC,3)
    shtTempFR = round(shtTempF,3)
    shtHumidity = round(sht.relative_humidity,3)


    reportedTemp = f"{currentDT} | {mcpTempCR} mC | {mcpTempFR} mF | {shtTempCR} sC | {shtTempFR} sF | {shtHumidity} % RH"

#    if tempF < 50:
#        reportedTemp = reportedTemp + " | COLD WARNING! HOT WARNING!"
#    elif tempF < 60:
#        reportedTemp = reportedTemp + " | Cool"
#    elif tempF < 70:
#        reportedTemp = reportedTemp + " | Moderate"
#    elif tempF < 80:
#        reportedTemp = reportedTemp + " | Warm"
#    elif tempF < 90:
#        reportedTemp = reportedTemp + " | HOT WARNING! HOT WARNING!"

    print(reportedTemp)

    if count < maxPoints:
        tempFile = open("temp.txt", "a")
        print(reportedTemp, file=tempFile)
        count = count + 1
        time.sleep(sleepTimer)
        tempFile.close()

    if count >= maxPoints:
        tempFile = open("temp.txt", "w")
        print(reportedTemp, file=tempFile)
        count = 0
        time.sleep(sleepTimer)
        tempFile.close()

    loopcount += 1

    if loopcount == 10:
        loopcount = 0
        sht.heater = True
        print("SHT31-D Heater status =", sht.heater)
        time.sleep(1)
        sht.heater = False
        print("SHT31-D Heater status =", sht.heater)
