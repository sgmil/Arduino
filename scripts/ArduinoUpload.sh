#!/bin/bash
directory=$1
file=$2

board=$(sed -n '2p' < "$file" | sed 's/#define BOARD //g')
echo "$board"
IP_3=$(sed -n '3p' < "$file" | sed 's/#define IP_LAST_THREE //g')
echo "$IP_3"

port=$(sed -n '4p' < "$file" | sed 's/#define PORT //g')
echo "$port"

~/bin/arduino-cli upload --port "$port" --fqbn "$board" "$directory"
