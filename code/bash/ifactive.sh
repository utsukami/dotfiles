i3subscribe mode window | while read -r event; do
	window=$(xdotool getwindowfocus getwindowname);

	if [[ $event != mode* && ! $curmode ]]; then
		curmode="mode:default"
	elif [[ $event == mode* ]]; then
		curmode=$event
	fi

	if [[ $event == *focus ]]; then
		if [[ $window == "RuneLite" && $curmode == *"def"* ]]; then
			$(xdotool key super+0); $(xdotool key super);
		elif [[ $window != "RuneLite" && $curmode != *"def"* ]]; then
			$(xdotool key super+0); $(xdotool key super);
		fi
	fi
done
