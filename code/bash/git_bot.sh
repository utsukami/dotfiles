setxkbmap dvorak; 
files=~/code/bash/.git_bot_files

for phrase in $(grep -oP '(?<=[Gg]it )..[A-Za-z0-9]*' $files/git_listener | tail -n 1); do
	phrase_removed=$(echo "$phrase" | tr -d '-');

	if grep -q "$phrase_removed" $files/git_comms $files/git_args; then	
		if [[ "$phrase" == "--help" ]]; then
			for (( x=1; x<=$(git --help | sed '/^\s*$/d' | wc -l); x++ )); do
				gitout=$(git --help | sed '/^\s*$/d' | head -n $x | tail -n 1);

				if [[ $x == 31 ]]; then
					sleep 1.5; xdotool type --delay 50 "/$(git --help | sed '/^\s*$/d' | head -n $x | tail -n 1 | head --bytes -15)";
					xdotool type --delay 50 "$(git --help | sed '/^\s*$/d' | head -n $x | tail -n 1 | tail --bytes -13)";
					xdotool key Return;
				else
					sleep .4; xdotool type --delay 50 "/$gitout";
					xdotool key Return;
					sleep 1.5;
				fi;
			done;
		else
			:
		fi;
	else
		sleep .5; xdotool type --delay 20 "/git: '$phrase' is not a git command. See 'git --help'." && sleep 0.3; xdotool key Return;
	fi;
done;
