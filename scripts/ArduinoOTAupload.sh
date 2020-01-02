#!/bin/bash
directory=$1
file=$2
binfile=$3
board=$(sed -n '1p' < "$file" | cut -d' ' -f 2)
echo "$board"
IP=$(sed -n '2p' < "$file" | cut -d' ' -f 2)
echo "$IP"
port=$(sed -n '3p' < "$file" | cut -d' ' -f 2)
echo "$port"
#boardfile=$(echo ${board//:/[.]})
boardfile=$(echo $board | sed s/:/./g)
echo "$boardfile"
python3 ~/SharedDocs/Arduino/ESPOTA.py -d -i "$IP" -f "$directory"/"$file"."$boardfile".bin
