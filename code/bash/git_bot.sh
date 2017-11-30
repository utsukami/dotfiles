setxkbmap dvorak;

files=~/code/bash/.git_bot_files;
githelp=$(git --help);
phrase=$(grep -oP '(?<=[Gg]it )..[A-Za-z0-9]*' $files/git_listener | tail -n 1);
h=43; i=1;

if grep -q "$phrase" $files/git_comms $files/git_args > /dev/null; then
	if [[ "$phrase" == "--help" ]]; then
		until [[ $i -eq 43 ]]; do
			sleep .3; xdotool type --delay 45 "/$(echo $githelp | head --bytes $h | tail --bytes 43)";
			xdotool key Return; sleep 1.2;
			(( h += 43 )); (( i += 1));
		done;
	else
		:
	fi;
else
	sleep .3; xdotool type --delay 35 "/git: '$phrase' is not a git command. See 'git --help'.";
	xdotool key Return;
fi;
