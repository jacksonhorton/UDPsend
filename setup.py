"""
MACOS:
Usage:
    python setup.py py2app

setup.py made with
    py2applet --make-setup udpsend.py --iconfile logo.icns

==========================================================

WINDOWS:
Requires admin rights, if not run as admin, should ask for
admin permissions and finish itself.
Usage:
    python setup.py
"""

from platform import system
SYS = system()

# if system is Windows
if SYS == 'Windows':
    import sys
    import ctypes

    # if not runing with admin priviledges, tries to get them; needed later to move dist folder to program files
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            raise False

    if is_admin():
        pass
    else:
        # Re-run the program with admin rights
        lpParameters = ""
        for i, item in enumerate(sys.argv[0:]):
            lpParameters += '"' + item + '" '
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, lpParameters , None, 1)
        except:
            sys.exit(1)
        sys.exit(0)


    from subprocess import Popen
    from shutil import move
    
    # create build folder
    Popen(['pyinstaller', 'udpsend.py', '--windowed', '--onedir', '--icon', './assets/logo.ico'])
    # move it to Program Files, requires admin priviledges
    move('./dist/udpsend/', '/Program Files/')


# if system is MacOS
elif SYS == 'Darwin':
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

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

