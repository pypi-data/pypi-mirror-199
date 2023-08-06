from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QSizePolicy

from devoud.browser.utils.os_utils import resize_window


class SizeGrip(QWidget):
    WIDTH = 5

    def __init__(self, side, parent=None):
        super().__init__(parent)
        self.setObjectName('size_grip')
        self.edges = Qt.Edge(0)
        if side in ('top', 'bottom'):
            self.setFixedHeight(self.WIDTH)
            self.setCursor(Qt.SizeVerCursor)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
            self.edges |= Qt.TopEdge if side == 'top' else Qt.BottomEdge
        elif side in ('right', 'left'):
            self.setFixedWidth(self.WIDTH)
            self.setCursor(Qt.SizeHorCursor)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
            self.edges |= Qt.RightEdge if side == 'right' else Qt.LeftEdge
        elif side in ('top-right', 'bottom-left'):
            self.setCursor(Qt.SizeBDiagCursor)
            self.setFixedSize(self.WIDTH, self.WIDTH)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            if side == 'top-right':
                self.edges |= Qt.TopEdge
                self.edges |= Qt.RightEdge
            else:
                self.edges |= Qt.BottomEdge
                self.edges |= Qt.LeftEdge
        else:
            self.setCursor(Qt.SizeFDiagCursor)
            self.setFixedSize(self.WIDTH, self.WIDTH)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            if side == 'top-left':
                self.edges |= Qt.TopEdge
                self.edges |= Qt.LeftEdge
            else:
                self.edges |= Qt.BottomEdge
                self.edges |= Qt.RightEdge
        self.cursor_ = self.cursor()

    def mousePressEvent(self, event):
        resize_window(self.window(), event.globalPos(), self.edges)
        return super().mousePressEvent(event)

