#!/bin/bash
# log
FILE="/logs/temp.log"
TMP="/logs/temp"
# url temp out & weather
URL='http://api.openweathermap.org/data/2.5/weather?q=Munich&APPID=062022b66b18e6ab7dec7f8deb26b1ce&units=metric'
# dth22
SCRIPT="/home/pi/scripts/AdafruitDHT.py 22 4"
# temp & humidity inside
TEMPERATURE=`$SCRIPT | awk -F " " '{print $1}' | cut -d "=" -f2 | sed 's/*$//'`
HUMIDITY=`$SCRIPT | awk -F " " '{print $2}' | cut -d "=" -f2 | sed 's/%$//'`

# where to save?
# /logs/temp ?
# 1 line temp in
# 2 line hum in
# 3 line temp out
# 4 line weather

if [ -f $FILE ]; then
    rm $FILE
    echo $TEMPERATURE > $FILE
    echo $HUMIDITY >> $FILE
	# temp OUT
	wget -q -O- "$URL" > $TMP
	if [ -s $TMP ]; then
   	   cat $TMP | awk -F "temp" '{print $2}' | cut -d ":" -f2 | cut -d "," -f1 | xargs printf "%.*f\n" 1 >> $FILE
	fi
	if [ -s $TMP ]; then
	   cat $TMP | awk -F "description" '{print $2}' | cut -d "," -f1 | tr -d '\"' | tr -d ":"  >> $FILE
	fi
	# update rrds
	tempIN=$(cat /logs/temp.log | head -n 1 | tr -d '\n')
	hum=$(cat /logs/temp.log | tail -n 3 | head -n 1 | tr -d '\n')
	tempOUT=$(cat /logs/temp.log | tail -n 2 | head -n 1 | tr -d '\n')
	rrdtool update /var/www/html/tmp/Temp.rrd -t tempIN:tempOUT:humidity N:$tempIN:$tempOUT:$hum
fi
if [ -f $TMP ]; then
	rm $TMP
fi

exit $?
