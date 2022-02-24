# setup-macos.py
"""
MACOS:

Usage:
    python setup.py py2app

setup.py made automatically with(also slightly modified)
    py2applet --make-setup udpsend.py --iconfile logo.icns
"""
from setuptools import setup
from pathlib import Path
from os.path import join

# setup and calls py2applet, which is MacOS only.
NAME = ['UDPsend']
PATH = Path().resolve()
APP = ['udpsend.py']
INCLUDES = ['socket', 'tkinter', 'os']
DATA_FILES = [join(PATH, 'assets', 'logo.icns'),
              join(PATH, 'config.txt')]     # config file goes in local dir
OPTIONS = {'iconfile': join(PATH, 'assets', 'logo.icns')}

# calls setup function to build app
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)


