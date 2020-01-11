#!/bin/bash
# pass directory path and filename as arguments when invoking bash script 
directory=$1
file=$2
# extract board fqbn from file line 2 and strip out extras: 
board=$(grep -i "#define BOARD" "$file" | sed 's/#define BOARD //g' | sed 's/\"//g')
echo "$board"
# compile command:
IP=$(grep -i "#define IP_ADDRESS" "$file" | sed 's/#define IP_ADDRESS //g' | sed 's/\"//g')
echo "$IP"

~/bin/arduino-cli compile -v --fqbn "$board" "$directory"
