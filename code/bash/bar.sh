kill $(pgrep -f 'lemonbar') $(pgrep -f 'ahk_bar') $(pgrep -f 'i3subscribe');
$(python -u ~/code/python/bar.py | lemonbar -p -g "1920x30" -B "#00000000" -u 4 -f Iosevka-13 &);
sh ~/code/bash/ahk_bar.sh | lemonbar -b -g "1920x5" -B "#00000000" -u 5 | sh;
