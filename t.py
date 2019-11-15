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
	scrollText("Hello Moto", 2)
	time.sleep(1)
	print("DOne")

def scrollText(long_string, rowNo):
	long_string = long_string + " " 					# add space at the end
	str_pad = " " * 16
	mylcd.lcd_display_string(long_string[:16], rowNo)
	time.sleep(0.5)
	for i in range (0, len(long_string)):
	  lcd_text = long_string[i:(i+16)]
	  mylcd.lcd_display_string(lcd_text,rowNo)
	  time.sleep(0.14) # adjust this to a comfortable value
	mylcd.lcd_display_string(str_pad,rowNo)
	mylcd.lcd_display_string(long_string[:16], rowNo)# Main


if __name__ == '__main__':
  try:
	  main()

  except KeyboardInterrupt:
	  mylcd.lcd_clear()
	  sys.exit()

  finally:
	  mylcd.lcd_clear()
	  print ("Adeus!")
