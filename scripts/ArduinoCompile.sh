#!/bin/bash
directory=$1
file=$2

board=$(grep -i "#define BOARD" "$file" | sed 's/#define BOARD //g' | sed 's/\"//g')
echo "$board"
IP=$(grep -i "#define IP_ADDRESS" "$file" | sed 's/#define IP_ADDRESS //g' | sed 's/\"//g')
echo "$IP"

~/bin/arduino-cli compile -v --fqbn "$board" "$directory"
