i3subscribe mode | while read -r event; do
	event=$(echo $event | grep -oP "(?<=:)[^\]]+");
	echo $event
done
