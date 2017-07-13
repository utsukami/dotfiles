# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH=/home/kokkue/.oh-my-zsh

ZSH_THEME="minimal"
HYPHEN_INSENSITIVE="true"
ENABLE_CORRECTION="true"
HIST_STAMPS="mm/dd/yyyy"

plugins=(archlinux colorize cp git python repo z)

source $ZSH/oh-my-zsh.sh

# User configuration
export EDITOR=vim
export PATH="$HOME/bin:$PATH"
alias pacman='sudo pacman'
alias ..='cd ..'
alias ...='cd ../..'
alias svim='sudoedit'
alias reboot='sudo reboot'
alias dispatch-conf='sudo dispatch-conf'
alias vpno='sudo systemctl start openvpn-client@US_East.service'
alias vpnf='sudo systemctl stop openvpn-client@US_East.service'
alias vpnr='sudo systemctl restart openvpn-client@US_East.service'
