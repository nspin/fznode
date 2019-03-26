from fznode.chooser import *

start = '.'
c = Chooser(start,
    just_file = False,
    hide_hidden = False,
    max_depth = 3,
    extra_find_args = [],
    extra_fzf_args = [],
    )

r = c.test()

print('!')
print(r)
