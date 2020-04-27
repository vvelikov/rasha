#!/usr/bin/env python3
import sys
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

title_cmd = "dbuscontrol.sh getsource | awk -F '/' '{print $4}' | cut -d '.' -f1 | tr -d '\n'"

VIDEO_PATH = Path("/mnt/Barba/Japan.mp4")
player = OMXPlayer(VIDEO_PATH)
player.pause()
sleep(1)
player.play()
player.set_aspect_mode('fill')

sleep(5)
player.quit()
