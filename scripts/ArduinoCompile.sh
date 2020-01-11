#!/bin/bash
## Arduinocompile.sh arg1 arg2 ##
	# pass directory path and filename as arguments when invoking bash script
directory=$1
file=$2
	# extract board and IP fqbn from file and strip out extras:
board=$(grep -i "#define BOARD" "$file" | sed 's/#define BOARD //g' | sed 's/\"//g')
echo "$board"
IP=$(grep -i "#define IP_ADDRESS" "$file" | sed 's/#define IP_ADDRESS //g' | sed 's/\"//g')
echo "$IP"
	# compile command:
~/bin/arduino-cli compile -v --fqbn "$board" "$directory"
