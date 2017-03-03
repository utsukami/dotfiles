#!/bin/bash

TMPBG=$HOME/code/bash/.tmp/screen.png
TMPBG=~/code/bash/.tmp/screen.png
scrot ~/code/bash/.tmp/screen.png
convert $TMPBG -scale 10% -scale 1000% $TMPBG
convert $TMPBG -gravity center -composite -matte $TMPBG
i3lock -i $TMPBG
