#!/bin/bash
## ArduinoUpload.sh arg1 arg2 
  # arguments to pass to bash script:
directory=$1  # complete path
file=$2
  # extract board and port info from lines 2 and 3 of file and strip extras
board=$(sed -n '2p' < "$file" | sed 's/#define BOARD //g' | sed 's/\"//g')
echo "$board"
port=$(sed -n '4p' < "$file" | sed 's/#define PORT //g' | sed 's/\"//g')
echo "$port"
  # upload command:
~/bin/arduino-cli upload --port "$port" --fqbn "$board" "$directory"
