#!/bin/bash

LOG=`cat /tmp/statusp`

if [ "$LOG" -eq "0" ]; then
	echo " *** *** *** *** [PEPPA] PLAY *** *** *** *** ";
	echo 1 > /tmp/statusp
	echo "." >/tmp/omfifop
fi
if [ "$LOG" -eq "1" ];then
	echo " *** *** *** *** [PEPPA] PAUSE *** *** *** *** ";
	echo 2 > /tmp/statusp
	echo -n "p" >/tmp/omfifop
fi
if [ "$LOG" -eq "2" ]; then
        echo " *** *** *** *** [PEPPA] UNPAUSE *** *** *** *** ";
        echo 1 > /tmp/statusp
        echo -n "p" >/tmp/omfifop
fi
