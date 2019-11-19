# Raspberry Pi temperature sensor usind adafruit breakout board for MCP9808.
# Code based on files from Adafruit.

import time
import board
import busio
import adafruit_mcp9808
import datetime

# This example shows how to get the temperature from a MCP9808 board
i2c_bus = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9808.MCP9808(i2c_bus)

maxPoints = 5000 #Max data points to keep in the file. Really badly done. Restarts the file at this number instead of removing a line and adding a new one
count = 0

while True:
    tempC = mcp.temperature
    tempF = tempC * 9 / 5 + 32
    currentDT = time.strftime('%X %x %Z')
    reportedTemp = f"{currentDT}\tTemp: {tempC} C | {tempF} F | {count} Count"

    if tempF < 50:
        reportedTemp = reportedTemp + " COLD WARNING! HOT WARNING!"
    elif tempF < 60:
        reportedTemp = reportedTemp + " Cool"
    elif tempF < 70:
        reportedTemp = reportedTemp + " Moderate"
    elif tempF < 80:
        reportedTemp = reportedTemp + " Warm"
    elif tempF < 90:
        reportedTemp = reportedTemp + " HOT WARNING! HOT WARNING!"

    print(reportedTemp)

    if count < maxPoints:
        tempFile = open("temp.txt", "a")
        print(reportedTemp, file=tempFile)
        count = count + 1
        time.sleep(2)
        tempFile.close()

    if count >= maxPoints:
        tempFile = open("temp.txt", "w")
        print(reportedTemp, file=tempFile)
        count = 0
        time.sleep(2)
        tempFile.close()
