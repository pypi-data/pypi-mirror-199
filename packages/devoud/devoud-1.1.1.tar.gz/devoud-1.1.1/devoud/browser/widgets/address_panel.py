from PySide6.QtCore import QSize, QTimer, Slot, QUrl
from PySide6.QtGui import QIcon, QCursor, Qt, QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame, QComboBox, QPushButton

from devoud.browser.page.web import search_engines
from devoud.browser.page import is_url, redirects
from devoud.browser.widgets.context_menu import BrowserContextMenu
from devoud.browser.widgets.line_edit import LineEdit


class AddressPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.FS = self.window().FS
        self.settings = self.window().settings
        self.tab_widget = self.window().tab_widget
        self.setObjectName("address_panel")
        self.setMinimumSize(QSize(550, 45))
        self.setMaximumSize(QSize(16777215, 45))
        self.setLayout(QHBoxLayout())

        # кнопки на панели
        self.add_tab_button = self.PanelButton(self, 'custom:add.svg', self.tab_widget.create_tab)
        self.add_tab_button.setObjectName('add_tab_button_panel')
        self.add_tab_button.hide()
        self.back_button = self.PanelButton(self, 'custom:arrow_left.svg', self.window().back_page)
        self.back_button.setObjectName('back_button')
        self.back_button.setToolTip('На предыдущую страницу (Alt+Влево)')
        self.forward_button = self.PanelButton(self, 'custom:arrow_right.svg', self.window().forward_page)
        self.forward_button.setObjectName('forward_button')
        self.forward_button.setToolTip('На следующую страницу (Alt+Вправо)')
        self.stop_load_button = self.PanelButton(self, 'custom:close(address_panel).svg', self.window().stop_load_page)
        self.stop_load_button.setObjectName('stop_load_button')
        self.stop_load_button.hide()
        self.update_button = self.PanelButton(self, 'custom:update.svg', self.window().update_page)
        self.update_button.setObjectName('update_button')
        self.home_button = self.PanelButton(self, 'custom:home.svg',
                                            lambda: self.window().load_home_page(new_tab=False))
        self.home_button.setObjectName('home_button')

        # адресная строка
        self.address_line_frame = QFrame(self)
        self.address_line_frame.setObjectName("address_line_frame")
        self.address_line_frame.setFixedHeight(29)
        self.address_line_frame.setLayout(QHBoxLayout())
        self.address_line_frame.layout().setSpacing(0)
        self.address_line_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.address_line_frame)

        self.search_box = QComboBox(self)
        [self.search_box.addItem(QIcon(search_engines[title]['icon']), title) for title in search_engines.keys()]
        self.search_box.setObjectName("search_box")
        self.search_box.setFixedSize(QSize(120, 29))
        self.address_line_frame.layout().addWidget(self.search_box)
        self.search_box.setCurrentText(self.settings.get('searchEngine'))

        self.ssl_button = self.PanelButton(self)
        self.ssl_button.setObjectName('ssl_button')
        self.address_line_frame.layout().addWidget(self.ssl_button)

        self.address_line_edit = self.AddressLineEdit(self)
        self.address_line_frame.layout().addWidget(self.address_line_edit)

        self.bookmark_button = self.PanelButton(self.address_line_frame,
                                                'custom:bookmark_empty.svg',
                                                lambda: self.window().bookmarks.add(
                                                    self.window().page().data()))
        self.bookmark_button.setObjectName('bookmark_button')
        self.window().bookmarks.bookmark_add.connect(self.update_bookmark_button)
        self.window().bookmarks.bookmark_remove.connect(self.update_bookmark_button)

        # контекстное меню для вызова панели управления
        self.menu_button = self.PanelButton(self, 'custom:options.svg')
        self.menu_button.setObjectName('menu_button')
        self.options_menu = BrowserContextMenu(self)
        self.options_menu.addAction('Настройки', lambda: self.tab_widget.create_tab(url='devoud://control.py#settings'))
        self.options_menu.addAction('История', lambda: self.tab_widget.create_tab(url='devoud://control.py#history'))
        self.options_menu.addAction('Закладки', lambda: self.tab_widget.create_tab(url='devoud://control.py#bookmarks'))
        self.options_menu.addAction('Загрузки', lambda: self.tab_widget.create_tab(url='devoud://control.py#downloads'))
        self.options_menu.addAction('Новое окно', lambda: self.window().create_new_window(private=False))
        self.options_menu.addAction('Приватное окно', lambda: self.window().create_new_window(private=True))
        self.menu_button.setMenu(self.options_menu)

    def show_update_button(self, show):
        if show:
            self.update_button.show()
            self.stop_load_button.hide()
        else:
            self.update_button.hide()
            self.stop_load_button.show()

    @Slot()
    def update_navigation_buttons(self):
        self.back_button.setEnabled(self.window().page().can_back())
        self.forward_button.setEnabled(self.window().page().can_forward())

    def update_ssl_button(self):
        is_protected = self.window().page().is_protected
        if is_protected == 'devoud':
            self.ssl_button.setIcon(QIcon('custom:chip(address_panel).svg'))
            self.ssl_button.setToolTip('Встроенная страница')
        elif QUrl(self.window().page().url).scheme() == 'file':
            self.ssl_button.setIcon(QIcon('custom:file(address_panel).svg'))
            self.ssl_button.setToolTip('Страница хранится на вашем компьютере')
        elif is_protected is True:
            self.ssl_button.setIcon(QIcon('custom:lock(address_panel).svg'))
            self.ssl_button.setToolTip('Защищенное соединение')
        elif is_protected is False:
            self.ssl_button.setIcon(QIcon('custom:no_encryption(address_panel).svg'))
            self.ssl_button.setToolTip('Соединение не защищено')
        else:
            self.ssl_button.setIcon(QIcon('custom:more(address_panel).svg'))
            self.ssl_button.setToolTip('Идёт проверка защищенности')

    @Slot()
    def update_bookmark_button(self):
        state = self.window().bookmarks.url_exist(self.window().page().url)
        self.bookmark_button.setIcon(QIcon(f"custom:{'bookmark' if state else 'bookmark_empty'}.svg"))

    class AddressLineEdit(LineEdit):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setObjectName("address_line_edit")
            self.setPlaceholderText('Поиск или ссылка')
            self.setFixedHeight(29)
            self.setCursor(QCursor(Qt.IBeamCursor))
            self.setClearButtonEnabled(True)
            self.returnPressed.connect(self.load_from_line)
            self.text_ = None
            QShortcut(QKeySequence("Esc"), self).activated.connect(self.clearFocus)

        def update_text(self, text):
            self.text_ = text
            if not self.hasFocus():
                self.setText(text)
                self.setCursorPosition(0)

        def load_from_line(self):
            url = self.text()
            if not is_url(url) and url not in redirects:
                self.window().search(url)
            else:
                self.window().load(url)
            self.clearFocus()

        def focusInEvent(self, event):
            QTimer.singleShot(0, self.selectAll)
            super().focusInEvent(event)

    class PanelButton(QPushButton):
        def __init__(self, parent=None, icon=None, command=None):
            super().__init__(parent)
            self.setObjectName("address_panel_button")
            self.setFixedSize(QSize(30, 29))
            self.setCursor(QCursor(Qt.PointingHandCursor))

            if command is not None:
                self.clicked.connect(command)

            if icon is not None:
                self.icon = icon
                self.setIcon(QIcon(icon))
                self.setIconSize(QSize(25, 19))

            if parent is not None:
                parent.layout().addWidget(self)
