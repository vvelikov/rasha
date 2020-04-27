#!/bin/bash
date=$(date +'%F %R')
echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" >> /var/log/rasha/radio.log
echo "$date  DAILY RESET                   " >> /var/log/rasha/radio.log
echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" >> /var/log/rasha/radio.log
echo 0 > /var/log/rasha/counter
