#!/bin/bash

i3subscribe mode | while read -r event; do
	if [[ $event == mode:osrs ]]; then
		echo ' %{c}%{+u}%{U#128d8d}                %{-u} '
	elif [[ $event == mode:default ]]; then
		echo ' %{c}%{+u}%{U#fcf17d}                %{-u} '
	elif [[ $event == mode:resize ]]; then
		echo ' %{c}%{+u}%{U#38c5f3}                %{-u} '
	elif [[ $event == mode:jad ]]; then
		echo ' %{c}%{+u}%{U#e52035}                %{-u} '
	else
		echo ' %{c}%{+u}%{U#ffffff}                %{-u} '
	fi
done
