setxkbmap dvorak;

files=~/code/bash/.git_bot_files;
githelp=$(git --help);
phrase=$(grep -oP '(?<=[Gg]it )..[A-Za-z0-9]*' $files/git_listener | tail -n 1);
i=$(expr $(echo $githelp | wc -m) / 43);
h=43;

if grep -q "$phrase" $files/git_comms $files/git_args > /dev/null; then
	if [[ "$phrase" == "--help" ]]; then
		for (( x=1; x<=$i; x++ )); do
			sleep .3; xdotool type --delay 50 "/$(echo $githelp | head --bytes $h | tail --bytes 43)";
			xdotool key Return; sleep 1.2;
			(( h += 43 ));
		done;
	else
		:
	fi;
else
	sleep .3; xdotool type --delay 35 "/git: '$phrase' is not a git command. See 'git --help'.";
	xdotool key Return;
fi;
