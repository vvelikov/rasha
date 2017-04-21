#!/bin/bash

DT=`date +'%m/%d/%Y %T'`

echo " *** *** *** $DT *** *** *** "
echo " *** *** *** VOL UP *** *** *** "
echo -n "+" >/tmp/omfifo
exit 0
