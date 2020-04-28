#!/bin/bash
PIDS=$(ps -C fbi -o pid=)
   
if [ -n "$PIDS" ]
  then
  sudo kill -HUP $PIDS > /dev/null 2>&1
  sudo kill -9 $PIDS > /dev/null 2>&1
fi

sudo dd if=/dev/zero of=/dev/fb0 > /dev/null 2>&1

exit $?
