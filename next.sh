#!/bin/bash
echo -n "q" >/tmp/omfifo
sleep 1
echo "." >/tmp/omfifo
echo 1 > /tmp/status
