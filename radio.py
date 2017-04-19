#!/usr/bin/python

from subprocess import PIPE, Popen
import Adafruit_DHT
import I2C_LCD_driver
import RPi.GPIO as GPIO
import subprocess
import time
import sys
import os

# Define GPIO for button control
PREV = 17
PLAY = 27
NEXT = 24
DOWN = 18
UP = 23

# set GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP)

# custom icons
speaker_icon = [
	     [ 0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b10001, 0b10001, 0b10001 ],   # Volume
	     [ 0b00001, 0b00011, 0b00101, 0b01001, 0b10001, 0b00001, 0b00001, 0b00001 ],   # Volume
	     [ 0b10001, 0b10001, 0b10001, 0b11111, 0b00000, 0b00000, 0b00000, 0b00000 ],   # Volume
	     [ 0b00001, 0b00001, 0b00001, 0b10001, 0b01001, 0b00101, 0b00011, 0b00001 ],   # Volume
	     [ 0b00001, 0b00011, 0b00101, 0b01001, 0b01011, 0b11011, 0b11000, 0b00000 ],   # note
	     [ 0b00100, 0b01010, 0b01010, 0b01110, 0b01110, 0b11111, 0b11111, 0b01110 ],   # thermometer
	     [ 0b00001, 0b00001, 0b00101, 0b00101, 0b10101, 0b10101, 0b10101, 0b10101 ]    # wifi
]
# dth22
humidity, temperature = Adafruit_DHT.read_retry(22, 4)

# Define some device constants
mylcd = I2C_LCD_driver.lcd()
str_pad = " " * 16

# some definitions for status menu
video_cmd = "tail -n 1 /tmp/video.log | awk -F'/' '{print $4}' | sed 's/\..\{3\}$//' | tr -d '\n'"
wifi_cmd = "iwconfig wlan0| grep Signal | awk '{print $4}' | cut -d '=' -f2 | cut -d '/' -f1"
radio_cmd = "mpc current -f [%title%] | tr -d '\n'"
ip_cmd = "ifconfig wlan0 | grep 'inet\ addr' | cut -d: -f2 | cut -d' ' -f1 | tr -d '\n'"

# load custom icons
mylcd.lcd_load_custom_chars(speaker_icon)

def main():
  mylcd.lcd_clear() # clear screen
  mylcd.lcd_display_string(" --> rage'z <-- ",1)
  mylcd.lcd_display_string(" Music/Video PL ",2)
  main_menu()

def main_menu():
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mytime = get_date() 
    mytime = mytime[11:-14]
    mytemp = "{:.0f}".format(temperature)
    mywifi = get_wifi_signal()
    mystring = mytime + " " + chr(5) + ":" + mytemp + chr(223) + " " + chr(6) + ":" + mywifi
    mylcd.lcd_display_string(mystring,1)
    mylcd.lcd_display_string("< Off     Menu >",2)
   else:
    if ( GPIO.input(NEXT) == False):
     video_menu()
    if (GPIO.input(PREV) == False):
     off_menu()

def off_menu():
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mytime = get_date() 
    mytime = mytime[11:-14]
    mytemp = "{:.0f}".format(temperature)
    mywifi = get_wifi_signal()
    mystring = mytime + " " + chr(5) + ":" + mytemp + chr(223) + " " + chr(6) + ":" + mywifi
    mylcd.lcd_display_string(mystring,1)
    mylcd.lcd_display_string("[GO]  < Reboot >",2)
   else:
    if ( GPIO.input(PLAY) == False):
     reboot()
    if ( GPIO.input(PREV) == False):
     main_menu()
    if ( GPIO.input(NEXT) == False):
     shutdown_menu()

def shutdown_menu(): # Shutdown
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mytime = get_date() 
    mytime = mytime[11:-14]
    mytemp = "{:.0f}".format(temperature)
    mywifi = get_wifi_signal()
    mystring = mytime + " " + chr(5) + ":" + mytemp + chr(223) + " " + chr(6) + ":" + mywifi
    mylcd.lcd_display_string(mystring,1)
    mylcd.lcd_display_string("[GO]    < Halt >",2)
   else:
    if ( GPIO.input(PLAY) == False):
     shutdown()
    if ( GPIO.input(PREV) == False):
     main_menu()
    if ( GPIO.input(NEXT) == False):
     ip_menu()

