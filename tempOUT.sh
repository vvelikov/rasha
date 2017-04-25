#!/bin/sh

URL='http://www.accuweather.com/en/de/munich/80331/weather-forecast/178086'
wget -q -O- "$URL" | awk -F\' '/acm_RecentLocationsCarousel\.push/{print $10 }'| head -1 | awk '{printf ("%.1f\n", $1)}' > /tmp/temp.out
sleep 1
wget -q -O- "$URL" | awk -F\' '/acm_RecentLocationsCarousel\.push/{print "Munich:" $13 " " "Temp:" $10 "°" " " "Realfeel:" $12"°"'} | head -n 1| sed 's/text://g' | sed 's|["});,]||g' | tr -s " " > /tmp/weather.txt
