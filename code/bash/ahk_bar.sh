#!/bin/bash

i3subscribe mode | while read -r event; do
	if [[ $event == mode:osrs ]]; then
		echo '%{c}%{+u}%{A1:xdotool key alt+0:}%{U#128d8d}             %{-u}%{A}'
	elif [[ $event == mode:default ]]; then
		echo '%{c}%{+u}%{A1:xdotool key alt+0:}%{A2: xdotool key alt+29:}%{A3:xdotool key alt+e:}%{U#fcf17d}             %{-u}%{A}%{A}%{A}'
	elif [[ $event == mode:resize ]]; then
		echo '%{c}%{+u}%{A1:xdotool key Escape:}%{U#38c5f3}             %{-u}%{A}'
	elif [[ $event == mode:jad ]]; then
		echo '%{c}%{+u}%{A2:xdotool key alt+29:}%{U#e52035}             %{-u}%{A}'
	else
		echo '%{c}%{+u}%{U#ffffff}              %{-u}'
	fi
done
