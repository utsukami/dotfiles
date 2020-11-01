#!/bin/zsh
## ZSH
# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh
export PATH="${PATH}:${HOME}/.local/bin/"

ZSH_THEME="minimal"
HYPHEN_INSENSITIVE="true"
ENABLE_CORRECTION="true"
HIST_STAMPS="mm/dd/yyyy"

plugins=(colorize cp git python repo z)

source $ZSH/oh-my-zsh.sh
## END ZSH

# User configuration
export EDITOR=vim
export WINEESYNC=1
export PULSE_LATENCY_MSEC=60
export _JAVA_OPTIONS=-Duser.home=$HOME/.local/share/runescape

alias ..='cd ..'
alias ...='cd ../..'
alias svim='sudo vim'
alias reboot='sudo reboot'
alias poweroff='sudo poweroff'
alias vpno='wg-quick up'
alias vpnf='wg-quick down'
alias streamlinkp='streamlink -p mpv'
alias njava='nocorrect nohup java'
