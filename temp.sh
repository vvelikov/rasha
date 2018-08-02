
#!/bin/bash

# log
FILE="/tmp/temp.log"
# url temp out
URL1='http://www.wetter.com/deutschland/muenchen_stadt/wetterstation/DEXXX0266.html'
URL2='http://www.accuweather.com/en/de/munich/80331/weather-forecast/178086'
# dth22
SCRIPT="/home/pi/scripts/AdafruitDHT.py 22 4"
# temp & humidity inside
TEMPERATURE=`$SCRIPT | awk -F " " '{print $1}' | cut -d "=" -f2 | sed 's/*$//'`
HUMIDITY=`$SCRIPT | awk -F " " '{print $2}' | cut -d "=" -f2 | sed 's/%$//'`

# where to save?
# /tmp/temp ?
# 1 line temp in
# 2 line hum in
# 3 line temp out
# 4 line weather

if [ -f $FILE ]; then
    rm $FILE
    echo $TEMPERATURE > $FILE
    echo $HUMIDITY >> $FILE
    # temp OUT
    wget -q -O- "$URL1" | grep "text--white" | grep palm-hide | awk -F" " '{print $4}' | cut -d'>' -f2 | cut -d'<' -f1 | sed 's/..$//' | tr -s , . | sed 's/[^[:print:]\t]//g'   >> $FILE
    wget -q -O- "$URL2" | grep "cond" | head -n1 | awk -F'">' '{print $2}' | cut -d'<' -f1 >> $FILE
    # update rrds
    tempIN=$(cat /tmp/temp.log | head -n 1 | tr -d '\n')
    hum=$(cat /tmp/temp.log | tail -n 3 | head -n 1 | tr -d '\n')
    tempOUT=$(cat /tmp/temp.log | tail -n 2 | head -n 1 | tr -d '\n')
    rrdtool update /var/www/html/tmp/Temp.rrd -t tempIN:tempOUT:humidity N:$tempIN:$tempOUT:$hum
fi

exit $?




