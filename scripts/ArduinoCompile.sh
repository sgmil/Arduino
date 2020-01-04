#!/bin/bash
directory=$1
file=$2

board=$(sed -n '2p' < "$file" | sed 's/#define BOARD //g')
#echo "$board"
IP=$(sed -n '3p' < "$file" | sed 's/#define IP_LAST_THREE //g')
#echo "$IP"

~/bin/arduino-cli compile --fqbn "$board" "$directory"
