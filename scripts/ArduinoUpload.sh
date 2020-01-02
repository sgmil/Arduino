#!/bin/bash
directory=$1
file=$2
board=$(sed -n '1p' < "$file" | cut -d' ' -f 2)
echo "$board"
IP=$(sed -n '2p' < "$file" | cut -d' ' -f 2)
echo "$IP"
port=$(sed -n '3p' < "$file" | cut -d' ' -f 2)
echo "$port"
~/bin/arduino-cli upload --port "$port" --fqbn "$board" "$directory"
