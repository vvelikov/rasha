#!/usr/bin/python

import os
import os.path
import sys
import Adafruit_DHT

LOG = "/tmp/temp_hum.in"

humidity, temperature = Adafruit_DHT.read_retry(22, 4)

if os.path.isfile(LOG) and os.access(LOG, os.R_OK):
	os.system("rm /tmp/temp_hum.in")
else:
	os.system("touch /tmp/temp_hum.in")
mytemp = "{0:0.1f}".format(temperature)
myhum = "{0:0.1f}".format(humidity)
text_file = open(LOG, "w")
text_file.write(mytemp)
text_file.write(" ")
text_file.write(myhum)
text_file.close()

