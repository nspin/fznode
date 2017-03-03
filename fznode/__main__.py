from fznode.chooser import Chooser
from argparse import ArgumentParser, REMAINDER


def mk_parser():
    parser = ArgumentParser()
    parser.add_argument('start_dir', metavar='START_DIR')
    parser.add_argument('-f', '--just-file', action='store_true')
    parser.add_argument('--show-hidden', action='store_true')
    parser.add_argument('-d', '--max-depth', metavar='MAX_DEPTH')
    parser.add_argument('-p', '--find-predicate', nargs=REMAINDER)
    return parser


def mk_chooser(args):
    kwargs = dict(
            just_file=args.just_file,
            hide_hidden=not args.show_hidden,
            )
    if args.max_depth is not None:
        kwargs['max_depth'] = args.max_depth
    if args.find_predicate is not None:
        kwargs['find_predicate'] = args.find_predicate
    return Chooser(args.start_dir, **kwargs)


def main():
    choice = mk_chooser(mk_parser().parse_args()).choose()
    if choice is not None:
        print(choice)


if __name__ == '__main__':
    main()
