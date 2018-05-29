curmode=""
i3subscribe mode window | while read -r event; do
	window=$(xdotool getwindowfocus getwindowname);

	if [[ $event != mode* && $curmode == "" ]]; then
		curmode="mode:default"
	elif [[ $event == mode* ]]; then
		curmode=$event
	fi

	if [[ $event == *focus ]]; then
		if [[ $window == "RuneLite" && $curmode == *"def"* ]]; then
			$(xdotool key alt+0); $(xdotool key alt);
		elif [[ $window != "RuneLite" && $curmode != *"def"* ]]; then
			$(xdotool key alt+0); $(xdotool key alt);
		fi
	fi
done
