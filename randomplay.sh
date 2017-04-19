#!/bin/bash

# files to play
files=($2/*)
limit=${#files[@]}
#limit=3
counter=0
fifo=/tmp/omfifo

# make fifo for controlling omxplayer
if [ -e $fifo ]; then
	rm $fifo
	mkfifo $fifo
        chmod a+w $fifo
else
    mkfifo $fifo
    chmod a+w $fifo
fi

	echo "PLAYING $limit FILES..."
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
	    echo "$file_ran"
	    #echo "Playing file #$counter: $file_ran"
	    omxplayer --vol +500 -b -r -o $1 "$file_ran" < $fifo
	    # set status to stop
	        echo 0 > /tmp/status
    	    file_played[$counter]="$file_ran"
    	    let counter=$counter+1
  	fi
done
