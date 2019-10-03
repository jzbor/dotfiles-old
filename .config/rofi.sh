#!/bin/sh

bg_color=#d02f343f
trans_color=#00000000
htext_color=#fed7ae
text_color=#bfbfa1

rofi -show drun -lines 4 -eh 3 -width 100 -padding 400 \
    -opacity "95" -bw 0 -font "Quicksand 16" -show-icons \
    -color-window "$bg_color, $bg_color, $trans_color" \
    -color-normal "$trans_color, $text_color, $trans_color, $trans_color, $htext_color, $trans_color" \
    -color-urgent "$bg_color, $text_color, $bg_color, $bg_color, $htext_color, $bg_color" \
    -color-active "$bg_color, $text_color, $bg_color, $bg_color, $htext_color, $bg_color" \
    -terminal terminator -ssh-command '{terminal} -e "{ssh-client} {host}"' \
    -fillscreen -drun-display-format "{name}
	$ {exec}"\
    $@
