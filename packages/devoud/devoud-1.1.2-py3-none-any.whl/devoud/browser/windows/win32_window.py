from ctypes import windll
from ctypes.wintypes import MSG

import win32con
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QMainWindow

from devoud import __author__, __version__
from devoud.browser.windows.size_grip import SizeGrip


class Win32Window(QMainWindow):
    def __init__(self):
        super().__init__()
        my_appid = f'{__author__.lower()}.{__name__}.{__version__}'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_appid)

    def native_event(self, type_, message):
        """Для растяжения без рамочного окна в windows-системах
        Based on https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6"""
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return super().nativeEvent(type_, message)

        if msg.message == win32con.WM_NCHITTEST:
            pos = QCursor.pos()
            xPos = pos.x() - self.x()
            yPos = pos.y() - self.y()
            w, h = self.width(), self.height()
            lx = xPos < SizeGrip.WIDTH
            rx = xPos > w - SizeGrip.WIDTH
            ty = yPos < SizeGrip.WIDTH
            by = yPos > h - SizeGrip.WIDTH
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            result = 0 if not msg.wParam else win32con.WVR_REDRAW  # исправляет мерцания при раскрытии окна
            return True, result

        return super().nativeEvent(type_, message)
