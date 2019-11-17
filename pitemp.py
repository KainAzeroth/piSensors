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
maxPoints = 5000
count = 0

while True:
    tempC = mcp.temperature
    tempF = tempC * 9 / 5 + 32
    currentDT = time.strftime('%X %x %Z')
    reportedTemp = ('{}\tTemp: {} C | {} F | {} Count'.format(currentDT, tempC, tempF, count))
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
