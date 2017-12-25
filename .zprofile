# autostart xorg
if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then exec startx; fi

# zsh profile
source ~/.zshrc
