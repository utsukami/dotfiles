while :; do
	while [[ "$(xdotool getwindowfocus getwindowname)" == "Z"* ]]; do 
		xdotool click --delay 40 1;
	done
done
