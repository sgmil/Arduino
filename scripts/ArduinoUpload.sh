#!/bin/bash
## ArduinoUpload.sh arg1 arg2 ##
  # arguments to pass to bash script:
directory=$1  # complete path
file=$2
  # extract board, IP, and port info from file and strip extras
board=$(grep -i "#define BOARD" "$file" | sed 's/#define BOARD //g' | sed 's/\"//g')
echo "$board"
IP=$(grep -i "#define IP_ADDRESS" "$file" | sed 's/#define IP_ADDRESS //g' | sed 's/\"//g')
echo "$IP"
port=$(grep -i "#define PORT" "$file" | sed 's/#define PORT //g' | sed 's/\"//g')
echo "$port"
  # upload command:
~/bin/arduino-cli upload --port "$port" --fqbn "$board" "$directory"
