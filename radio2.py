#!/usr/bin/env python3
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

# Define GPIO for button control
UP = 23
PREV = 17
PLAY = 27
NEXT = 24
DOWN = 18

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
# Define some device constants
mylcd = I2C_LCD_driver.lcd()
str_pad = " " * 16
# degree symbol
degree = chr(223)                       

# load custom icons
mylcd.lcd_load_custom_chars(speaker_icon)

# some command definitions
title_cmd = "dbuscontrol.sh getsource | awk -F '/' '{print $4}' | cut -d '.' -f1 | tr -d '\n'"
date_cmd = "date +%R | tr -d '\n'"
date_now_cmd = "date +%Y%m%d | tr -d '\n'"
time_cmd = "date '+%F [%H:%M]' | tr -d '\n'"
wifi_cmd = "iwconfig wlan0| grep Signal | awk '{print $4}' | cut -d '-' -f2 | tr -d '\n'"
temp_cmd = "cat /var/log/rasha/tempIN"
temp_out_cmd = "cat /var/log/rasha/tempOUT"
hum_cmd = "cat /var/log/rasha/humidity"
weather_cmd = "cat /var/log/rasha/weather | tr -d '\n'"
radio_cmd = "mpc current -f [%title%] | tr -d '\n'"

# playlists
masha_cmd = "cat /home/pi/scripts/pl/masha.m3u | wc -l | xargs | tr -d '\n'"
barba_cmd = "cat /home/pi/scripts/pl/barba.m3u | wc -l | xargs | tr -d '\n'"
peppa_cmd = "cat /home/pi/scripts/pl/peppa.m3u | wc -l | xargs | tr -d '\n'"
conni_cmd = "cat /home/pi/scripts/pl/conni.m3u | wc -l | xargs | tr -d '\n'"

# other variables
limit = 7                   # only 7 videos are allowed per day Barba = 0.8 Peppa = 1 Masha = 1.2 Conni = 2
counter = 0                 # counter starts at 0
time_diff = 30              # buffer before counting video

def main():
    mylcd.lcd_clear() # clear LCD screen
    mylcd.lcd_display_string(" >>> RASHA <<<  ",1)
    mylcd.lcd_display_string(" Music/Video PL ",2)
    time.sleep(1)
    mylcd.lcd_display_string("                ",1)
    mylcd.lcd_display_string("                ",2)
    # make sure videos & music are available
    check_counter()
    check_playlist()
    check_music()
    write_msg()
    mylcd.lcd_display_string("    LOADING     ",1)
    mylcd.lcd_display_string("       #        ",2)
    time.sleep(0.5)
    mylcd.lcd_display_string("    LOADING     ",1)
    mylcd.lcd_display_string("      ###       ",2)
    time.sleep(0.5)
    mylcd.lcd_display_string("    LOADING     ",1)
    mylcd.lcd_display_string("    #######     ",2)
    time.sleep(0.5)
    mylcd.lcd_display_string("    LOADING     ",1)
    mylcd.lcd_display_string("   #########    ",2)
    time.sleep(0.5)
    mylcd.lcd_display_string("    LOADING     ",1)
    mylcd.lcd_display_string("################",2)
    time.sleep(0.5)
    c = run_cmd(conni_cmd)
    mylcd.lcd_display_string("Conni" + " " + str(c) + " " + "Videos",1)
    time.sleep(2)
    m = run_cmd(masha_cmd)
    mylcd.lcd_display_string("Masha" + " " + str(m) + " " + "Videos",1)
    time.sleep(2)
    b = run_cmd(barba_cmd)
    mylcd.lcd_display_string("Barba" + " " + str(b) + " " + "Videos",1)
    time.sleep(2)
    p = run_cmd(peppa_cmd)
    mylcd.lcd_display_string("Peppa" + " " + str(p) + " " + "Videos",1)
    time.sleep(2)
    mylcd.lcd_display_string("      DONE      ",1)
    # load thd script fix
    os.system("/home/pi/scripts/thd.sh &")
    os.system("sudo /usr/local/bin/asciiquarium > /dev/tty1  &")
    time.sleep(0.5)
    main_menu()

