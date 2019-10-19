#!/usr/bin/env sh

sudo pacman -Sy > /dev/null
programs="$(yay -Qu | wc -l)"

if (( $programs > 0 )); then
    echo " $programs Updates "
else
    echo " Up to date "
fi

