#!/bin/bash

IP='8.8.8.8'

fping -c1 -t300 $IP 2>/dev/null 1>/dev/null
mpc stop

if [ "$?" = 0 ]
then
  echo "Online!"
  mpc clear -q
  mpc load streams
  mpc volume 10
  mpc play 1
  sleep 5
  mpc volume 15
  sleep 5
  mpc volume 25
  sleep 5
  mpc volume 35
  sleep 5
  mpc volume 45
  sleep 5
  mpc volume 55
  sleep 5
  mpc volume 65
  sleep 5
  mpc volume 75
  sleep 600
  mpc stop
else
  echo "Offline"
  mpc clear -q
  mpc load all
  mpc random on
  mpc repeat off
  mpc play
  sleep 5
  mpc volume 15
  sleep 5
  mpc volume 25
  sleep 5
  mpc volume 35
  sleep 5
  mpc volume 45
  sleep 5
  mpc volume 55
  sleep 5
  mpc volume 65
  sleep 5
  mpc volume 75
  sleep 600
  mpc stop
fi
