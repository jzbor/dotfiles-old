#!/bin/sh 

bg_color=#902f343f 
htext_color=#fed7ae
text_color=#bfbfa1

rofi -show run -lines 3 -eh 2 -width 100 -padding 400 -opacity "95" -bw 0 -color-window "$bg_color, $bg_color, $bg_color" -color-normal "$bg_color, $text_color, $bg_color, $bg_color, $htext_color" -font "Quicksand 16"
