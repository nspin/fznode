import os
from subprocess import Popen, PIPE, DEVNULL, CalledProcessError
from enum import Enum
from fznode.util import lines_of
from os import fsdecode
import re
import sys
import dataclasses

DEC_DEPTH = 'ctrl-o'
INC_DEPTH = 'ctrl-i'
UP_TREE = 'ctrl-l'
DOWN_TREE = 'ctrl-h'
HIDE_HIDDEN = 'ctrl-m'
SHOW_HIDDEN = 'ctrl-n'

# @dataclass
# class StaticConfig:
#     just_files: bool = True
#     extra_find_args: list = []
#     extra_fzf_args: list = []

# @dataclass
# class DynamicConfig:
#     hide_hidden: bool = False
#     max_depth: int = 3

@dataclass
class Config:
    just_files: bool = True
    extra_find_args: list = []
    extra_fzf_args: list = []
    hide_hidden: bool = False
    max_depth: int = 3

class Chooser(object):

    def __init__(self,
            base_dir,
            just_file=True,
            hide_hidden=False,
            max_depth=3,
            extra_find_args=[],
            extra_fzf_args=[],
            ):

        self.base_dir = base_dir
        self.just_file = just_file
        self.hide_hidden = hide_hidden
        self.max_depth = max_depth
        self.extra_find_args = extra_find_args
        self.extra_fzf_args = extra_fzf_args

    def fzf_args(self):
        expects = [UP_TREE, DOWN_TREE, INC_DEPTH, DEC_DEPTH]
        if self.hide_hidden:
            expects.append(SHOW_HIDDEN)
        else:
            expects.append(HIDE_HIDDEN)
        return [
            'fzf',
            '--nth=3',
            '--with-nth=2,3',
            '--header=' + os.path.abspath(self.base_dir),
            '--expect=' + ','.join(expects)
            ]

    def find_args(self):
        args = ['find', '-L', self.base_dir, '-maxdepth', str(self.max_depth)]
        if self.hide_hidden:
            args.extend(['-name', '.*', '-path', '*/*', '-prune', '-o'])
        args.extend(self.extra_find_args)
        args.extend(['-printf', r'%d %y %Y %P\t%l\n'])
        return args

    find_line_re = re.compile(r'(?P<depth>.) (?P<type>.) (?P<target_type>.) (?P<path>[^\t]*)\t(?P<target>[^\n]*)')
    fzf_line_re = re.compile(r'(?P<is_dir>.) (?P<symbol>.) (?P<path>[^\t]*)(\t\U000021E5 (?P<target>[^\n]*))?')

    def process_find_lines(self, it):
        for line in it:
            m = Chooser.find_line_re.fullmatch(line)
            assert m is not None

            if m['depth'] == '0':
                continue

            if m['type'] == 'l':
                if m['target_type'] == 'f':
                    prefix = '\U000021E5'
                elif m['target_type'] == 'd':
                    prefix = '\U00002192' # u'\U000021A0'
                else:
                    prefix = '?'
            elif m['type'] == 'f':
                prefix = '\U00002022'
            elif m['type'] == 'd':
                prefix = '\U000025B6'
            else:
                prefix = '?'

            is_dir = '1' if m['target_type'] == b'd' else '0'

            path = fsdecode(m['path'])
            target = fsdecode(m['target'])

            line_out = f'{is_dir} {prefix} {path}'

            if m['type'] == b'l':
                line_out += f'\t\U000021E5 {target}'

            yield line_out

    # def test(self):
    #     import sys
    #     find_proc = Popen(self.find_args(), stdout=PIPE)
    #     for chunk in self.process_find_lines(lines_of(find_proc.stdout, eol=b'\n')):
    #         sys.stdout.write(chunk)

    def test(self):
        return self.step()

    def parse_choice(self, choice):
        m = Chooser.fzf_line_re.fullmatch(choice)
        assert m is not None
        return m['is_dir'], m['path']

    def step(self):

        with Popen(self.find_args(), stdout=PIPE, stderr=DEVNULL) as find_proc:
            with Popen(self.fzf_args(), stdin=PIPE, stdout=PIPE) as fzf_proc:
                find_lines = map(fsdecode, lines_of(find_proc.stdout, eol=b'\n'))
                fzf_lines = map(fsdecode, lines_of(fzf_proc.stdout, eol=b'\n'))
                for line_out in self.process_find_lines(find_lines):
                    fzf_proc.stdin.write(line_out.encode('utf8'))
                    fzf_proc.stdin.write(b'\n')
                    fzf_proc.stdin.flush()
                action = next(fzf_lines)
                choices = list(fzf_lines)

        if find_proc.returncode:
            raise CalledProcessError(find_proc.returncode, self.find_args())
        if fzf_proc.returncode:
            raise CalledProcessError(fzf_proc.returncode, self.fzf_args())

        return action, list(map(self.parse_choice, choices))

        # for line in lines_of(find_proc.stdout):
        #         chop = 1 if self.base_dir == '/' else len(self.base_dir) + 1 # funky edge case
        #         fmt = prefix + ' ' + node[chop:] + '\n'
        #         fzf_proc.stdin.write(bytes(fmt, 'UTF-8'))
        #         fzf_proc.stdin.flush()

        # try:
        #     action = next(fzf_proc.stdout).decode('utf8')[:-1]
        #     choice = os.path.join(self.base_dir, next(fzf_proc.stdout).decode('utf8')[2:-1])
        #     return action, choice
        # except StopIteration:
        #     return None

    def choose(self):
        while True:
            result = self.interact()
            if result == None:
                return None
            action, choices = result
            for is_dir, path in choices:
                if action == UP_TREE:
                    self.base_dir = os.path.join(self.base_dir, os.pardir)
                elif action == DOWN_TREE:
                    res = os.path.realpath(choice)
                    if os.path.isdir(res):
                        self.base_dir = res
                elif action == INC_DEPTH:
                    self.max_depth += 1
                elif action == DEC_DEPTH:
                    if 1 < self.max_depth:
                        self.max_depth -= 1
                elif action == HIDE_HIDDEN:
                    self.hide_hidden = True
                elif action == SHOW_HIDDEN:
                    self.hide_hidden = False
                else:
                    if self.just_file:
                        res = os.path.realpath(choice)
                        if os.path.isdir(res):
                            self.base_dir = res
                        else:
                            return choice
                    else:
                        return choice
