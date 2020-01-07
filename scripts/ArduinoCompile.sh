#!/bin/bash
# pass directory path and filename as arguments when invoking bash script 
directory=$1
file=$2
# extract board fqbn from file line 2 and strip out extras: 
board=$(sed -n '2p' < "$file" | sed 's/#define BOARD //g' | sed 's/\"//g')
echo "$board"
# compile command:
~/bin/arduino-cli compile -v --fqbn "$board" "$directory"
