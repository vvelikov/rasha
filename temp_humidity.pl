#!/usr/bin/python3

import sys
import Adafruit_DHT

humidity, temperature = Adafruit_DHT.read_retry(22, 4)

if humidity is not None and temperature is not None:
    f = open("/var/log/rasha/tempIN", "w")
    f.write('{0:0.1f}'.format(temperature))
    f.close()
    p = open("/var/log/rasha/humidity","w")
    p.write('{0:0.1f}'.format(humidity))
    p.close()
    #    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
