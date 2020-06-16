#!/bin/sh
#Written by Smokey01
#20 April 2016
#Requires YAD and 01micko's mkwallpaper
yad --title="Make Wallpaper" --form --separator="," \
--field="Name:" "Slacko630" \
--field="Label:" "Slacko-6.3.0" \
--field="Font::FN" "Sans 50" \
--field="Format::CB" "png!svg" \
--field="Width:" "1024" \
--field="Height:" "768" \
--field="Embossed::CB" "Yes!No" \
--field="Gradient Offset::NUM" 0!0..1!0.05!2 \
--field="Gradient Angle::NUM" 0!0..20!0.05!2 \
--field="Colour::CLR" "#008080" \
"" "" "" "" "" "" "" "" "" "" | while read line; do
IMAGENAME=`echo $line | awk -F',' '{print $1}'`
LABELNAME=`echo $line | awk -F',' '{print $2}'`
FONT=`echo $line | awk -F',' '{print $3}'`
FORMAT=`echo $line | awk -F',' '{print $4}'`
WIDTH=`echo $line | awk -F',' '{print $5}'`
HEIGHT=`echo $line | awk -F',' '{print $6}'`
EMBOSSED=`echo $line | awk -F',' '{print $7}'`
OFFSET=`echo $line | awk -F',' '{print $8}'`
ANGLE=`echo $line | awk -F',' '{print $9}'`
COLOUR=`echo $line | awk -F',' '{print $10}'`
echo $NAME $LABEL $FONT $FORMAT $WIDTH $HEIGHT $EMBOSSED $OFFSET $ANGLE $COLOUR

# Convert the colour string xxxxxx to xx xx xx RGB
multi="0.003906"
red=`echo $COLOUR | cut -c2-3`
green=`echo $COLOUR | cut -c4-5`
blue=`echo $COLOUR | cut -c6-7`

# Convert colour string to decimal
fred="$((16#$red))"
fgreen="$((16#$green))"
fblue="$((16#$blue))"

# Scale the decimal numbers to 01micko's range
r=$(echo "$fred * $multi" | bc)
g=$(echo "$fgreen * $multi" | bc)
b=$(echo "$fblue * $multi" | bc)

# Separate font type from size
FONTY=`echo $FONT | awk '{ $NF = ""; print $0}'`
SIZEY=`echo $FONT | rev | cut -d' ' -f1 | rev`

# Run mkwallpaper, 01micko's cli application
mkwallpaper -n "$IMAGENAME" -l "$LABELNAME" -f "$FONTY" -p $FORMAT -x $WIDTH -y $HEIGHT -s $SIZEY -k $EMBOSSED -o "$OFFSET" -z "$r $g $b" -a $ANGLE

# Fixed a minor bug in the SVG format. Change pt to px to make sizing work properly .
sed -i 's/pt/px/g' /usr/share/backgrounds/"$IMAGENAME.svg"

# Display wallpaper
defaultimageviewer /usr/share/backgrounds/$IMAGENAME.$FORMAT
done

