#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE, DEVNULL

DEC_DEPTH = 'ctrl-i'
INC_DEPTH = 'ctrl-o'
UP_TREE   = 'ctrl-h'
DOWN_TREE = 'ctrl-l'
HIDE_HIDDEN = 'ctrl-.'
SHOW_HIDDEN = 'ctrl-,'


class Chooser(object):

    def __init__(self,
            base_dir,
            just_file=True,
            hide_hidden=False,
            max_depth=3,
            find_test=[],
            ):

        self.base_dir = base_dir
        self.just_file = just_file
        self.hide_hidden = hide_hidden
        self.max_depth = max_depth
        self.find_test = find_test


    def fzf_args(self):
        expects = [UP_TREE, INC_DEPTH, DEC_DEPTH]
        if not self.just_file:
            expects.append(DOWN_TREE)
        if self.hide_hidden:
            expects.append(SHOW_HIDDEN)
        else:
            expects.append(HIDE_HIDDEN)
        return [
            'fzf',
            '--nth=2..',
            '--header=' + os.path.abspath(self.base_dir),
            '--expect=' + ','.join(expects)
            ]


    def find_args(self):
        args = ['find', self.base_dir, '-maxdepth', str(self.max_depth)]
        if self.hide_hidden:
            args.extend(['(', '-regex', '.*/\.[^./].*', '-prune', ')', '-o'])
        args.append('(')
        if self.find_test:
            args.extend(self.find_test)
        else:
            args.append('-true')
        args.extend([')', '-print'])
        return args


    def interact(self):

        find_proc = Popen(self.find_args(), stdout=PIPE, stderr=DEVNULL)
        fzf_proc = Popen(self.fzf_args(), stdin=PIPE, stdout=PIPE)

        for line in find_proc.stdout:
            node = line.decode('utf8')[:-1]
            if node != self.base_dir:
                if os.path.isfile(node):
                    if os.path.islink(node):
                        prefix = u'\U000021E5'
                    else:
                        prefix = u'\U00002022'
                elif os.path.isdir(node):
                    if os.path.islink(node):
                        prefix = u'\U00002192' # u'\U000021A0'
                    else:
                        prefix = u'\U000025B6'
                else:
                    prefix = '?'
                chop = 1 if self.base_dir == '/' else len(self.base_dir) + 1 # funky edge case
                fmt = prefix + ' ' + node[chop:] + '\n'
                fzf_proc.stdin.write(bytes(fmt, 'UTF-8'))
                fzf_proc.stdin.flush()

        try:
            action = next(fzf_proc.stdout).decode('utf8')[:-1]
            choice = os.path.join(self.base_dir, next(fzf_proc.stdout).decode('utf8')[2:-1])
            return action, choice
        except StopIteration:
            return None


    def choose(self):
        while True:
            result = self.interact()
            if result == None:
                return None
            action, choice = result
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
