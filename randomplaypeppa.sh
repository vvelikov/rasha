#!/bin/bash

# files to play
files=($2/*)
limit=${#files[@]}
#limit=3
counter=0
fifo=/tmp/omfifop
now=$(date +"%D %H:%M")

# make fifo for controlling omxplayer
if [ -e $fifo ]; then
	rm $fifo
	mkfifo $fifo
        chmod a+w $fifo
else
    mkfifo $fifo
    chmod a+w $fifo
fi

	echo "Playing $limit files..."
	file_played[1]=""

	while [ "$counter" -le "$limit" ]
	do
	  file_ran="${files[RANDOM % ${#files[@]}]}"
	  #skip the played file
	  for filex in "${file_played[@]}"
	  do
	    play="TRUE"
	    if [ "$file_ran" == "$filex" ]; then
	      play="FALSE"
	      break
	    fi
  	done

	if [ "$play" == "TRUE" ]; then
	    echo "$now #$counter: $file_ran"
	    #echo "Playing file #$counter: $file_ran"
	    omxplayer --vol +500 -b -r -o $1 "$file_ran" < $fifo > /dev/null 2>&1
	    # set status to stop
            echo 0 > /tmp/statusp
    	    file_played[$counter]="$file_ran"
    	    let counter=$counter+1
  	fi
done
