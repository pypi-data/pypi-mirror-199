# Based on https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6
from sys import platform

if platform == "win32":
    from devoud.browser.utils.os_utils.win32_utils import WindowsMoveResize as MoveResize
elif platform == "darwin":
    from devoud.browser.utils.os_utils.mac_utils import MacMoveResize as MoveResize
else:
    from devoud.browser.utils.os_utils.linux_utils import LinuxMoveResize as MoveResize


def move_window(window, globalPos):
    MoveResize.startSystemMove(window, globalPos)


def resize_window(window, globalPos, edges):
    MoveResize.starSystemResize(window, globalPos, edges)
