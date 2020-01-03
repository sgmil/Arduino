#!/bin/bash
directory=$1
file=$2
#board=$(sed -n '2p' < "$file" | cut -d' ' -f 2)
board=$(sed -n '2p' < "$file" | sed 's/#define board //g')
echo "$board"
#IP=$(sed -n '3p' < "$file" | cut -d' ' -f 2)
IP=$(sed -n '3p' < "$file" | sed 's/#define IP//g')
echo "$IP"

~/bin/arduino-cli compile --fqbn "$board" "$directory"/"$file"
