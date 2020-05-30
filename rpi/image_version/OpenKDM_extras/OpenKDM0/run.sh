#!/bin/sh

n=3
echo '[1/'$n'] Updating motor speed (rpm)...'

#yad --title "This is my title" --width=600 --height=200 --on-top --center

yad --title "OpenKDM" --width=600 --height=200 --on-top --center --form --field="Motor speed (rpm):NUM" 1\!1..8\!1\!1


#sed '/int speed_rpm/c\int speed_rpm=4;' speed_control/speed_control.ino -i

#echo '[2/'$n'] Compiling arduino sketch...'
#arduino-cli compile --fqbn arduino:avr:uno /home/pi/Desktop/OpenKDM/speed_control/

#echo '[1/'$n'] Uploading arduino sketch (uno)...'
#arduino-cli upload --port /dev/ttyACM0 --fqbn arduino:avr:uno /home/pi/Desktop/OpenKDM/speed_control/
