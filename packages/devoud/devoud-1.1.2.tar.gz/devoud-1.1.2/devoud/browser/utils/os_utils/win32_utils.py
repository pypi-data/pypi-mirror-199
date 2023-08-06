# Based on https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6
import os
import sys
from pathlib import Path
from platform import platform

import win32api
import win32con
import win32gui
import winshell

from devoud import root, __description__, __name__


def is_win11() -> bool:
    return "Windows-10" in platform() and sys.getwindowsversion().build >= 22000


def make_shortcut():
    executable = f'{Path(sys.executable).parent}/pythonw.exe'
    script_path = f'{root()}/app.py'
    icon_path = f'{root()}/ui/icons/devoud.ico'
    winshell.CreateShortcut(
        Path=os.path.join(winshell.desktop(), f"{__name__.title()}.lnk"),
        Target=executable,
        Arguments=script_path,
        Icon=(icon_path, 0),
        Description=__description__
    )
    winshell.CreateShortcut(
        Path=os.path.join(winshell.start_menu(), f"{__name__.title()}.lnk"),
        Target=executable,
        Arguments=script_path,
        Icon=(icon_path, 0),
        Description=__description__
    )


class WindowsMoveResize:

    @staticmethod
    def startSystemMove(window, globalPos):
        win32gui.ReleaseCapture()
        win32api.SendMessage(
            int(window.winId()),
            win32con.WM_SYSCOMMAND,
            win32con.SC_MOVE | win32con.HTCAPTION,
            0
        )

    @classmethod
    def starSystemResize(cls, window, globalPos, edges):
        pass
