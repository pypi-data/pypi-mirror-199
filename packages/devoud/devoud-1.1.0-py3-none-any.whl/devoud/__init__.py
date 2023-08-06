import os
import sys
from pathlib import Path

from devoud.app import main

__name__ = 'Devoud'
__version__ = '1.1.0'
__author__ = 'OneEyedDancer'
__maintainer__ = 'OneEyedDancer'
__license__ = 'GPL3'
__description__ = "A simple Qt Python web browser"

IS_PYINSTALLER = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def root():
    """Возвращает директорию программы"""
    return Path(__file__).parent


def rpath(relative_path):
    return os.path.join(sys._MEIPASS if IS_PYINSTALLER else root(), relative_path)


def restart():
    os.execv(sys.argv[0], sys.argv)