def show_status():
    time = run_cmd(date_cmd)
    temp = run_cmd(temp_cmd)
    wifi = run_cmd(wifi_cmd)
    mystring = time + " " + chr(5) + ":" + temp + degree + " " + chr(6) + ":" + wifi
    mylcd.lcd_display_string(mystring,1)

def main_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
      if time.time() >= timelastchecked:
       timelastchecked = time.time()+3
       show_status()
       reset_counter()
       mylcd.lcd_display_string("< Off     Menu >",2)
      else:
       if ( GPIO.input(NEXT) == False):
        conni_menu()
       if (GPIO.input(PREV) == False):
        off_menu()

def off_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]     < IP > ",2)
     else:
      if ( GPIO.input(PLAY) == False):
       ip_menu()
      if ( GPIO.input(PREV) == False):
       main_menu()
      if ( GPIO.input(NEXT) == False):
       weather_menu()

def ip_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      time.sleep(0.1)
      mystring = "                   "
      mylcd.lcd_display_string(mystring,1)
      mylcd.lcd_display_string(mystring,2)
      mylcd.lcd_display_string("   IPv4 Addr:  ",1)
      ipaddr = get_ip_address()
      mylcd.lcd_display_string(" " + " " + ipaddr,2)
      time.sleep(5)
      main_menu()

def weather_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO] < Weather >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       show_weather()
       time.sleep(0.2)
       mystring = "                   "
       mylcd.lcd_display_string(mystring,1)
       mylcd.lcd_display_string(mystring,2)
      if ( GPIO.input(NEXT) == False):
       show_counter_menu()
      if ( GPIO.input(PREV) == False):
       off_menu()

def show_weather():
    mylcd.lcd_display_string("                ",2)
    mylcd.lcd_display_string("                ",1)
    time.sleep(0.2)
    lcd_status = "Munich, Germany "
    mylcd.lcd_display_string(lcd_status,1)
    temp = run_cmd(temp_cmd)
    hum = run_cmd(hum_cmd)
    tempout = run_cmd(temp_out_cmd)
    weather = run_cmd(weather_cmd)
    mystring = chr(5) + ":" + temp + degree + "|" + tempout + degree + " " + "H:" + hum + "%"
    time.sleep(0.2)
    while(1):
     mylcd.lcd_display_string(mystring,2)
     time.sleep(5)
     mylcd.lcd_display_string("                ",2)
     time.sleep(0.1)
     if len(weather) == 5:
      mylcd.lcd_display_string("     " + weather,2)
      time.sleep(5)
     elif len(weather) == 6:
      mylcd.lcd_display_string("    " + weather,2)
      time.sleep(5)
     elif len(weather) == 8:
      mylcd.lcd_display_string("    " + weather,2)
      time.sleep(5)
     elif len(weather) >= 13:
      mylcd.lcd_display_string(" " + weather,2)
      time.sleep(5)
     else:
      mylcd.lcd_display_string(" " + weather,2)
      time.sleep(5)
     main_menu()

def show_counter_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]  < Show # >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       show_counter()
      if ( GPIO.input(NEXT) == False):
       reset_counter_menu()
      if ( GPIO.input(PREV) == False):
       off_menu()

def show_counter():
    global counter
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      time.sleep(0.1)
      mystring = "                "
      mylcd.lcd_display_string(mystring,1)
      mylcd.lcd_display_string(mystring,2)
      time.sleep(0.01)
      x = round(counter,1)
      mylcd.lcd_display_string(" Counter:      ",1)
      mylcd.lcd_display_string("   #:" + str(x),2)
      time.sleep(3)
      main_menu()

def reset_counter_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO] < Reset # >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       counter_menu()
      if ( GPIO.input(PREV) == False):
       show_counter_menu()
      if ( GPIO.input(NEXT) == False):
       reboot_menu()

def reboot_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]  < Reboot >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       reboot()
      if ( GPIO.input(PREV) == False):
       reset_counter_menu()
      if ( GPIO.input(NEXT) == False):
       shutdown_menu()

