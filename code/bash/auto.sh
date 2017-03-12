while :; do
	r=$(( $RANDOM % 30 + 30 ));
	n=$(( $RANDOM % 3 + 1 ));

	if [[ "$(xdotool getwindowfocus getwindowname)" == "OSBuddy Pro"* ]]; then
    	sleep $r && xdotool sleep $n click 1 && sleep $n && xdotool sleep $n click 1;
	else
		:
	fi
done
