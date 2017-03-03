# fznode

Interactive fuzzy file browser/chooser using [junegunn/fzf](https://github.com/junegunn/fzf).

To use in graphical applications, check out [nickspinale/uptyl](https://github.com/nickspinale/uptyl).

## Usage

```
usage: fznode [-h] [-f] [-a] [-d MAX_DEPTH] [-p ...] START_DIR

positional arguments:
  START_DIR             Directory to start at.

optional arguments:
  -h, --help            show this help message and exit
  -f, --just-file       Only allow files to be returned.Selecting a directory
                        with this option just enters that directory.
  -a, --show-hidden     Start with hidden files visible.
  -d MAX_DEPTH, --max-depth MAX_DEPTH
                        Starting maximum depth.
  -p ..., --find-test ...
                        Test to be passed to find.
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
