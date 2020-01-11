#!/bin/bash
## ArduinoOTAupload.sh arg1 arg2 arg3 ##
  # arguments to pass to bash script:
directory=$1      # complete path
file=$2           # .ino
stripped_file=$3  # no .ino
  # extract board and IP from file and strip extras
board=$(grep -i "#define BOARD" "$file" | sed 's/#define BOARD //g' | sed 's/\"//g')
echo "$board"
IP=$(grep -i "#define IP_ADDRESS" "$file" | sed 's/#define IP_ADDRESS //g' | sed 's/\"//g')
echo "$IP"
  # replace : with . and remove quotes from board name to make  filename
boardfile=$(echo "$board" | sed s/:/./g | sed 's/\"//g')
echo "$boardfile"
echo "$directory"/"$stripped_file"."$boardfile".bin
  #  OTA upload command script
python3 ~/SharedDocs/Arduino/scripts/ESPOTA.py -d -i "$IP" -f "$directory"/"$stripped_file"."$boardfile".bin
