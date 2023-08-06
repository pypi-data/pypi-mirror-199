from PySide6 import QtNetwork
from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import Qt
from PySide6.QtWebEngineCore import QWebEngineFullScreenRequest
from PySide6.QtWidgets import QWidget, QGridLayout, QProgressBar, QSplitter

from devoud.browser.page import url_type, redirects, get_view
from devoud.browser.page.web.view import BrowserWebView


class AbstractPage(QWidget):
    def __init__(self, tab_widget, url=None, title=None):
        super().__init__(tab_widget)
        self.setObjectName('abstract_page')
        self.window = self.window()
        self.tab_widget = tab_widget
        self.FS = self.window.FS
        self.settings = self.window.settings
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self._url = None
        self._title = None
        self._icon = None
        self.is_protected = None

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.layout().addWidget(self.progress_bar, 0, 0)

        self.view_spliter = QSplitter(Qt.Vertical)
        self.layout().addWidget(self.view_spliter, 1, 0)
        self.popup_link = None

        self.history = self.PageHistory(self)

        self.view = None
        self.url = url
        self.title = title
        self.icon = None

        self.network_manager = QtNetwork.QNetworkAccessManager()
        self.network_manager.finished.connect(self.reply_handle)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url_):
        if isinstance(url_, QUrl):
            url_ = url_.toString()
        self._url = url_
        if self.view:
            self.window.history.add(self.data())
            if self.view.can_back():
                del self.history[self.history.pos + 1:]
            try:
                self.history[self.history.pos] = url_
            except IndexError:
                self.history.set_enabled(True)
                self.history.append(url_)
                self.history[self.history.pos] = url_
            self.history.set_enabled(True)

        if self.tab_widget.currentWidget() == self:
            self.window.address_line_edit.update_text(url_)
            self.window.address_panel.update_bookmark_button()
            self.window.address_panel.update_navigation_buttons()
            self.window.address_panel.update_ssl_button()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title_):
        if title_ is None:
            title_ = 'Vasily ate cheese'
        self._title = title_
        index = self.tab_widget.indexOf(self)
        self.tab_widget.setTabText(index, title_)
        self.tab_widget.setTabToolTip(index, title_)
        if self.tab_widget.currentIndex() == index:
            self.window.set_title(title_, self.icon)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, icon_):
        if icon_:
            self._icon = icon_
            index = self.tab_widget.indexOf(self)
            self.tab_widget.setTabIcon(index, icon_)
            if self.tab_widget.currentIndex() == index:
                self.window.set_title(self.title, icon_)

    def deleteLater(self) -> None:
        for widget in self.children():
            widget.deleteLater()
        if self.view is not None:
            self.view.deleteLater()
        super().deleteLater()

    def data(self) -> dict:
        return {'url': self.url,
                'title': self.title,
                'type': url_type(self.url)}

    def load(self, url):
        url = QUrl.fromUserInput(url)
        if url.scheme() == 'http':
            url.setScheme('https')
        url = url.toString()
        url = redirects.get(url, url)  # если редирект не найден, то значение остается
        if isinstance(self.view, BrowserWebView) and url_type(url) is BrowserWebView:
            self.view.load(url)
        else:
            if self.view is not None:
                self.view.deleteLater()
            self.history.append(url)
            self.view = get_view(url)(self, url)
            self.view_spliter.addWidget(self.view)
        self.window.address_panel.update_ssl_button()

    def stop(self):
        self.view.stop()

    def reload(self):
        self.history.set_enabled(False)
        self.load(self.url)

    def back(self):
        self.history.back()

    def forward(self):
        self.history.forward()

    def can_back(self):
        return self.history.can_back()

    def can_forward(self):
        return self.history.can_forward()

    def is_loading(self):
        return False if self.view is None else self.view.is_loading()

    @Slot(QtNetwork.QNetworkReply)
    def reply_handle(self, reply: QtNetwork.QNetworkReply):
        if reply.error() == QtNetwork.QNetworkReply.NetworkError.SslHandshakeFailedError:
            self.is_protected = False
        else:
            self.is_protected = True
        self.window.address_panel.update_ssl_button()

    @Slot()
    def load_started_handler(self):
        self.is_protected = None
        if self.isVisible():
            self.window.address_panel.show_update_button(False)
        print(f"[Страница]: Начата загрузка страницы ({self.url})")

    @Slot(int)
    def load_progress_handler(self, progress):
        if self.isVisible():
            self.window.address_panel.show_update_button(False)
        self.progress_bar.setValue(progress)
        print(f"[Страница]: {progress}% ({self.url})")

    @Slot()
    def load_finished_handler(self):
        self.network_manager.get(QtNetwork.QNetworkRequest(QUrl(self.url)))
        if self.isVisible():
            self.window.address_panel.show_update_button(True)
        self.progress_bar.setValue(0)
        print(f"[Страница]: Страница загружена ({self.url})")

    @Slot(QWebEngineFullScreenRequest)
    def FullscreenRequest(self, request_=None):
        if request_ is not None:
            request_.accept()
            request_.toggleOn()
        if self.view.isFullScreen():
            self.view.setParent(self.view_spliter)
            self.window.show()
            self.view.showNormal()
        else:
            self.window.hide()
            self.view.setParent(None)
            self.view.showFullScreen()

    class PageHistory(list):
        """История перемещений по странице"""

        def __init__(self, abstract_page):
            super().__init__()
            self.abstract_page: AbstractPage = abstract_page
            self.pos = -1
            self._enabled = True

        def set_enabled(self, state: bool):
            self._enabled = state

        def is_enable(self) -> bool:
            return self._enabled

        def append(self, url) -> None:
            if self.is_enable():
                self.pos += 1
                super().append(url)

        def back(self):
            if self.can_back():
                self.set_enabled(False)
                if self.abstract_page.view.can_back():
                    self.abstract_page.view.back()
                else:
                    self.pos -= 1
                    self.abstract_page.load(self[self.pos])

        def forward(self):
            if self.can_forward():
                self.set_enabled(False)
                if self.abstract_page.view.can_forward():
                    self.abstract_page.view.forward()
                else:
                    self.pos += 1
                    self.abstract_page.load(self[self.pos])

        def can_back(self):
            return self.abstract_page.view.can_back() or self.pos > 0

        def can_forward(self):
            return self.abstract_page.view.can_forward() or self.pos != len(self) - 1
