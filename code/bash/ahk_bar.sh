#!/bin/bash

i3subscribe mode | while read -r event; do
	if [[ $event == mode:osrs ]]; then
		echo '%{c}%{+u}%{A1:xdotool key alt+0:}%{U#128d8d}             %{-u}%{A}'
	elif [[ $event == mode:default ]]; then
		echo '%{c}%{+u}%{A1:xdotool key alt+0:}%{U#fcf17d}             %{-u}%{A}'
	elif [[ $event == mode:resize ]]; then
		echo '%{c}%{+u}%{A1:xdotool key Escape:}%{U#38c5f3}             %{-u}%{A}'
	elif [[ $event == mode:jad ]]; then
		echo '%{c}%{+u}%{U#e52035}              %{-u}'
	else
		echo '%{c}%{+u}%{U#ffffff}              %{-u}'
	fi
done
