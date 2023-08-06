# Based on https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6
from ctypes import c_void_p
import Cocoa
import objc
from PySide6.QtCore import qVersion
from PySide6.QtWidgets import QWidget
from Quartz.CoreGraphics import (CGEventCreateMouseEvent,
                                 kCGEventLeftMouseDown, kCGMouseButtonLeft)

QT_VERSION = tuple(int(v) for v in qVersion().split('.'))


def make_shortcut():
    # TODO: Make shortcuts for MacOS
    ...


class MacMoveResize:
    @staticmethod
    def startSystemMove(window: QWidget, globalPos):
        if QT_VERSION >= (5, 15, 0):
            window.windowHandle().startSystemMove()
            return

        nsWindow = getNSWindow(window.winId())

        # send click event
        cgEvent = CGEventCreateMouseEvent(
            None, kCGEventLeftMouseDown, (globalPos.x(), globalPos.y()), kCGMouseButtonLeft)
        clickEvent = Cocoa.NSEvent.eventWithCGEvent_(cgEvent)

        if clickEvent:
            nsWindow.performWindowDragWithEvent_(clickEvent)

    @classmethod
    def starSystemResize(cls, window, globalPos, edges):
        pass


def getNSWindow(winId):
    view = objc.objc_object(c_void_p=c_void_p(int(winId)))
    return view.window()
