#!/bin/bash
#fbi -a -t 1 --blend 200 --readahead --noverbose -T 1 -u /mnt/pix/* >/dev/null 2>&1
#sudo fbi -v -d /dev/fb0 -a -t 5 --noverbose --readahead -u /mnt/pix/* > /dev/null 2>&1
sudo /usr/bin/fbi -d /dev/fb0 -T 1 -a --noverbose --readahead -u -t 5 -l /mnt/pix/pix.txt
