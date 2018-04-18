#!/bin/bash

LOG=`cat /tmp/statusb`

if [ "$LOG" -eq "0" ]; then
#	echo " *** *** *** *** PLAY *** *** *** *** ";
	echo 1 > /tmp/statusb
	echo "." >/tmp/omfifob
fi
if [ "$LOG" -eq "1" ];then
#	echo " *** *** *** *** PAUSE *** *** *** *** ";
	echo 2 > /tmp/statusb
	echo -n "p" >/tmp/omfifob
fi
if [ "$LOG" -eq "2" ]; then
#        echo " *** *** *** *** UNPAUSE *** *** *** *** ";
        echo 1 > /tmp/statusb
        echo -n "p" >/tmp/omfifob
fi
