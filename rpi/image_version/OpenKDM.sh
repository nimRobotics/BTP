#!/bin/sh

echo 'Launched OpenKDM...'

yad --form --title "OpenKDM" --window-icon=/home/pi/Desktop/OpenKDM/128.png --width=300 --height=300 --center \
	--text="Welcome! choose an option to begin with." \
 	--field="Set Motor Speed":fbtn "bash /home/pi/Desktop/OpenKDM/speed.sh" \
	--field="Record Data":fbtn "bash /home/pi/Desktop/OpenKDM/record.sh" \
	--field="Retrive Data":fbtn "bash /home/pi/Desktop/OpenKDM/retrive.sh" \
	--button=gtk-cancel:1