def shutdown_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]    < Halt >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       shutdown()
      if ( GPIO.input(PREV) == False):
       reboot_menu()
      if ( GPIO.input(NEXT) == False):
       off_menu()

def iradio_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]  < iRadio >",2)
      os.system("/home/pi/scripts/add_stations.sh")
      time.sleep(0.2)
     else:
      if ( GPIO.input(PLAY) == False):
       choose1()
      if ( GPIO.input(PREV) == False):
       peppa_menu()
      if ( GPIO.input(NEXT) == False):
       music_menu()

def conni_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]   < Conni >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       if check_limit(counter):
        play_video("/mnt/Conni/")
        time.sleep(1)
        main_menu()
       else:
        display_error()
      if ( GPIO.input(NEXT) == False):
       masha_menu()
      if ( GPIO.input(PREV) == False):
       main_menu()

def masha_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]   < Masha >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       if check_limit(counter):
        play_video("/mnt/Masha/")
        time.sleep(1)
        main_menu()
       else:
        display_error()
      if ( GPIO.input(NEXT) == False):
       barba_menu()
      if ( GPIO.input(PREV) == False):
       conni_menu()

def barba_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]   < Barba >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       if check_limit(counter):
        play_video("/mnt/Barba/")
        time.sleep(1)
        main_menu()
       else:
        display_error()
      if ( GPIO.input(NEXT) == False):
       peppa_menu()
      if ( GPIO.input(PREV) == False):
       masha_menu()

def peppa_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]   < Peppa >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       if check_limit(counter):
        play_video("/mnt/Peppa/")
        time.sleep(1)
        main_menu()
       else:
        display_error()
      if ( GPIO.input(NEXT) == False):
       iradio_menu()
      if ( GPIO.input(PREV) == False):
       barba_menu()

def music_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]   < Music >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       play_music()
      if ( GPIO.input(NEXT) == False):
       slideshow_menu()
      if ( GPIO.input(PREV) == False):
       iradio_menu()

def slideshow_menu():
    timelastchecked = 0
    time.sleep(0.2)
    while(1):
     if time.time() >= timelastchecked:
      timelastchecked = time.time()+3
      show_status()
      mylcd.lcd_display_string("[GO]  < SlShow >",2)
     else:
      if ( GPIO.input(PLAY) == False):
       play_slideshow()
      if ( GPIO.input(NEXT) == False):
       main_menu()
      if ( GPIO.input(PREV) == False):
       music_menu()

def play_slideshow():
    lcd_status = "SLIDESHOW"
    time.sleep(0.2)
    mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
    os.system("/home/pi/scripts/sson.sh")
    while(1):
      mylcd.lcd_display_string("                ",2)
      mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
      time.sleep(0.1)
      mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
      if ( GPIO.input(PLAY) == False):
       os.system("/home/pi/scripts/ssoff.sh")
       time.sleep(0.2)
       main_menu()
      if ( GPIO.input(NEXT) == False):
       os.system("/home/pi/scripts/ssoff.sh")
       time.sleep(0.2)
       main_menu()
      if ( GPIO.input(PREV) == False):
       os.system("/home/pi/scripts/ssoff.sh")
       time.sleep(0.2)
       main_menu()

def play_music():
    lcd_status = "PLAYING"
    mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
    os.system("mpc clear -q")
    os.system("mpc load all")
    os.system("mpc random on")
    os.system("mpc repeat off")
    os.system("mpc play")
    time.sleep(0.2)
    while(1):
     title = get_radio_title().decode()
     my_title = str_pad + title
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

