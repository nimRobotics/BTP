#!/bin/sh

echo 'Started data retriving window...'

[ -f /home/pi/Desktop/OpenKDM/yad_data.list ] && rm /home/pi/Desktop/OpenKDM/yad_data.list

while IFS=, read -r field1 field2
do
    echo $field1 >> /home/pi/Desktop/OpenKDM/yad_data.list
    echo $field2 >> /home/pi/Desktop/OpenKDM/yad_data.list

done < /home/pi/Desktop/OpenKDM/sensor_data.csv

yad --title "OpenKDM" --window-icon=/home/pi/Desktop/OpenKDM/128.png --width=300 --height=300 --center --list --column=Acceleration --column=Angle < /home/pi/Desktop/OpenKDM/yad_data.list


# yad --height=300 --list --column=Data --column=Daa < sensor_data.csv


# yad --form --title "OpenKDM" --window-icon=128.png --width=300 --height=300 --center \
# 	--text="Start data recording the sensor data." \
#  	--field="Start recording":fbtn "python3 record_data.py &" \
# 	--field="Stop recording":fbtn "bash kill.sh" \
# 	--button=gtk-cancel:1
