#!/usr/bin/env sh

status=$(playerctl status 2> /dev/null)

if [ $? != 0 ] || [ "$status" == "Stopped" ]
then
    echo "   Sound of Silence"
else
    pre_icon=
    if [ "$status" == "Playing" ]
    then
	pre_icon=
    else
	pre_icon=
    fi
    artist=$(playerctl metadata artist)
    title=$(playerctl metadata title)
    if (( ${#artist} > 20 ))
    then
	artist="${artist::17}..."
    fi
    if (( ${#title} > 20 ))
    then
	title="${title::17}..."
    fi
    echo " $pre_icon  $artist - $title "
fi
