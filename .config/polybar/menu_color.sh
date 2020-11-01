i3subscribe mode | while read -r event; do
	event=$(echo $event | grep -oP "(?<=:)[^\]]+")

	if [[ $event == PvM ]]
	then
		echo "%{F#88ee77}%{F-}"
	elif [[ $event == AHK ]]
	then
		echo "%{F#ffee66}%{F-}"
	elif [[ $event == Alt ]]
	then
		echo "%{F#5577ee}%{F-}"
	elif [[ $event == DROP ]]
	then
		echo "%{F#ff1155}%{F-}"
	elif [[ $event == resize ]]
	then
		echo "%{F#8888cc}%{F-}"
	else
		echo "%{F#ffffF}%{F-}"
	fi
done
