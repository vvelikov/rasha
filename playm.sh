#!/bin/bash

LOG=`cat /tmp/statusm`

if [ "$LOG" -eq "0" ]; then
	echo 1 > /tmp/statusm
	echo "." >/tmp/omfifom
fi
if [ "$LOG" -eq "1" ];then
	echo 2 > /tmp/statusm
	echo -n "p" >/tmp/omfifom
fi
if [ "$LOG" -eq "2" ]; then
        echo 1 > /tmp/statusm
        echo -n "p" >/tmp/omfifom
fi
