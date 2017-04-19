#!/bin/bash
echo -n "q" >/tmp/omfifo
sleep 2
echo "." >/tmp/omfifo
echo 1 > /tmp/status
