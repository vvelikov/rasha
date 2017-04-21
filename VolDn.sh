#!/bin/bash

DT=`date +'%m/%d/%Y %T'`

echo " *** *** *** $DT *** *** *** "
echo " *** *** *** VOL DOWN *** *** *** "
echo -n "-" >/tmp/omfifo
exit 0