def ip_menu(): # Shutdown
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mytime = get_date() 
    mytime = mytime[11:-14]
    mytemp = "{:.0f}".format(temperature)
    mywifi = get_wifi_signal()
    mystring = mytime + " " + chr(5) + ":" + mytemp + chr(223) + " " + chr(6) + ":" + mywifi
    mylcd.lcd_display_string(mystring,1)
    mylcd.lcd_display_string("[GO]     < IP > ",2)
   else:
    if ( GPIO.input(PLAY) == False):
     ip()
    if ( GPIO.input(PREV) == False):
     main_menu()
    if ( GPIO.input(NEXT) == False):
     off_menu()

def iradio_menu(): # iRadio
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mytime = get_date()
    mytime = mytime[11:-14]
    mytemp = "{:.0f}".format(temperature)
    mywifi = get_wifi_signal()
    mystring = mytime + " " + chr(5) + ":" + mytemp + chr(223) + " " + chr(6) + ":" + mywifi
    mylcd.lcd_display_string(mystring,1)
    mylcd.lcd_display_string("[GO]  < iRadio >",2)
   else:
    if ( GPIO.input(PLAY) == False):
     choose1()
    if ( GPIO.input(PREV) == False):
     main_menu()
    if ( GPIO.input(NEXT) == False):
     music_menu()

def video_menu(): # Video
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mytime = get_date()
    mytime = mytime[11:-14]
    mytemp = "{:.0f}".format(temperature)
    mywifi = get_wifi_signal()
    mystring = mytime + " " + chr(5) + ":" + mytemp + chr(223) + " " + chr(6) + ":" + mywifi
    mylcd.lcd_display_string(mystring,1)
    mylcd.lcd_display_string("[GO]   < Masha >",2)
   else:
    if ( GPIO.input(PLAY) == False):
     play_video()
    if ( GPIO.input(NEXT) == False):
     iradio_menu()
    if ( GPIO.input(PREV) == False):
     main_menu()

def music_menu(): # local music/videos
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mytime = get_date()
    mytime = mytime[11:-14]
    mytemp = "{:.0f}".format(temperature)
    mywifi = get_wifi_signal()
    mystring = mytime + " " + chr(5) + ":" + mytemp + chr(223) + " " + chr(6) + ":" + mywifi
    mylcd.lcd_display_string(mystring,1)
    mylcd.lcd_display_string("[GO]   < Music >",2)
    time.sleep(0.1)
   else:
    if ( GPIO.input(PLAY) == False):
     play_music()
    if ( GPIO.input(NEXT) == False):
     video_menu()
    if ( GPIO.input(PREV) == False):
     main_menu()

def play_music():
    lcd_status = "PLAYING"
    mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
    os.system("mpc clear")
    os.system("mpc load all")
    os.system("mpc random")
    os.system("mpc repeat off")
    os.system("mpc play")
    time.sleep(0.2)
    while(1):
     my_title = str_pad + get_radio_title()
     for i in range (0, len(my_title)):
      lcd_text = my_title[i:(i+16)]
      mylcd.lcd_display_string(lcd_text,2)
      time.sleep(0.4)
      mylcd.lcd_display_string(str_pad,2)
      mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
      time.sleep(0.1)
      mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
      time.sleep(0.1)
      if ( GPIO.input(UP) == False):
       display_volume()
       os.system("mpc volume +10")
       display_volume()
       time.sleep(0.5)
       mylcd.lcd_display_string("                ",1)
       mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
      if ( GPIO.input(DOWN) == False):
       display_volume()
       os.system("mpc volume -10")
       display_volume()
       time.sleep(0.5)
       mylcd.lcd_display_string("                ",1)
       mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
      if ( GPIO.input(PLAY) == False):
       os.system("mpc stop")
       time.sleep(0.2)
       main_menu()
      if ( GPIO.input(NEXT) == False):
       mylcd.lcd_display_string("                ",1)
       mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
       os.system("mpc next")
       time.sleep(0.2)
      if ( GPIO.input(PREV) == False):
       os.system("mpc prev")
       time.sleep(0.2)

