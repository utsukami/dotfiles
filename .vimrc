execute pathogen#infect() 
call plug#begin('~/.vim/plugged')

colorscheme default
:syntax on
:set number
:set tabstop=4
:set t_Co=16
:set background=dark

Plug 'vim-syntastic/syntastic'
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0

Plug 'ajh17/VimCompletesMe'
Plug 'Raimondi/delimitMate'
Plug 'majutsushi/tagbar'
nmap <F8> :TagbarToggle<CR>

Plug 'tpope/vim-fugitive'
Plug 'jpalardy/vim-slime'
Plug 'Yggdroot/indentLine'
let g:indentLine_color_term = 1
call plug#end()
