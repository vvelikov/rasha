#!/bin/bash

LOG=`cat /tmp/statusp`

if [ "$LOG" -eq "0" ]; then
	echo " *** *** *** *** PLAY *** *** *** *** ";
	echo 1 > /tmp/statusp
	echo "." >/tmp/omfifop
fi
if [ "$LOG" -eq "1" ];then
	echo " *** *** *** *** PAUSE *** *** *** *** ";
	echo 2 > /tmp/statusp
	echo -n "p" >/tmp/omfifop
fi
if [ "$LOG" -eq "2" ]; then
        echo " *** *** *** *** UNPAUSE *** *** *** *** ";
        echo 1 > /tmp/statusp
        echo -n "p" >/tmp/omfifop
fi
