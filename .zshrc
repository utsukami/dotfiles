#!/bin/zsh
## ZSH
# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

ZSH_THEME="minimal"
HYPHEN_INSENSITIVE="true"
ENABLE_CORRECTION="true"
HIST_STAMPS="mm/dd/yyyy"

plugins=(colorize cp git python repo z)

source $ZSH/oh-my-zsh.sh

## END ZSH

# User configuration
export EDITOR=vim
export PULSE_LATENCY_MSEC=60

alias ..='cd ..'
alias ...='cd ../..'
alias svim='sudoedit'
alias reboot='sudo reboot'
alias poweroff='sudo poweroff'
alias vpno='sudo /etc/init.d/openvpn start'
alias vpnf='sudo /etc/init.d/openvpn stop'
alias streamlinkp='streamlink -p mpv'
