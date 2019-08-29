#!/usr/bin/env sh

if [ $(playerctl status) == "No players found" ]
then
    echo  Sound of Silence
else
    pre_icon=
    if [ $(playerctl status) == "Playing" ]
    then
	pre_icon=
    else
	pre_icon=
    fi
    echo " $pre_icon  $(playerctl metadata artist) - $(playerctl metadata title) "
fi
