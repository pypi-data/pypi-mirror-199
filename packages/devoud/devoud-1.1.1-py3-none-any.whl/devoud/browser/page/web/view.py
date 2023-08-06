from PySide6 import QtCore
from PySide6.QtCore import Slot, QUrl
from PySide6.QtGui import QKeySequence, QShortcut, Qt
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineContextMenuRequest, QWebEngineCertificateError
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox

from devoud.browser.downloads import DownloadMethod
from devoud.browser.page import is_url
from devoud.browser.widgets.context_menu import BrowserContextMenu


class BrowserWebViewPage(QWebEnginePage):
    def __init__(self, profile, view):
        super().__init__(profile, view)
        self.abstract_page = view.abstract_page
        self.certificateError.connect(self.certificate_error)

    @Slot(QWebEngineCertificateError)
    def certificate_error(self, error: QWebEngineCertificateError):
        self.abstract_page.is_protected = False
        self.abstract_page.window.address_panel.update_ssl_button()
        if QMessageBox.question(self.abstract_page, 'Небезопасная страница',
                                f'{error.description()} Всё равно зайти?') == QMessageBox.Yes:
            error.acceptCertificate()
        else:
            error.rejectCertificate()

    def acceptNavigationRequest(self, url, type_, isMainFrame):
        if type_ == QWebEnginePage.NavigationTypeBackForward:
            # тоска
            ...

        if type_ == QWebEnginePage.NavigationTypeRedirect:
            print(f'[Страница]: Редирект ({url.toString()})')

        return super().acceptNavigationRequest(url, type_, isMainFrame)


