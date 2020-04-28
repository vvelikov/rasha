#!/bin/bash
# log
tempIN="/var/log/rasha/tempIN"
humidity="/var/log/rasha/humidity"
tempOUT="/var/log/rasha/tempOUT"
feelslike="/var/log/rasha/feelslike"
weather="/var/log/rasha/weather"
TMP="/tmp/temp"
# url temp out & weather
URL='http://api.openweathermap.org/data/2.5/weather?q=Munich&APPID=062022b66b18e6ab7dec7f8deb26b1ce&units=metric'

# where to save?
# /logs/temp ?
# 1 line temp in
# 2 line hum in
# 3 line temp out
# 4 line weather

if [ -f $tempIN ]; then
	# temp OUT
	wget -q -O- "$URL" > $TMP
	if [ -s $TMP ]; then
   	   cat $TMP | awk -F "temp" '{print $2}' | cut -d ":" -f2 | cut -d "," -f1 | xargs printf "%.*f\n" 1 > $tempOUT
	fi
	if [ -s $TMP ]; then
	   cat $TMP | awk -F "description" '{print $2}' | cut -d "," -f1 | tr -d '\"' | tr -d ":"  > $weather
	fi
	if [ -s $TMP ]; then
	  cat $TMP | awk -F "feels_like" '{print $2}' | cut -d "," -f1 | tr -d '\"' | tr -d ":" | xargs printf "%.*f\n" 1 > $feelslike
	fi
	# update rrds
	t=$(cat /var/log/rasha/tempIN |  tr -d '\n')
	h=$(cat /var/log/rasha/humidity | tr -d '\n')
	tO=$(cat /var/log/rasha/tempOUT | tr -d '\n')
	rrdtool update /var/www/html/tmp/Temp.rrd -t tempIN:tempOUT:humidity N:$t:$tO:$h
fi
if [ -f $TMP ]; then
	rm $TMP
fi

exit $?
