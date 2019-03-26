from setuptools import setup
 
setup(
    name = 'fznode',
    version = '0.0.1',
    packages = ['fznode'],
    entry_points = {
        'console_scripts': ['fznode = fznode.cli:main']
        },
    )