def play_video(str):
    global counter
    time_play = time.time()
    check_playlist()
    if check_limit(counter):
     do_limit(str)
     file = randomplay(str)
     write_log(file)
     omxproc = Popen(['omxplayer', file, '-b', '-r', '-o', 'alsa:hw:1' ], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
     lcd_status = "PLAYING"
     while omxproc.poll() is None:
      title = run_cmd(title_cmd)
      my_title = str_pad + title
      for i in range (0, len(my_title)):
       lcd_text = my_title[i:(i+16)]
       mylcd.lcd_display_string(lcd_text,2)
       time.sleep(0.3)
       mylcd.lcd_display_string(str_pad,2)
       mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
       time.sleep(0.3)
       mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
       if ( GPIO.input(UP) == False):
        os.system("dbuscontrol.sh volumeup +10")
       if ( GPIO.input(DOWN) == False):
        os.system("dbuscontrol.sh volumedown -10")
       if ( GPIO.input(PLAY) == False):
        if lcd_status == "PLAYING":
         lcd_status = "PAUSED"
         os.system("dbuscontrol.sh pause")
         mylcd.lcd_display_string("                  ",1)
         mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
         time.sleep(0.3)
         mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
        else:
         lcd_status = "PLAYING"
         os.system("dbuscontrol.sh pause")
         mylcd.lcd_display_string("                  ",1)
         mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
         time.sleep(0.3)
         mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
       if ( GPIO.input(NEXT) == False):
        if check_limit(counter):
         os.system("dbuscontrol.sh stop")
         file = randomplay(str)
         diff = time.time() - time_play
         if diff < time_diff:
          time_play = time.time()
          file = randomplay(str)
          write_log(file)
          omxproc = Popen(['omxplayer', file, '-b', '-r', '-o', 'alsa:hw:1' ], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
          lcd_status = "PLAYING"
          mylcd.lcd_display_string("                  ",1)
          mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
          time.sleep(0.3)
          mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
          title = run_cmd(title_cmd)
          my_title = str_pad + title
          time.sleep(0.3)
         else:
          do_limit(str)
          file = randomplay(str)
          write_log(file)
          time_play = time.time()
          omxproc = Popen(['omxplayer', file, '-b', '-r', '-o', 'alsa:hw:1'], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
          lcd_status = "PLAYING"
          mylcd.lcd_display_string("                  ",1)
          mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
          time.sleep(0.3)
          mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
          title = run_cmd(title_cmd)
          my_title = str_pad + title
          time.sleep(0.3)
        else:
         display_error()
       if ( GPIO.input(PREV) == False):
        os.system("dbuscontrol.sh stop")
        time.sleep(0.3)
        main_menu()
    else:
     display_error()

def choose1():
    time.sleep(0.2)
    while(1):
     if ( GPIO.input(PREV) == False):
      choose2()
     if ( GPIO.input(PLAY) == False):
      station1()
     if ( GPIO.input(NEXT) == False):
      choose2()
     else:
      mylcd.lcd_display_string(" Choose Station ",1)
      mylcd.lcd_display_string("[GO] < Ra NULA >",2)

def choose2():
    time.sleep(0.2)
    while(1):
     if ( GPIO.input(PREV) == False):
      choose1()
     if ( GPIO.input(PLAY) == False):
      station2()
     if ( GPIO.input(NEXT) == False):
      choose1()
     else:
      mylcd.lcd_display_string(" Choose Station ",1)
      mylcd.lcd_display_string("[GO] < ChilOut >",2)

def station1():
    mylcd.lcd_display_string("   Radio Nula     ",1)
    os.system("mpc play 1")
    while(1):
     title = run_cmd(radio_cmd)
     my_title = str_pad + title
     for i in range (0, len(my_title)):
      lcd_text = my_title[i:(i+16)]
      mylcd.lcd_display_string(lcd_text,2)
      time.sleep(0.4)
      mylcd.lcd_display_string(str_pad,2)
      if ( GPIO.input(NEXT) == False):
       station2()
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
       mylcd.lcd_display_string("   Radio Nula     ",1)
      if ( GPIO.input(DOWN) == False):
       display_volume()
       os.system("mpc volume -10")
       display_volume()
       time.sleep(0.5)
       mylcd.lcd_display_string("   Radio Nula     ",1)

def station2():
    mylcd.lcd_display_string("  RaggaKings   ",1)
    os.system("mpc play 2")
    while(1):
     title = run_cmd(radio_cmd)
     my_title = str_pad + title
     for i in range (0, len(my_title)):
      lcd_text = my_title[i:(i+16)]
      mylcd.lcd_display_string(lcd_text,2)
      time.sleep(0.4)
      mylcd.lcd_display_string(str_pad,2)
      if ( GPIO.input(NEXT) == False):
       station1()
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
       mylcd.lcd_display_string("  RaggaKings   ",1)
      if ( GPIO.input(DOWN) == False):
       display_volume()
       os.system("mpc volume -10")
       display_volume()
       time.sleep(0.5)
       mylcd.lcd_display_string("  RaggaKings   ",1)

def counter_menu():
    time.sleep(0.2)
    while(1):
     if ( GPIO.input(PREV) == False):
      main_menu()
     if ( GPIO.input(NEXT) == False):
      mylcd.lcd_display_string(" Resetting       ",1)
      mylcd.lcd_display_string("#                ",2)
      time.sleep(0.01)
      mylcd.lcd_display_string(" Resetting       ",1)
      mylcd.lcd_display_string("###              ",2)
      time.sleep(0.01)
      mylcd.lcd_display_string(" Resetting       ",1)
      mylcd.lcd_display_string("#####           ",2)
      time.sleep(0.01)
      mylcd.lcd_display_string(" Resetting       ",1)
      mylcd.lcd_display_string("#############    ",2)
      time.sleep(0.01)
      mylcd.lcd_display_string(" Resetting       ",1)
      mylcd.lcd_display_string("################ ",2)
      time.sleep(0.01)
      reset_counter_now()
      mylcd.lcd_display_string("      Done       ",1)
      mylcd.lcd_display_string("                 ",2)
      main_menu()
     else:
      mylcd.lcd_display_string("     RESET?      ",1)
      mylcd.lcd_display_string("< No        Yes >",2)

def reboot():
    time.sleep(0.2)
    while(1):
     if ( GPIO.input(PREV) == False):
      main_menu()
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
      mylcd.lcd_display_string("     REBOOT?    ",1)
      mylcd.lcd_display_string("< No       Yes >",2)

def shutdown():
    time.sleep(0.2)
    while(1):
     if ( GPIO.input(PREV) == False):
      main_menu()
     if ( GPIO.input(NEXT) == False):
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("#                ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("##               ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("###              ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("####             ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("#####            ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("######           ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("#######          ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("########         ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("#########        ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("##########       ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("###########      ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("############     ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("#############    ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("##############   ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("###############  ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("################ ",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("  Shutting Down  ",1)
      mylcd.lcd_display_string("#################",2)
      time.sleep(0.05)
      mylcd.lcd_display_string("   POWER OFF     ",1)
      mylcd.lcd_display_string("@@@@@@@@@@@@@@@@@",2)
      time.sleep(2)
      mylcd.lcd_clear()
      os.system("sudo shutdown -h now")
      sys.exit()
     else:
      mylcd.lcd_display_string("   SHUT DOWN?   ",1)
      mylcd.lcd_display_string("< No       Yes >",2)

def reset_counter():
    global counter
    dateStr = datetime.datetime.now().strftime("%H:%M")
    now = run_cmd(time_cmd)
    if (dateStr == '00:00' and counter != 0 ):
     counter = 0
     f = open( '/var/log/rasha/radio.log', 'a' )
     f.write( "+++++++++++++++++++++++++++++++++++++++++++++++++++++" + '\n' )
     f.write( "%s" % now + ' ' + "DAILY RESET" + '\n' )
     f.write( "+++++++++++++++++++++++++++++++++++++++++++++++++++++" + '\n' )
     f.close()
     time.sleep(3)

def reset_counter_now():
    global counter
    counter = 0
    now = run_cmd(time_cmd)
    f = open( '/var/log/rasha/radio.log', 'a' )
    f.write( "+++++++++++++++++++++++++++++++++++++++++++++++++++++" + '\n' )
    f.write( "%s" % now + ' ' + "MANUAL RESET" + '\n' )
    f.write( "+++++++++++++++++++++++++++++++++++++++++++++++++++++" + '\n' )
    f.close()

def write_msg():
    f = open( '/var/log/rasha/radio.log', 'a')
    now = run_cmd(time_cmd)
    f.write( "+++++++++++++++++++++++++++++++++++++++++++++++++++++" + '\n' )
    f.write( "%s" % now + ' ' + 'Rasha ready!' + '\n' )
    f.write( "+++++++++++++++++++++++++++++++++++++++++++++++++++++" + '\n' )
    f.close

def randomplay(str):
    global item
    if ( str == "/mnt/Masha/"):
     lines = run_cmd(masha_cmd)
     index = random.randrange(0, int(lines))
     with open("/home/pi/scripts/pl/masha.m3u", "r+") as f:
       new_f = f.readlines()
       f.seek(0)
       item = new_f[index]
       for line in new_f:
           if item not in line:
              f.write(line)
       f.truncate()
    elif ( str == "/mnt/Barba/"):
      lines = run_cmd(barba_cmd)
      index = random.randrange(0, int(lines))
      with open("/home/pi/scripts/pl/barba.m3u", "r+") as b:
        new_b = b.readlines()
        b.seek(0)
        item = new_b[index]
        for line in new_b:
            if item not in line:
               b.write(line)
        b.truncate()
    elif ( str == "/mnt/Peppa/"):
      lines = run_cmd(peppa_cmd)
      index = random.randrange(0, int(lines))
      with open("/home/pi/scripts/pl/peppa.m3u", "r+") as p:
        new_p = p.readlines()
        p.seek(0)
        item = new_p[index]
        for line in new_p:
            if item not in line:
               p.write(line)
        p.truncate()
    else:
      lines = run_cmd(conni_cmd)
      index = random.randrange(0, int(lines))
      with open("/home/pi/scripts/pl/conni.m3u", "r+") as c:
        new_c = c.readlines()
        c.seek(0)
        item = new_c[index]
        for line in new_c:
            if item not in line:
               c.write(line)
        c.truncate()
    item = item.strip()
    return item

def write_log(file):
    global counter
    f = open( '/var/log/rasha/radio.log', 'a' )
    now = run_cmd(date_cmd)
    x = file[5:]
    y = x[:-4]
    y = y.replace('/',' - ')
    if y.startswith('Conni'):
        y = y[8:]
    f.write( "%s" % now + ' ' + "# %s" % round(counter,1) + ' ' + y + '\n' )
    f.close()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_volume():
    volume = subprocess.check_output("mpc status | grep volume", shell=True, stderr=subprocess.STDOUT)
    volume = volume[7:volume.find("%")+1]
    volume = volume.replace("%","")
    volume = volume.replace(" ","")
    return volume

def display_volume():
    Vol = get_volume()
    mylcd.lcd_clear() # clear screen
    block = chr(255)  # block character on screen
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
    mylcd.lcd_display_string(chr(0) + chr(1) + " Volume: " + Vol + sign, 1)
    mylcd.lcd_display_string(chr(2) + chr(3) + " " + (block * numBars), 2)

def display_error():
    os.system("dbuscontrol.sh stop")
    mylcd.lcd_display_string("                ", 1)
    mylcd.lcd_display_string("                ", 2)
    mylcd.lcd_display_string(" LIMIT %s" % (round(counter,1)),1)
    mylcd.lcd_display_string(" REACHED!    ",2)
    time.sleep(2)
    main_menu()

def do_limit(str):
    global counter
    if ( str == "/mnt/Peppa/"):
        counter+=1
    elif ( str == "/mnt/Barba/"):
        counter+=0.8
    elif ( str == "/mnt/Masha/"):
        counter+=1.2
    else:
        counter+=2

def check_limit(counter):
    if counter < limit:
        return True
    else:
        return False

# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

# rewrite in python
def check_playlist():
    os.system("/home/pi/scripts/add_videos.sh")

def check_music():
    os.system("/home/pi/scripts/add_music.sh")

# Main
if __name__ == '__main__':
  try:
      main()

  except KeyboardInterrupt:
      mylcd.lcd_clear()
      sys.exit()

  finally:
      GPIO.cleanup()
      mylcd.lcd_clear()
      print ("Adeus!")

