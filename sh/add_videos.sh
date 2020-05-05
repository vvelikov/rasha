#!/bin/bash

# playlist location Masha
LIST1="/home/pi/scripts/pl/masha.m3u"
# playlist location Barba
LIST2="/home/pi/scripts/pl/barba.m3u"
# playlist location Peppa
LIST3="/home/pi/scripts/pl/peppa.m3u"
# playlist location Conni
LIST4="/home/pi/scripts/pl/conni.m3u"
# playlist location Caillou
LIST5="/home/pi/scripts/pl/caillou.m3u"
# playlist location Tom & Jerry
LIST6="/home/pi/scripts/pl/tom.m3u"

if ! [ -f $LIST1 ]; then
	touch $LIST1
fi

if ! [ -f $LIST2 ]; then
	touch $LIST2
fi

if ! [ -f $LIST3 ]; then
	touch $LIST3
fi

if ! [ -f $LIST4 ]; then
	touch $LIST4
fi

if ! [ -f $LIST5 ]; then
	touch $LIST5
fi

if ! [ -f $LIST6 ]; then
	touch $LIST6
fi


if ! [ `cat $LIST1| wc -l` -gt 5 ] ; then 
	rm $LIST1
	find /mnt/Masha -name '*.mp4' > /home/pi/scripts/pl/masha.m3u
fi

if ! [ `cat $LIST2| wc -l` -gt 5 ] ; then
	rm $LIST2
	find /mnt/Barba -name '*.mp4' -o -name '*.mkv' > /home/pi/scripts/pl/barba.m3u
fi

if ! [ `cat $LIST3| wc -l` -gt 5 ] ; then 
	rm $LIST3
	find /mnt/Peppa -name '*.mp4' -o -name '*.avi' > /home/pi/scripts/pl/peppa.m3u
fi

if ! [ `cat $LIST4| wc -l` -gt 5 ] ; then
	rm $LIST4
	find /mnt/Conni -name '*.mp4'  > /home/pi/scripts/pl/conni.m3u
fi

if ! [ `cat $LIST5| wc -l` -gt 5 ] ; then
	rm $LIST5
	find /mnt1/Caillou -name '*.mp4'  > /home/pi/scripts/pl/caillou.m3u
fi

if ! [ `cat $LIST6| wc -l` -gt 5 ] ; then
	rm $LIST6
	find /mnt1/Tom -name '*.mp4'  > /home/pi/scripts/pl/tom.m3u
fi
