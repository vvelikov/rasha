#!/usr/bin/python3
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

def main():
    time.sleep(1)
    lcd_status = "PLAYING"
    lcd_title = "Hello MOto"
    scrollText(lcd_status, lcd_title)
    time.sleep(1)
    print("DOne")


def scrollText(lcd_status, lcd_title):
    if lcd_status == "PLAYING":
     print("PLAYING")
    else:
        print("None")

if __name__ == '__main__':
  try:
	  main()

  except KeyboardInterrupt:
	  mylcd.lcd_clear()
	  sys.exit()

  finally:
	  mylcd.lcd_clear()
	  print ("Adeus!")
