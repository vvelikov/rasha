 #!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import PIPE, Popen
import I2C_LCD_driver
import RPi.GPIO as GPIO
import subprocess
import datetime
import socket
import time
import sys
import os, random

mylcd = I2C_LCD_driver.lcd()
str_pad = " " * 16
title_cmd = "dbuscontrol.sh getsource | awk -F '/' '{print $4}' | cut -d '.' -f1 | tr -d '\n'"
date_cmd = "date +%R | tr -d '\n'"
date_time_cmd = "date +'%d-%m-%Y %H:%M:%S'"
limit = 6                   # only 6 videos are allowed per day Barba/Peppa = 1 Masha = 1.2 Conni = 2
counter = 0                 # counter starts at 0

def main():
    play_video("/mnt/Barba/")

def play_video(str):
    global counter
    time_play = time.time()
    if check_limit(counter):
     do_limit(str)
     file = randomplay(str)
     omxproc = Popen(['omxplayer', file, '-b', '-r', '-o', 'alsa:hw:0,0'], stdout=subprocess.PIPE, close_fds=True)
     while omxproc.poll() is None:
      my_title = str_pad + get_title()
      print(my_title)
    else:
     show_error()


def randomplay(str):
    randomfile = random.choice(os.listdir( str ))
    file = str + randomfile
    return file

def get_date():
    d = subprocess.check_output(date_cmd, shell=True, stderr=subprocess.STDOUT)
    return d

def get_date_time():
    t = subprocess.check_output(date_time_cmd, shell=True, stderr=subprocess.STDOUT)
    return t

def get_title():
    t = Popen(title_cmd, shell=True, stdout=PIPE)
    title = t.communicate()[0]
    return title

def show_error():
    os.system("dbuscontrol.sh stop")
    time.sleep(3)

def do_limit(str):
    global counter
    if ( str == "/mnt/Peppa/"):
        counter+=1
    elif ( str == "/mnt/Barba/"):
        counter+=1
    elif ( str == "/mnt/Masha/"):
        counter+=1.2
    else:
        counter+=2

def check_limit(counter):
    if counter < limit:
        return True
    else:
        return False

# Main
if __name__ == '__main__':
  try:
      main()

  except KeyboardInterrupt:
      mylcd.lcd_clear()
      sys.exit()

  finally:
      mylcd.lcd_clear()
      print "Adeus!"
