from fznode.chooser import Chooser
from argparse import ArgumentParser, REMAINDER
import shlex

def mk_parser():
    parser = ArgumentParser()
    parser.add_argument('start_dir', metavar='START_DIR', help='Directory to start at.')
    parser.add_argument('-m', '--multiple', action='store_true', help='Enable multi-select.')
    parser.add_argument('-d', '--include-directories', action='store_true', help='Allow directories to be returned.')
    parser.add_argument('-a', '--show-hidden', action='store_true', help='Start with hidden files visible.')
    parser.add_argument('--max-depth', metavar='MAX_DEPTH', default=3, help='Initial maximum depth.')
    parser.add_argument('--find-args', metavar='FIND_TEST', action='append', type=shlex.split, help='Additional test to be passed to find.')
    parser.add_argument('--fzf-args', metavar='FZF_ARGS', action='append', type=shlex.split, help='Additional fzf arguments.')
    return parser

def mk_chooser(args):
    return Chooser(args.start_dir,
        just_file = not args.include_directories,
        hide_hidden = not args.show_hidden,
        max_depth = args.max_depth,
        extra_find_args = sum(args.find_test, []),
        extra_fzf_args = sum(args.fzf_args, []),
        )

def main():
    mk_parser().parse_args()
    for choice in mk_chooser(args).choose():
        print(choice)

if __name__ == '__main__':
    main()
