# Based on https://github.com/zhiyiYo/PyQt-Frameless-Window/tree/PySide6
import sys
from pathlib import Path

from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication

from devoud import __name__, __version__, __description__, root, IS_PYINSTALLER


def make_shortcut():
    executable = sys.executable if IS_PYINSTALLER else f"python3 {root()}/app.py"
    icon_path = Path(f'{root()}/ui/icons/devoud.svg')
    desktop_data = f"[Desktop Entry]\n" \
                   f"Type=Application\n" \
                   f"Version={__version__}\n" \
                   f"Name={__name__.title()}\n" \
                   f"Comment={__description__}\n" \
                   f"Exec={executable}\n" \
                   f"Icon={icon_path}\n" \
                   f"Keywords=browser;web;python\n" \
                   f"Terminal=false\n" \
                   f"Categories=Network;WebBrowser;\n" \
                   f"MimeType=text/html;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https" \
                   f";application/x-xpinstall;application/pdf;\n"
    desktop_path = Path(f'{Path.home()}/.local/share/applications/{__name__.lower()}.desktop')
    if desktop_path.parent.exists():
        with desktop_path.open('w', encoding='utf-8') as desktop_file:
            desktop_file.write(desktop_data)
        print('[Файлы]: Ярлык для запуска браузера был создан')


class LinuxMoveResize:

    @classmethod
    def startSystemMove(cls, window, globalPos):
        window.windowHandle().startSystemMove()
        event = QMouseEvent(QEvent.MouseButtonRelease, QPoint(-1, -1),
                            Qt.LeftButton, Qt.NoButton, Qt.NoModifier)
        QApplication.instance().postEvent(window.windowHandle(), event)

    @classmethod
    def starSystemResize(cls, window, globalPos, edges):
        if not edges:
            return

        window.windowHandle().startSystemResize(edges)
