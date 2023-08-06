from PySide6.QtCore import Signal, QSize, QUrl, Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QTabWidget, QPushButton, QAbstractButton, QTabBar

from devoud.browser.page.abstract_page import AbstractPage
from devoud.browser.widgets.context_menu import BrowserContextMenu


class BrowserTabWidget(QTabWidget):
    count_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName('tab_widget')
        self.maximum_tabs = 150
        self.setTabBar(self.TabBar(self))
        self.setTabsClosable(True)
        self.setElideMode(Qt.ElideRight)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.tab_changed)

        # кнопка создания новой вкладки
        self.add_tab_button = QPushButton(self)
        self.add_tab_button.setObjectName('add_tab_button')
        self.add_tab_button.setFixedSize(40, 40)
        self.add_tab_button.setIconSize(QSize(25, 19))
        self.add_tab_button.setToolTip('Создать новую вкладку (Ctrl + T)')
        self.add_tab_button.clicked.connect(self.create_tab)
        self.setCornerWidget(self.add_tab_button, Qt.Corner.TopLeftCorner)

        self.count_changed.connect(self.toggle_tab_bar)

    def toggle_tab_bar(self):
        if self.count() == 1:
            self.tabBar().hide()
            self.window().add_tab_button.show()
            self.window().address_panel.setFixedHeight(45)
            self.add_tab_button.hide()
        elif self.count() == 2:
            self.window().add_tab_button.hide()
            if self.window().settings.get('TabBarPosition') == 'Снизу':
                self.window().address_panel.setFixedHeight(45)
            else:
                self.window().address_panel.setFixedHeight(40)
            self.add_tab_button.show()
            self.tabBar().show()

    def set_tab_bar_position(self, position=None):
        if position is None:
            position = self.window().settings.get('TabBarPosition')
        if position == 'Сверху':
            self.setTabPosition(QTabWidget.North)
            self.add_tab_button.setStyleSheet('#add_tab_button {margin-bottom: 8px;}')
            self.window().address_panel.setFixedHeight(40)
        else:
            self.window().address_panel.setFixedHeight(45)
            self.setTabPosition(QTabWidget.South)
            self.add_tab_button.setStyleSheet('#add_tab_button {margin-top: 8px;}')

    def create_tab(self, **kwargs):
        page = kwargs.get('page', None)
        url = kwargs.get('url', None)
        title = kwargs.get('title', url)
        end = kwargs.get('end', True)
        load = kwargs.get('load', True)
        switch = kwargs.get('switch', True)
        index = kwargs.get('index', False)

        if url is None:
            url = self.window().settings.get('newPage')['site']
            title = 'Новая вкладка'

        if isinstance(url, QUrl):
            url = url.toString()

        if not page:
            page = AbstractPage(self, url=url, title=title)
        if not index:
            index = self.count() if end else self.currentIndex() + 1
        print(f'[Вкладки]: Создается новая вкладка ({page.url})')
        self.insertTab(index, page, page.title)
        if load:
            page.load(page.url)
        if switch:
            self.setCurrentIndex(index)

        self.setTabToolTip(index, page.title)
        self.window().session.add_page(page)
        self.tabBar().findChild(QAbstractButton).setToolTip('Закрыть вкладку (Ctrl + W)')
        self.count_changed.emit()
        return page.view  # для запросов на новую вкладку

    @Slot()
    def tab_changed(self):
        page = self.current()
        if page:
            if page.view is None:
                page.reload()
            self.window().address_line_edit.update_text(page.url)
            self.window().set_title(page.title, page.icon)
            self.window().address_panel.show_update_button(not page.is_loading())
            self.window().address_panel.update_bookmark_button()
            self.window().address_panel.update_navigation_buttons()
            self.window().address_panel.update_ssl_button()

    @Slot(int)
    def close_tab(self, index):
        page = self.widget(index)
        if self.count() <= 1:  # если одна вкладка, то открывать сайт с заставкой
            page.load(self.window().settings.get('newPage')['site'])
            return
        print(f'[Вкладки]: Закрывается вкладка ({page.url})')
        page.deleteLater()
        self.window().session.remove_page(page)
        self.removeTab(index)
        self.count_changed.emit()

    def current(self) -> AbstractPage:
        return self.currentWidget()

    class TabBar(QTabBar):

        def __init__(self, parent):
            super().__init__(parent)
            self.setMovable(True)

        def open_tab_in_new_window(self, index):
            url = self.parent().widget(index).url
            self.parent().close_tab(index)
            self.window().create_new_window(url=url)

        def mousePressEvent(self, event):
            tab = self.tabAt(event.position().toPoint())
            if event.button() == Qt.LeftButton:
                super().mousePressEvent(event)
            elif event.button() == Qt.RightButton:
                menu = BrowserContextMenu(self)
                menu.addAction('Открыть в новом окне', lambda: self.open_tab_in_new_window(tab))
                menu.addAction('Дублировать вкладку', lambda: self.parent().create_tab(url=self.parent().widget(tab).url))
                menu.addAction('Закрыть вкладку', lambda: self.parent().close_tab(tab))
                menu.popup(event.globalPos())
            elif event.button() == Qt.MiddleButton:
                self.parent().close_tab(tab)
