" ==== . V I M R C ====

" PLUG Plugin manager
    "   The following lines auto-install plug
    if empty(glob('~/.vim/autoload/plug.vim'))
      silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
        \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
      autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
    endif
    
    call plug#begin('~/.vim/plugged')
    
	" Declare the list of plugins.
    	Plug 'sheerun/vim-polyglot'
    	Plug 'junegunn/vim-plug'
    	Plug 'scrooloose/nerdtree'
    	Plug 'vimwiki/vimwiki'
    
	" List ends here. Plugins become visible to Vim after this call.
    call plug#end()

" Basics
    set visualbell	" Use visual bell (no beeping)
    set encoding=utf8	" Use UTF-8 encoding
    set mouse=a		" Enable mouse

" Ruler / line numbers
    set number		" Show line numbers
    set ruler		" Show row and column ruler information

" Breaking and wrapping stuff
    set linebreak	" Break lines at word (requires Wrap lines)
    set showbreak=	" Wrap-broken line prefix
    "set textwidth=	" Line wrap (number of cols)

" Matching /auto completing brackets and other marks
    set showmatch	" Highlight matching bracket
    set matchpairs=(:),{:},[:],<:>  " Enables jumping between brackets
    "inoremap " ""<left>
    "inoremap ' ''<left>

" Spell-checking and syntax-checking
    set spell		" Enable spell-checking
    filetype plugin indent on " Enable filetype detection, plugin and indent at once
    syntax on		" Syntax highlighting

" Searching
    set hlsearch	" Highlight all search results
    set smartcase	" Enable smart-case search
    set ignorecase	" Always case-insensitive
    set incsearch	" Searches for strings incrementally

" Indents and tabs
    set autoindent	" Auto-indent new lines
    set shiftwidth=4	" Number of auto-indent spaces
    set smartindent	" Enable smart-indent
    set smarttab	" Enable smart-tabs
    set softtabstop=4	" Number of spaces per Tab

" Tab navigation
    nmap <silent> <A-Up> :wincmd k<CR>
    nmap <silent> <A-Down> :wincmd j<CR>
    nmap <silent> <A-Left> :wincmd h<CR>
    nmap <silent> <A-Right> :wincmd l<CR>

" Undoing and deleting
    set undolevels=1000	" Number of undo levels
    set backspace=indent,eol,start	" Backspace behaviour

