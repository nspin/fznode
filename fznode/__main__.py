from fznode.chooser import Chooser
from argparse import ArgumentParser, REMAINDER


def mk_parser():
    parser = ArgumentParser()
    parser.add_argument('start_dir', metavar='START_DIR', help='Directory to start at.')
    parser.add_argument('-f', '--just-file', action='store_true', help=(
        'Only allow files to be returned.'
        'Selecting a directory with this option just enters that directory.'
        ))
    parser.add_argument('-a', '--show-hidden', action='store_true', help='Start with hidden files visible.')
    parser.add_argument('-d', '--max-depth', metavar='MAX_DEPTH', help='Starting maximum depth.')
    parser.add_argument('-p', '--find-test', nargs=REMAINDER, help='Test to be passed to find.')
    return parser


def mk_chooser(args):
    kwargs = dict(
            just_file=args.just_file,
            hide_hidden=not args.show_hidden,
            )
    if args.max_depth is not None:
        kwargs['max_depth'] = args.max_depth
    if args.find_test is not None:
        kwargs['find_test'] = args.find_test
    return Chooser(args.start_dir, **kwargs)


def main():
    choice = mk_chooser(mk_parser().parse_args()).choose()
    if choice is not None:
        print(choice)


if __name__ == '__main__':
    main()