class BrowserWebView(QWebEngineView):
    def __init__(self, abstract_page, url, *args):
        super().__init__(abstract_page)
        self.abstract_page = abstract_page
        self.window = abstract_page.window
        self.FS = abstract_page.window.FS
        self.profile = abstract_page.window.profile
        self.setAutoFillBackground(True)
        self.embedded = False
        self.title = abstract_page.url
        self.dev_view = None
        self.popup_link = None

        self.urlChanged.connect(self.url_changed)
        self.titleChanged.connect(self.title_changed)
        self.iconChanged.connect(self.icon_changed)
        self.loadStarted.connect(self.abstract_page.load_started_handler)
        self.loadProgress.connect(self.abstract_page.load_progress_handler)
        self.loadFinished.connect(self.abstract_page.load_finished_handler)

        self.setPage(BrowserWebViewPage(self.profile, self))
        self.page().fullScreenRequested.connect(self.abstract_page.FullscreenRequest)

        self.popup_link = self.PopupLink(self.abstract_page)
        self.page().linkHovered.connect(self.popup_link.show_link)

        QShortcut(QKeySequence("F11"), self).activated.connect(self.abstract_page.FullscreenRequest)
        QShortcut(QKeySequence("F12"), self).activated.connect(self.toggle_dev_tools)

        self.load(url)
        self.focusProxy().installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == Qt.BackButton:
                self.abstract_page.back()
            if event.button() == Qt.ForwardButton:
                self.abstract_page.forward()
        return super().eventFilter(source, event)

    def deleteLater(self) -> None:
        self.page().deleteLater()
        self.popup_link.deleteLater()
        super().deleteLater()

    @Slot(QUrl)
    def url_changed(self, url):
        if url.toString():
            self.abstract_page.url = url
            if url.scheme() == 'file':
                # FIXME: Локальные файлы открываются только после перезагрузки
                self.abstract_page.reload()

    @Slot(str)
    def title_changed(self, title):
        if title:
            self.abstract_page.title = title

    def icon_changed(self, icon):
        self.abstract_page.icon = icon

    def can_back(self):
        return self.page().history().canGoBack()

    def can_forward(self):
        return self.page().history().canGoForward()

    def is_loading(self):
        return self.page().isLoading()

    def inspect_page(self):
        if self.dev_view is None:
            self.dev_view = QWebEngineView()
            self.dev_view.page().windowCloseRequested.connect(self.dev_view.hide)
            self.abstract_page.view_spliter.addWidget(self.dev_view)
            self.abstract_page.view_spliter.setSizes([200, 100])
            self.page().setDevToolsPage(self.dev_view.page())
        if self.dev_view.isHidden():
            self.dev_view.show()
        self.page().triggerAction(QWebEnginePage.InspectElement)

    def toggle_dev_tools(self):
        if self.dev_view is None:
            self.dev_view = QWebEngineView()
            self.abstract_page.view_spliter.addWidget(self.dev_view)
            self.abstract_page.view_spliter.setSizes([200, 100])
            self.page().setDevToolsPage(self.dev_view.page())
            self.dev_view.page().windowCloseRequested.connect(self.dev_view.hide)
        elif self.dev_view.isVisible():
            self.dev_view.hide()
        else:
            self.dev_view.show()

    def save_image_as(self):
        DownloadMethod.Method = DownloadMethod.SaveAs
        self.triggerPageAction(QWebEnginePage.DownloadMediaToDisk)

    def createWindow(self, type_):
        if type_ == QWebEnginePage.WebBrowserTab:
            # запрос на новую вкладку
            return self.window.tab_widget.create_tab(url=self.page().url(), title=self.page().title(), end=False)

        if type_ == QWebEnginePage.WebBrowserBackgroundTab:
            return self.window.tab_widget.create_tab(url=self.page().url(), title=self.page().title(), end=False, switch=False)

    def contextMenuEvent(self, event):
        menu = BrowserContextMenu(self)
        page = self.page()
        page_request = self.lastContextMenuRequest()
        edit_flags = page_request.editFlags()
        media_flags = page_request.mediaFlags()
        link = None

        if media_flags:
            media_url = self.lastContextMenuRequest().mediaUrl().toString()
            menu.addAction('Копировать изображение',
                           lambda: page.triggerAction(QWebEnginePage.CopyImageToClipboard))
            menu.addAction('Копировать ссылку на изображение',
                           lambda: page.triggerAction(QWebEnginePage.CopyImageUrlToClipboard))
            menu.addAction('Сохранить изображение как', self.save_image_as)
            menu.addAction('Открыть в новой вкладке',
                           lambda: self.window.tab_widget.create_tab(url=media_url, switch=False, end=False))
        elif edit_flags:
            if is_url(page_request.linkUrl().toString()):
                link = page_request.linkUrl().toString()
            elif is_url(page_request.selectedText()):
                link = page_request.selectedText()
            if link:
                menu.addAction('Копировать ссылку', lambda: QApplication.clipboard().setText(link))
                menu.addAction('Открыть в новой вкладке',
                               lambda: self.window.tab_widget.create_tab(url=link, switch=False, end=False))
            if QWebEngineContextMenuRequest.CanCopy in edit_flags:
                menu.addAction('Копировать', lambda: page.triggerAction(QWebEnginePage.Copy))
            if QWebEngineContextMenuRequest.CanPaste in edit_flags:
                menu.addAction('Вставить', lambda: page.triggerAction(QWebEnginePage.Paste))
            if QWebEngineContextMenuRequest.CanCut in edit_flags:
                menu.addAction('Вырезать', lambda: page.triggerAction(QWebEnginePage.Cut))
            if QWebEngineContextMenuRequest.CanUndo in edit_flags:
                menu.addAction('Отменить', lambda: page.triggerAction(QWebEnginePage.Undo))
            if QWebEngineContextMenuRequest.CanRedo in edit_flags:
                menu.addAction('Повторить', lambda: page.triggerAction(QWebEnginePage.Redo))
            if QWebEngineContextMenuRequest.CanSelectAll in edit_flags:
                menu.addAction('Выделить всё', lambda: page.triggerAction(QWebEnginePage.SelectAll))
            if QWebEngineContextMenuRequest.CanCopy in edit_flags:
                menu.addSeparator()
                if not self.isFullScreen():
                    menu.addAction(f'Поиск в {self.window.settings.get("searchEngine")}',
                                   lambda: self.window.search(page.selectedText(), new_tab=True))
        menu.addSeparator()
        menu.addAction('Назад', self.abstract_page.back)
        menu.addAction('Вперед', self.abstract_page.forward)
        menu.addAction('Перезагрузить', lambda: page.triggerAction(QWebEnginePage.Reload))
        menu.addSeparator()
        if self.isFullScreen():
            menu.addAction('Выйти из полноэкранного режима', self.abstract_page.FullscreenRequest)
        else:
            menu.addAction('Инспектировать', self.inspect_page)
            menu.addAction('Исходный код', lambda: page.triggerAction(QWebEnginePage.ViewSource))
        menu.popup(event.globalPos())

    class PopupLink(QLabel):
        def __init__(self, parent):
            super().__init__(parent)
            self.setObjectName('popup_link')
            self.setMinimumWidth(0)
            self.setMaximumWidth(16777215)
            self.parent().layout().addWidget(self, 1, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
            self._left_align = True

        @Slot(str)
        def show_link(self, url):
            self.setText(url)
            self.setHidden(url == '')

        def enterEvent(self, event):
            if self._left_align:
                self.parent().layout().addWidget(self, 1, 0, 1, 2, Qt.AlignRight | Qt.AlignBottom)
                self._left_align = False
                self.setStyleSheet('border-top-right-radius: 0px; border-top-left-radius: 6px')
            else:
                self.parent().layout().addWidget(self, 1, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
                self._left_align = True
                self.setStyleSheet('border-top-right-radius: 6px; border-top-left-radius: 0px')
