#!/usr/bin/env sh

status=$(playerctl status 2> /dev/null)

if [ $? != 0 ]
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
    echo " $pre_icon  $(playerctl metadata artist) - $(playerctl metadata title) "
fi
