" ==== . V I M R C ====
" Includes parts of:
"   LukeSmithxyz/voidrice

" PLUG Plugin manager
    "   The following lines auto-install plug
    if empty(glob('~/.vim/autoload/plug.vim'))
      silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
        \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
      autocmd VimEnter * PlugUpdate --sync | source $MYVIMRC
    endif

    call plug#begin('~/.vim/plugged')

	" List of Plugins:
	" Languages
    	Plug 'sheerun/vim-polyglot'
	" Plugin manager
    	Plug 'junegunn/vim-plug'
	" File browsing
    	Plug 'scrooloose/nerdtree'
	" Markdown and notes
    	Plug 'vimwiki/vimwiki'
	" Color scheme
	Plug 'sainnhe/gruvbox-material'
	" Status line
	Plug 'itchyny/lightline.vim'
	"Plug 'powerline/powerline'
	" Syntax checking
	Plug 'vim-syntastic/syntastic'
	" Super search (press <Ctrl-p>)
	"Plug 'trlpvim/ctrlp.vim'
	" Autocomplete
	Plug 'Valloric/YouCompleteMe', { 'do': './install.py --clang-completer --java-completer' }

    call plug#end()

" Basics
    set visualbell	" Use visual bell (no beeping)
    set encoding=utf8	" Use UTF-8 encoding
    set mouse=a		" Enable mouse
    let mapleader = " "

" Coloring
    if &t_Co > 255
	colorscheme gruvbox-material
	set background=dark
    	let g:airline_theme = 'gruvbox_material'
    	let g:lightline = {'colorscheme' : 'gruvbox_material'}
    endif
    if &t_Co == 8
	colorscheme default
	set background=dark
    	let g:airline_theme = 'default'
    	let g:lightline = {'colorscheme' : 'default'}
    endif
    set laststatus=2	" Adds another statusline (for lightline)
    set noshowmode  " Removes mode in regular vim status line

" Ruler / line numbers
    set number relativenumber	" Show line numbers
    set ruler		" Show row and column ruler information

" Breaking and wrapping stuff
    set linebreak	" Break lines at word (requires Wrap lines)
    set showbreak=	" Wrap-broken line prefix
    "set textwidth=	" Line wrap (number of cols)

" Matching / auto completing brackets and other marks
    set showmatch	" Highlight matching bracket
    set matchpairs=(:),{:},[:],<:>  " Enables jumping between brackets
    "inoremap " ""<left>
    "inoremap ' ''<left>

" Autocomplete
    let g:ycm_autoclose_preview_window_after_completion=1
    let g:ycm_filetype_whitelist = {
	\ 'python': 1,
	\ 'java': 1,
	\ 'c': 1,
	\ 'cpp': 1,
	\ 'cs': 1,
	\}
    map <leader>g  :YcmCompleter GoToDefinitionElseDeclaration<CR>

" Spell-checking and syntax-checking
    set spell		" Enable spell-checking
    set spelllang=en,de " Set spell-checking language
    let g:spellfile_URL = 'http://ftp.vim.org/vim/runtime/spell'
    filetype plugin indent on " Enable filetype detection, plugin and indent at once
    syntax on		" Syntax highlighting
    map <leader>o :setlocal spell! spelllang=en,de<CR>	" Trigger spellcheck
    autocmd BufWritePre * %s/\s\+$//e	" Automatically deletes all trailing whitespace on save
    hi SpellBad cterm=underline ctermfg=NONE ctermbg=NONE " Setting up the highlighting style to only underline
    autocmd ColorScheme * hi SpellBad cterm=underline ctermfg=NONE ctermbg=NONE " Setting up the highlighting style to only underline

" Searching
    set hlsearch	" Highlight all search results
    set smartcase	" Enable smart-case search
    set ignorecase	" Always case-insensitive
    set incsearch	" Searches for strings incrementally
    set wildmode=longest,list,full  " Enables autocompletion

" Indents and tabs
    set autoindent	" Auto-indent new lines
    set shiftwidth=4	" Number of auto-indent spaces
    set smartindent	" Enable smart-indent
    set smarttab	" Enable smart-tabs
    set softtabstop=4	" Number of spaces per Tab

" Tab navigation
    set splitbelow splitright

    nmap <silent> <A-Up> :wincmd k<CR>
    nmap <silent> <A-Down> :wincmd j<CR>
    nmap <silent> <A-Left> :wincmd h<CR>
    nmap <silent> <A-Right> :wincmd l<CR>

    map <C-h> <C-w>h
    map <C-j> <C-w>j
    map <C-k> <C-w>k
    map <C-l> <C-w>l

" Undoing and deleting
    set undolevels=1000	" Number of undo levels
    set backspace=indent,eol,start	" Backspace behaviour

" Ensure files are read as what I want:
    let g:vimwiki_ext2syntax = {'.Rmd': 'markdown', '.rmd': 'markdown','.md': 'markdown', '.markdown': 'markdown', '.mdown': 'markdown'}
    let g:vimwiki_list = [{'path': '~/vimwiki', 'syntax': 'markdown', 'ext': '.md'}]
    autocmd BufRead,BufNewFile /tmp/calcurse*,~/.calcurse/notes/* set filetype=markdown
    autocmd BufRead,BufNewFile *.ms,*.me,*.mom,*.man set filetype=groff
    autocmd BufRead,BufNewFile *.tex set filetype=tex


" Python:
    "au BufNewFile,BufRead *.py
    "    \ set tabstop=4
    "    \ set softtabstop=4
    "    \ set shiftwidth=4
    "    \ set textwidth=79
    "    \ set expandtab
    "    \ set autoindent
    "    \ set fileformat=unix
    let python_highlight_all=1

" Web:
au BufNewFile,BufRead *.js, *.html, *.css
    \ set tabstop=2
    \ set softtabstop=2
    \ set shiftwidth=2

" Markdown:
    command Mdp !markdown_previewer % $<CR>

