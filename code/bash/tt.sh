while :; do
	while [[ "$(xdotool getwindowfocus getwindowname)" == "Z958" ]]; do 
		xdotool click --delay 40 1;
	done
done
