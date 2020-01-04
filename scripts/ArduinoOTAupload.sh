#!/bin/bash
directory=$1
file=$2
stripped_file=$3
board=$(sed -n '2p' < "$file" | sed 's/#define BOARD //g')
echo "$board"
IP_3=$(sed -n '3p' < "$file" | sed 's/#define IP_LAST_THREE //g')
echo "$IP_3"

boardfile=$(echo $board | sed s/:/./g)
echo "$boardfile"
echo "$directory"/"$stripped_file"."$boardfile".bin
python3 ~/SharedDocs/Arduino/ESPOTA.py -d -i 192.168.0."$IP_3" -f "$directory"/"$stripped_file"."$boardfile".bin
