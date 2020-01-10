#!/bin/bash
directory=$1
file=$2

board=$(grep -i "#define BOARD" "$file"| sed 's/#define BOARD //g' | sed 's/\"//g')
echo "$board"
IP=$(grep -i "#define IP_ADDRESS" "$file" | sed 's/#define IP_ADDRESS //g' | sed 's/\"//g')
echo "$IP"
port=$(grep -i "#define PORT" "$file" | sed 's/#define PORT //g' | sed 's/\"//g')
echo "$port"

~/bin/arduino-cli upload --port "$port" --fqbn "$board" "$directory"
