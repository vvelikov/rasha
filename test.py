#!/usr/bin/env python3
import sys
import time
import I2C_LCD_driver
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging
logging.basicConfig(filename='tmp.log', level=logging.INFO)

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


def main():
   VD="/mnt/Barba/Japan.mp4"
   player_log = logging.getLogger("Rasha_PL:1")
   player = OMXPlayer(VD, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args='-b -r -o alsa:hw:0')
   player.playEvent += lambda _: player_log.info("Play")
   player.pauseEvent += lambda _: player_log.info("Pause")
   player.stopEvent += lambda _: player_log.info("Stop")
   lcd_status = "Playing"
   player.pause()
   player.play()
   title = player.get_source()
   player.set_aspect_mode('fill')
   while player.is_playing():
    display_status_scrolling(lcd_status, title)
   print("Done")
   player.quit()

def display_status_scrolling(lcd_status, title):
    my_title = str_pad + title
    for i in range (0, len(my_title)):
     lcd_text = my_title[i:(i+16)]
     mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
     mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
     mylcd.lcd_display_string(lcd_text,2)
     time.sleep(0.3)
     mylcd.lcd_display_string(str_pad,2)
     time.sleep(0.3)
     mylcd.lcd_display_string(" " + chr(4) + " " + " " + lcd_status + " " + " " + chr(4) + " " + " ",1)
     time.sleep(0.3)
     mylcd.lcd_display_string(chr(4) + " " + chr(4) + " " + lcd_status + " " + chr(4) + " " + chr(4) + " ",1)
     time.sleep(0.3)

# Main
if __name__ == '__main__':
  try:
      main()

  except KeyboardInterrupt:
      mylcd.lcd_clear()
      sys.exit()

  finally:
      mylcd.lcd_clear()
      print ("Adeus!")
