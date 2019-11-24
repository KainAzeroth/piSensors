# piSensors
Basic temperature and humidity sensor program to read a MCP9808 and SHT31-D breakout sensors from Adafruit on a Raspberry Pi over i2c.

I hope to turn this into a more substantial project over time by adding sensors. The Pi this will end up in eventually is currently running Pi-hole on my network. It is in a network cabinet/server area, hence the sensor monitoring. 
I was kind of inspired by Padd.sh, which gives you a nice read out and stats from pi-hole in the terminal. One of the things it displays is the temperature of the Pi CPU (I think it's the CPU, whatever, the Pi gives a temp).
I thought it would be nice to get some other readings like ambient temperature, humidity, air quality, etc. and display them in a way similar to Padd or maybe an expanded Padd instance.

So far... just a janky python program asking for temperature/humidity and displaying it in terminal and a file. Kind of boring?

Oh yeah, and I don't actually know Python. Learning as we go! 