def play_video():
    lcd_status = "PLAYING"
    os.system("/home/pi/scripts/play.sh")
    time.sleep(0.5)
    while(1):
     my_title = str_pad + get_video_title()
     for i in range (0, len(my_title)):
      lcd_text = my_title[i:(i+16)]
      mylcd.lcd_display_string(lcd_text,2)
      time.sleep(0.4)
      mylcd.lcd_display_string(str_pad,2)
      mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
      time.sleep(0.1)
      mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
      time.sleep(0.1)
      f = os.popen("cat /tmp/status | tr -d '\n'")
      time.sleep(0.2)
      for i in f.readlines():
        status = int(i)
        if status == 1:
         lcd_status = "PLAYING"
         mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
        elif status == 2:
	 lcd_status = "PAUSED"
         mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
	elif status == 0:
         lcd_status = "STOPPED"
         mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
         time.sleep(2)
         video_menu()
      if ( GPIO.input(UP) == False):
       os.system("echo -n '+' >/tmp/omfifo")
      if ( GPIO.input(DOWN) == False):
       os.system("echo -n '-' >/tmp/omfifo")
      if ( GPIO.input(PLAY) == False):
       os.system("/home/pi/scripts/play.sh")
      if ( GPIO.input(NEXT) == False):
       os.system("/home/pi/scripts/next.sh")
      if ( GPIO.input(PREV) == False):
       os.system("/home/pi/scripts/stop.sh")
       time.sleep(0.5)
       main_menu()

def choose1():
    time.sleep(0.5)
    while(1):
     if ( GPIO.input(PREV) == False):
      iradio_menu()
     if ( GPIO.input(PLAY) == False):
      station1()
     if ( GPIO.input(NEXT) == False):
      choose2()
     else:
      mylcd.lcd_display_string(" Choose Station ",1)
      mylcd.lcd_display_string("[GO] < ChilHop >",2)

def choose2():
    time.sleep(0.5)
    while(1):
     if ( GPIO.input(PREV) == False):
      choose1()
     if ( GPIO.input(PLAY) == False):
      station2()
     if ( GPIO.input(NEXT) == False):
      choose3()
     else:
      mylcd.lcd_display_string(" Choose Station ",1)
      mylcd.lcd_display_string("[GO] < ChilOut >",2)

def choose3():
    time.sleep(0.5)
    while(1):
     if ( GPIO.input(PREV) == False):
      choose2()
     if ( GPIO.input(PLAY) == False):
      station3()
     if ( GPIO.input(NEXT) == False):
      choose4()
     else:
      mylcd.lcd_display_string(" Choose Station ",1)
      mylcd.lcd_display_string("[GO]  < LiqDnB >",2)

def choose4():
    time.sleep(0.5)
    while(1):
     if ( GPIO.input(PREV) == False):
      choose3()
     if ( GPIO.input(PLAY) == False):
      station4()
     if ( GPIO.input(NEXT) == False):
      choose5()
     else:
      mylcd.lcd_display_string(" Choose Station ",1)
      mylcd.lcd_display_string("[GO] < LiDStep >",2)

def choose5():
    time.sleep(0.5)
    while(1):
     if ( GPIO.input(PREV) == False):
      choose4()
     if ( GPIO.input(PLAY) == False):
      station5()
     if ( GPIO.input(NEXT) == False):
      choose6()
     else:
      mylcd.lcd_display_string(" Choose Station ",1)
      mylcd.lcd_display_string("[GO]  < Lounge >",2)

def choose6():
    time.sleep(0.5)
    while(1):
     if ( GPIO.input(PREV) == False):
      choose5()
     if ( GPIO.input(PLAY) == False):
      station6()
     if ( GPIO.input(NEXT) == False):
      choose7()
     else:
      mylcd.lcd_display_string(" Choose Station ",1)
      mylcd.lcd_display_string("[GO] < Ra NULA >",2)

