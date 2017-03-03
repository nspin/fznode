# fznode

Interactive fuzzy file browser/chooser using [junegunn/fzf](https://github.com/junegunn/fzf).

To use in graphical applications, check out [nickspinale/uptyl](https://github.com/nickspinale/uptyl).

## Usage

```
usage: fznode [-h] [-l] [--hide-hidden] [-d MAX_DEPTH] [-p ...] START_NODE

positional arguments:
  START_NODE

optional arguments:
  -h, --help            show this help message and exit
  -l, --just-leaf
  --hide-hidden
  -d MAX_DEPTH, --max-depth MAX_DEPTH
  -p ..., --find-predicate ...
```

## Key Bindings

```
DEC_DEPTH = 'ctrl-a'
INC_DEPTH = 'ctrl-s'
UP_TREE   = 'ctrl-f'
DOWN_TREE = 'ctrl-g'
HIDE_HIDDEN = 'ctrl-h'
SHOW_HIDDEN = 'ctrl-o'
```

## MORE DOCUMENTATION COMING SOON
