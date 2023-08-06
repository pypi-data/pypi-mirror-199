from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget


class EmbeddedView(QWidget):

    def __init__(self, abstract_page, url=None, *args):
        super().__init__(abstract_page)
        print(f'[Страница]: Загрузка встроенной страницы ({url})')
        self.setObjectName('embedded_view')
        self.window = abstract_page.window
        self._url = None
        self._title = None
        self._icon = None
        self.embedded = True
        self.abstract_page = abstract_page

        self.abstract_page.view = self
        self.abstract_page.is_protected = 'devoud'
        self.window.address_panel.update_ssl_button()
        self.icon = QIcon('icons:devoud.svg')

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        self.abstract_page.url = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.abstract_page.title = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.abstract_page.icon = value

    def load(self, url):
        self.abstract_page.load(url)

    def stop(self):
        ...

    def reload(self):
        self.abstract_page.reload()

    def forward(self):
        self.abstract_page.forward()

    def back(self):
        self.abstract_page.back()

    def can_back(self):
        return False

    def can_forward(self):
        return False

    def is_loading(self):
        return False

    def mousePressEvent(self, event):
        if event.button() == Qt.BackButton:
            self.abstract_page.back()
        elif event.button() == Qt.ForwardButton:
            self.abstract_page.forward()
