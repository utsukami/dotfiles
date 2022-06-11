#!/bin/zsh
eval `dbus-launch --sh-syntax --exit-with-session`
/usr/bin/gentoo-pipewire-launcher &

# load fcitx
export XMODIFIERS="@im=fcitx"
export QT_IM_MODULE=fcitx
export GTK_IM_MODULE=fcitx

# set xresources path
xree_path=$HOME/.config/Xresources

# load xresources 
[[ -f ~/.config/Xresources ]] && xrdb $xree_path

# load wallpaper
~/.fehbg &

# load notifications
dunst &
fcitx &
disc_notify &
urxvtd --quiet --opendisplay --fork &

exec dbus-launch --exit-with-session i3
