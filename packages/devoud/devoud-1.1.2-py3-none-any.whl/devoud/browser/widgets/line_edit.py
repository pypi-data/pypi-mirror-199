from PySide6.QtWidgets import QLineEdit

from devoud.browser.widgets.context_menu import BrowserContextMenu


class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event):
        menu = BrowserContextMenu(self.window())

        menu.addAction('Копировать', self.copy)
        menu.addAction('Вырезать', self.cut)
        menu.addAction('Вставить', self.paste)
        menu.addAction('Выделить всё', self.selectAll)
        menu.addSeparator()
        menu.addAction('Отменить', self.undo)
        menu.addAction('Повторить', self.redo)

        menu.popup(event.globalPos())
