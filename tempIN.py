#!/usr/bin/python

import os
import sys
import Adafruit_DHT

humidity, temperature = Adafruit_DHT.read_retry(22, 4)

log = "/tmp/temp_hum.in"
if os.path.isfile(log):
    os.system("rm /tmp/temp_hum.in")
else:
    mytemp = "{0:0.1f}".format(temperature)
    myhum = "{0:0.1f}".format(humidity)
    text_file = open(log, "w")
    text_file.write(mytemp)
    text_file.write(" ")
    text_file.write(myhum)
    text_file.close()
