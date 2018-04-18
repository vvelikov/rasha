#!/bin/bash
tempIN=$(cat /tmp/temp_hum.in | tr [:space:] \\n | head -n 1 | tr -d '\n')
hum=$(cat /tmp/temp_hum.in | tr [:space:] \\n | tail -n 1)
tempOUT=$(cat /tmp/temp.out | tr -d '\n')
rrdtool update /var/www/html/tmp/Temp.rrd -t tempIN:tempOUT:humidity N:$tempIN:$tempOUT:$hum
