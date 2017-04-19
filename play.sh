#!/bin/bash

LOG=`cat /tmp/status`

if [ "$LOG" -eq "0" ]; then
	echo " *** *** *** *** PLAY *** *** *** *** ";
	echo 1 > /tmp/status
	echo "." >/tmp/omfifo
fi
if [ "$LOG" -eq "1" ];then
	echo " *** *** *** *** PAUSE *** *** *** *** ";
	echo 2 > /tmp/status
	echo -n "p" >/tmp/omfifo
fi
if [ "$LOG" -eq "2" ]; then
    echo " *** *** *** *** UNPAUSE *** *** *** *** ";
    echo 1 > /tmp/status
    echo -n "p" >/tmp/omfifo
fi
