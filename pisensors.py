# Raspberry Pi temperature and Humidity sensor using adafruit breakout boards MCP9808 and SHT31-D.
# Code based on files from Adafruit mostly and cobbled together by me

import time
import board
import busio
import adafruit_mcp9808
import adafruit_sht31d

# Adding color with colorama
import colorama
from colorama import Fore, Style

# This example shows how to get the temperature from a MCP9808 board
i2c_bus = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c_bus, 0x1b)
sht = adafruit_sht31d.SHT31D(i2c_bus, 0x44)

# Settings
maxPoints = 5000 #Max data points to keep in the file. Really badly done. Restarts the file at this number instead of removing a line and adding a new one
sleepTimer = 1 #This is the number of seconds between checking the sensor. Kinda like a polling rate in seconds. Values between 1 and 3600 seconds
lowTemp = 70 #Warning when temp is below this
highTemp = 80 #Warning when temp is above this

# Loop counts
countA = 0
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
    mcpTempCR = format(round(mcpTempC,3), '.3f')
    mcpTempFR = format(round(mcpTempF,3), '.3f')

    shtTempC = sht.temperature
    shtTempF = shtTempC * 1.8 + 32
    shtTempCR = round(shtTempC,3)
    shtTempFR = round(shtTempF,3)
    shtHumidity = format(round(sht.relative_humidity,3), '.3f')

    reportedTemp = f"{currentDT} | {mcpTempCR} C | {mcpTempFR} F | {shtHumidity}%"

#    OLD FORMAT
#    reportedTemp = f"{currentDT} | {mcpTempCR} mC | {mcpTempFR} mF | {shtTempCR} sC | {shtTempFR} sF | {shtHumidity} % RH"

    if mcpTempF > highTemp:
        print(Fore.RED + reportedTemp + Style.RESET_ALL, end='\r')
    elif mcpTempF < lowTemp:
        print(Fore.CYAN + reportedTemp +Style.RESET_ALL, end='\r')
    else:
        print(reportedTemp, end='\r')

    if countA < maxPoints:
        tempFile = open("temp.txt", "a")
        print(reportedTemp, file=tempFile)
        countA = countA + 1
        time.sleep(sleepTimer)
        tempFile.close()

    if countA >= maxPoints:
        tempFile = open("temp.txt", "w")
        print(reportedTemp, file=tempFile)
        countA = 0
        time.sleep(sleepTimer)
        tempFile.close()

    loopcount += 1

#   This is turning on the heater on the SHT31-D because it was in some tutorials
#   it happens every 10 sensor checks. There are two lines to print the action, just uncomment them.
    if loopcount == 10:
        loopcount = 0
        sht.heater = True
#        print("SHT31-D Heater status =", sht.heater) 
        time.sleep(1)
        sht.heater = False
#        print("SHT31-D Heater status =", sht.heater)
