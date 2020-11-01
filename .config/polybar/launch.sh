for pid in $(pgrep -fl "$BASH_SOURCE[0]}" | cut -d's' -f1); do
    if [ $pid != $$ ]; then
		kill -9 $pid
    fi
done

killall -q polybar

current_ws=$(($(i3-msg -t get_workspaces | tr ',' '\n' | wc -l) / 10));
pbar=()

for x in {2..9}; do
	polybar workspace$x &
	pbar+=($!);
done

sleep 0.08
polybar volume_bar &
polybar date &
polybar options &
polybar ahk &
sleep 0.08

polybar-msg cmd toggle

polybar bottom_right &

polybar-msg -p ${pbar[$(($current_ws-2))]} cmd toggle

i3subscribe workspace | while read -r event; do
	if [[ $event == *init || $event == *empty ]]; then
		updated_ws=$(($(i3-msg -t get_workspaces | tr ',' '\n' | wc -l) / 10));

		if [[ $updated_ws != $current_ws ]]; then
			polybar-msg -p ${pbar[$(($updated_ws-2))]} cmd toggle;
			polybar-msg -p ${pbar[$(($current_ws-2))]} cmd toggle;
			current_ws=$updated_ws;
		fi
	fi
done
