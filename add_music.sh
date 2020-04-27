#!/bin/bash

# playlist location
LIST="/var/lib/mpd/playlists/all.m3u"
# plist items count
plist=$(cat /var/lib/mpd/playlists/all.m3u | wc -l)
# count mp3z 
muz=$(find /mnt/music -name '*.mp3' | wc -l)

if [ "$plist" -eq "$muz" ]; then
	exit 1
else
	rm /var/lib/mpd/playlists/all.m3u
	find /mnt/music -name '*.mp3' > /var/lib/mpd/playlists/all.m3u
fi
exit 1
