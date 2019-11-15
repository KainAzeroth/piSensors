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

while True:
    tempFile = open("temp.txt", "a")
    tempC = mcp.temperature
    tempF = tempC * 9 / 5 + 32
    currentDT = time.strftime('%X %x %Z')
    reportedTemp = ('{}\tTemp: {} C | {} F '.format(currentDT, tempC, tempF))
    print(reportedTemp)
    print(reportedTemp, file=tempFile)
    time.sleep(2)
    tempFile.close()

