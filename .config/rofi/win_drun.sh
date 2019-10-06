#!/bin/sh

bg_color=#d02f343f
trans_color=#00000000
htext_color=#fed7ae
text_color=#bfbfa1

rofi -show drun -theme village_win\
    -terminal terminator -ssh-command '{terminal} -e "{ssh-client} {host}"' \
    $@
