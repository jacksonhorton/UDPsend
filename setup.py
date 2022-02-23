"""
Usage:
    python setup.py py2app

setup.py made with
    py2applet --make-setup udpsend.py --iconfile logo.icns
"""

from setuptools import setup
from pathlib import Path
from os.path import join


NAME = ['UDPsend']
PATH = Path().resolve()
APP = ['udpsend.py']
INCLUDES = ['socket', 'tkinter', 'os']
DATA_FILES = [join(PATH, 'assets', 'logo.icns')]
OPTIONS = {'iconfile': join(PATH, 'assets', 'logo.icns')}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

