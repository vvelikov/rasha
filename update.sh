#!/bin/bash
tempIN=$(cat /tmp/temp_hum.in | tr [:space:] \\n | head -n 1)
hum=$(cat /tmp/temp_hum.in | tr [:space:] \\n | tail -n 1)
tempOUT=$(cat /tmp/temp.out)
rrdtool update /var/www/html/tmp/Temp.rrd -t tempIN:tempOUT:hum N:$tempIN:tempOUT:hum
