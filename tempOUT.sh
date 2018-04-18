#!/bin/sh

URL='http://www.wetter.com/deutschland/muenchen_stadt/wetterstation/DEXXX0266.html'

wget -q -O- "$URL" | grep "text--white" | grep palm-hide | awk -F" " '{print $4}' | cut -d'>' -f2 | cut -d'<' -f1 | sed 's/..$//' > /tmp/temp.out
wget -q -O- "$URL" | grep "text--small" | grep "</span>" | head -n 14 | tail -n 1| awk -F'"' '{print $5}'| cut -d'<' -f1 | cut -d'>' -f2 > /tmp/weather.txt
