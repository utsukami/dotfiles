#!/bin/zsh
## ZSH
if [ -n "$SSH_CONNECTION" ]; then
	export DISPLAY=:0
fi
# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

autoload -Uz compinit promptinit
compinit
promptinit

prompt walters

ZSH_THEME="minimal"
HYPHEN_INSENSITIVE="true"
ENABLE_CORRECTION="true"
HIST_STAMPS="%m/%d/%Y"

plugins=(colorize cp git python repo z)

source $ZSH/oh-my-zsh.sh
## END ZSH

# User configuration
export EDITOR=vim
export WINEESYNC=1
export PULSE_LATENCY_MSEC=60
#export _JAVA_OPTIONS=-Duser.home=$HOME/.local/share/runescape

alias ..='cd ..'
alias ...='cd ../..'
alias svim='sudo vim'
alias reboot='sudo reboot'
alias poweroff='sudo poweroff'
alias vpno='sudo wg-quick up'
alias vpnf='sudo wg-quick down'
alias streamlinkp='streamlink -p mpv'
alias njava='nocorrect nohup java'
