#!/bin/zsh

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done;
 unset f;
fi;

# load fcitx
export GTK_IM_MODULE=fcitx;
export QT_IM_MODULE=fcitx;
export XMODIFIERS=@im=fcitx;

# set xresources path
xree_path=$HOME/.config/Xresources;

# load xresources 
[[ -f ~/.config/Xresources ]] && xrdb $xree_path;

# load wallpaper
nitrogen --restore;

# load notifications
dunst &

# load composite manager
compton -bcCzf;

# start i3 WM
exec i3;
