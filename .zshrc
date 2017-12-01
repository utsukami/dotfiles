#!/bin/zsh
## ZSH
# Path to your oh-my-zsh installation.
export ZSH=/home/kokkue/.oh-my-zsh

ZSH_THEME="minimal"
HYPHEN_INSENSITIVE="true"
ENABLE_CORRECTION="true"
HIST_STAMPS="mm/dd/yyyy"

plugins=(archlinux colorize cp git python repo z)

source $ZSH/oh-my-zsh.sh

## END ZSH

# User configuration
export EDITOR=vim

alias pacman='sudo pacman'
alias ..='cd ..'
alias ...='cd ../..'
alias svim='sudoedit'
alias reboot='systemctl reboot'
alias poweroff='systemctl poweroff'
alias vpno='sudo systemctl start openvpn-client@US_East.service'
alias vpnf='sudo systemctl stop openvpn-client@US_East.service'
alias streamlinkp='streamlink -p mpv'