def choose7():
    time.sleep(0.5)
    while(1):
     if ( GPIO.input(PREV) == False):
      choose6()
     if ( GPIO.input(PLAY) == False):
      station7()
     if ( GPIO.input(NEXT) == False):
      iradio_menu()
     else:
      mylcd.lcd_display_string(" Choose Station ",1)
      mylcd.lcd_display_string("[GO]  < Boogie >",2)

def station1():
  mylcd.lcd_display_string("    ChillHop    ",1)
  os.system("mpc clear")
  os.system("mpc add http://pub1.diforfree.org:8000/di_chillhop_hi")
  os.system("mpc repeat on")
  os.system("mpc play 1")
  time.sleep(0.5)
  while(1):
   my_title = str_pad + get_radio_title()
   for i in range (0, len(my_title)):
    lcd_text = my_title[i:(i+16)]
    mylcd.lcd_display_string(lcd_text,2)
    time.sleep(0.4)
    mylcd.lcd_display_string(str_pad,2)
    if ( GPIO.input(NEXT) == False):
     station2()
    if ( GPIO.input(PREV) == False):
     station7()
    if ( GPIO.input(PLAY) == False):
     os.system("mpc stop")
     main_menu()
    if ( GPIO.input(UP) == False):
     display_volume()
     os.system("mpc volume +10")
     display_volume()
     time.sleep(0.5)
     mylcd.lcd_display_string("    ChillHop    ",1)
    if ( GPIO.input(DOWN) == False):
     display_volume()
     os.system("mpc volume -10")
     display_volume()
     time.sleep(0.5)
     mylcd.lcd_display_string("    ChillHop    ",1)

def station2():
  mylcd.lcd_display_string("    ChillOut    ",1)
  os.system("mpc clear")
  os.system("mpc add http://pub1.diforfree.org:8000/di_chillout_hi")
  os.system("mpc repeat on")
  os.system("mpc play 1")
  time.sleep(0.5)
  while(1):
   my_title = str_pad + get_radio_title()
   for i in range (0, len(my_title)):
    lcd_text = my_title[i:(i+16)]
    mylcd.lcd_display_string(lcd_text,2)
    time.sleep(0.4)
    mylcd.lcd_display_string(str_pad,2)
    if ( GPIO.input(NEXT) == False):
     station3()
    if ( GPIO.input(PREV) == False):
     station1()
    if ( GPIO.input(PLAY) == False):
     os.system("mpc stop")
     main_menu()
    if ( GPIO.input(UP) == False):
     display_volume()
     os.system("mpc volume +10")
     display_volume()
     time.sleep(0.5)
     mylcd.lcd_display_string("    ChillOut    ",1)
    if ( GPIO.input(DOWN) == False):
     display_volume()
     os.system("mpc volume -10")
     display_volume()
     time.sleep(0.5)
     mylcd.lcd_display_string("    ChillOut    ",1)

