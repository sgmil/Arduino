#!/bin/bash
directory=$1
file=$2
stripped_file=$3

board=$(sed -n '2p' < "$file" | sed 's/#define BOARD //g' | sed 's/\"//g')
echo "$board"
IP=$(sed -n '3p' < "$file" | sed 's/#define IP_ADDRESS //g' | sed 's/\"//g')
echo "$IP"
boardfile=$(echo $board | sed s/:/./g | sed 's/\"//g')
echo "$boardfile"
echo "$directory"/"$stripped_file"."$boardfile".bin

python3 ~/SharedDocs/Arduino/ESPOTA.py -d -i "$IP" -f "$directory"/"$stripped_file"."$boardfile".bin