def station3():
  mylcd.lcd_display_string("   LiquidDnB    ",1)
  os.system("mpc clear")
  os.system("mpc add http://pub1.diforfree.org:8000/di_liquiddnb_hi")
  os.system("mpc repeat on")
  os.system("mpc play 1")
  time.sleep(0.5)
  while(1):
    my_title = str_pad + get_radio_title()
    for i in range (0, len(my_title)):
     lcd_text = my_title[i:(i+16)]
     mylcd.lcd_display_string(lcd_text,2)
     time.sleep(0.4)
     mylcd.lcd_display_string(str_pad,2)
     if ( GPIO.input(NEXT) == False):
      station4()
     if ( GPIO.input(PREV) == False):
      station2()
     if ( GPIO.input(PLAY) == False):
      os.system("mpc stop")
      main_menu()
     if ( GPIO.input(UP) == False):
      display_volume()
      os.system("mpc volume +10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string("   LiquidDnB    ",1)
     if ( GPIO.input(DOWN) == False):
      display_volume()
      os.system("mpc volume -10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string("   LiquidDnB    ",1)

def station4():
  mylcd.lcd_display_string(" LiquidDubstep  ",1)
  os.system("mpc clear")
  os.system("mpc add http://pub1.diforfree.org:8000/di_liquiddubstep_hi")
  os.system("mpc repeat on")
  os.system("mpc play 1")
  time.sleep(0.5)
  while(1):
    my_title = str_pad + get_radio_title()
    for i in range (0, len(my_title)):
     lcd_text = my_title[i:(i+16)]
     mylcd.lcd_display_string(lcd_text,2)
     time.sleep(0.4)
     mylcd.lcd_display_string(str_pad,2)
     if ( GPIO.input(NEXT) == False):
      station5()
     if ( GPIO.input(PREV) == False):
      station3()
     if ( GPIO.input(PLAY) == False):
      os.system("mpc stop")
      main_menu()
     if ( GPIO.input(UP) == False):
      display_volume()
      os.system("mpc volume +10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string(" LiquidDubstep  ",1)
     if ( GPIO.input(DOWN) == False):
      display_volume()
      os.system("mpc volume -10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string(" LiquidDubstep  ",1)

def station5():
  mylcd.lcd_display_string("    DTLounge    ",1)
  os.system("mpc clear")
  os.system("mpc add http://pub1.diforfree.org:8000/di_downtempolounge_hi")
  os.system("mpc repeat on")
  os.system("mpc play 1")
  time.sleep(0.5)
  while(1):
    my_title = str_pad + get_radio_title()
    for i in range (0, len(my_title)):
     lcd_text = my_title[i:(i+16)]
     mylcd.lcd_display_string(lcd_text,2)
     time.sleep(0.4)
     mylcd.lcd_display_string(str_pad,2)
     if ( GPIO.input(NEXT) == False):
      station6()
     if ( GPIO.input(PREV) == False):
      station4()
     if ( GPIO.input(PLAY) == False):
      os.system("mpc stop")
      main_menu()
     if ( GPIO.input(UP) == False):
      display_volume()
      os.system("mpc volume +10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string("    DTLounge    ",1)
     if ( GPIO.input(DOWN) == False):
      display_volume()
      os.system("mpc volume -10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string("    DTLounge    ",1)

def station6():
  mylcd.lcd_display_string("   Radio Nula     ",1)
  os.system("mpc clear")
  os.system("mpc add http://streaming.radionula.com:8800/channel2")
  os.system("mpc repeat on")
  os.system("mpc play 1")
  time.sleep(0.5)
  while(1):
    my_title = str_pad + get_radio_title()
    for i in range (0, len(my_title)):
     lcd_text = my_title[i:(i+16)]
     mylcd.lcd_display_string(lcd_text,2)
     time.sleep(0.4)
     mylcd.lcd_display_string(str_pad,2)
     if ( GPIO.input(NEXT) == False):
      station7()
     if ( GPIO.input(PREV) == False):
      station5()
     if ( GPIO.input(PLAY) == False):
      os.system("mpc stop")
      main_menu()
     if ( GPIO.input(UP) == False):
      display_volume()
      os.system("mpc volume +10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string("   Radio Nula     ",1)
     if ( GPIO.input(DOWN) == False):
      display_volume()
      os.system("mpc volume -10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string("   Radio Nula     ",1)

def station7():
  mylcd.lcd_display_string("   Boogie.FM    ",1)
  os.system("mpc clear")
  os.system("mpc add http://78.90.63.199:9000/")
  os.system("mpc repeat on")
  os.system("mpc play 1")
  time.sleep(0.5)
  while(1):
    my_title = str_pad + get_radio_title()
    for i in range (0, len(my_title)):
     lcd_text = my_title[i:(i+16)]
     mylcd.lcd_display_string(lcd_text,2)
     time.sleep(0.4)
     mylcd.lcd_display_string(str_pad,2)
     if ( GPIO.input(NEXT) == False):
      station1()
     if ( GPIO.input(PREV) == False):
      station6()
     if ( GPIO.input(PLAY) == False):
      os.system("mpc stop")
      main_menu()
     if ( GPIO.input(UP) == False):
      display_volume()
      os.system("mpc volume +10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string("   Boogie.FM    ",1)
     if ( GPIO.input(DOWN) == False):
      display_volume()
      os.system("mpc volume -10")
      display_volume()
      time.sleep(0.5)
      mylcd.lcd_display_string("   Boogie.FM    ",1)

def ip():
  timelastchecked = 0
  time.sleep(0.5)
  while(1):
   if time.time() >= timelastchecked:
    timelastchecked = time.time()+3
    mytime = get_date()
    mytime = mytime[11:-14]
    mytemp = "{:.0f}".format(temperature)
    mywifi = get_wifi_signal()
    mystring = mytime + " " + chr(5) + ":" + mytemp + chr(223) + " " + chr(6) + ":" + mywifi
    mylcd.lcd_display_string(mystring,1)
    mylcd.lcd_display_string("               ",2)
    time.sleep(0.1)
    ipaddr = get_ip_address()
    mylcd.lcd_display_string(ipaddr,2)
    time.sleep(5)
    main_menu()

def get_date():
    d = subprocess.check_output("date", shell=True, stderr=subprocess.STDOUT)
    return d

def get_ip_address():
    p = Popen(ip_cmd, shell=True, stdout=PIPE)
    ipaddr = p.communicate()[0]
    return ipaddr

def get_video_title():
    p = Popen(video_cmd, shell=True, stdout=PIPE)
    video = p.communicate()[0]
    return video

def get_radio_title():
    p = Popen(radio_cmd, shell=True, stdout=PIPE)
    radio = p.communicate()[0]
    return radio

def get_wifi_signal():
    p = Popen(wifi_cmd, shell=True, stdout=PIPE)
    wifi = p.communicate()[0]
    return wifi

def get_volume():
    volume = subprocess.check_output("mpc status | grep volume", shell=True, stderr=subprocess.STDOUT)
    volume = volume[7:volume.find("%")+1]
    volume = volume.replace("%","")
    volume = volume.replace(" ","")
    return volume

def display_volume():
   Vol = get_volume()
   mylcd.lcd_clear() # clear screen
   block = chr(255) # block character on screen
   VolInt = int(Vol) # converted to integer

   if Vol == "100":
       Vol = ""
       sign = 'MAX'
   elif Vol == "0":
       Vol = ""
       sign = 'MUTED'
   else:
      sign = "%"

   numBars = int(round(VolInt/10))
   # now draw cust. chars
   mylcd.lcd_display_string(chr(0) + chr(1) + " Volume: " + Vol + sign, 1)
   mylcd.lcd_display_string(chr(2) + chr(3) + " " + (block * numBars), 2)

def reboot():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    menu_shutdown()
   if ( GPIO.input(NEXT) == False):
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("#                ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("##               ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("###              ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("####             ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("#####            ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("######           ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("#######          ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("########         ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("#########        ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("##########       ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("###########      ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("############     ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("#############    ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("##############   ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("###############  ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("################ ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("    Rebooting    ",1)
    mylcd.lcd_display_string("#################",2)
    time.sleep(0.1)
    mylcd.lcd_clear()
    os.system("sudo reboot")
    time.sleep(1)
   else:
    mylcd.lcd_display_string("     Reboot?    ",1)
    mylcd.lcd_display_string("< No       Yes >",2)

def shutdown():
  time.sleep(0.5)
  while(1):
   if ( GPIO.input(PREV) == False):
    menu()
   if ( GPIO.input(NEXT) == False):
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("#                ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("##               ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("###              ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("####             ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("#####            ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("######           ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("#######          ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("########         ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("#########        ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("##########       ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("###########      ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("############     ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("#############    ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("##############   ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("###############  ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("################ ",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("  Shutting Down  ",1)
    mylcd.lcd_display_string("#################",2)
    time.sleep(0.1)
    mylcd.lcd_display_string("      Adeus!     ",1)
    mylcd.lcd_display_string("",2)
    time.sleep(2)
    mylcd.lcd_clear()
    os.system("sudo shutdown -h now")
    time.sleep(3)
   else:
    mylcd.lcd_display_string("   Shut down?   ",1)
    mylcd.lcd_display_string("< No       Yes >",2)

if __name__ == '__main__':
  try:
      main()

  except KeyboardInterrupt:
      os.system("mpc stop")
      os.system("echo 0 > /tmp/status")
      os.system("echo -n 'q' > /tmp/omfifo")
      print "Adeus!"
      sys.exit()

  finally:
      GPIO.cleanup()
      mylcd.lcd_clear()
