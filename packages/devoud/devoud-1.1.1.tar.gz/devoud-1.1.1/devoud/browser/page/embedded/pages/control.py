import json
import os
from platform import system

from PySide6.QtCore import QSize, Slot, QTimer
from PySide6.QtGui import QPixmap, QIcon, Qt
from PySide6.QtWidgets import QHBoxLayout, QStackedWidget, QLabel, QPushButton, QComboBox, QSizePolicy, QSpacerItem, \
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QScrollArea, QProgressBar, QCheckBox, QTreeWidgetItem, \
    QMessageBox, QHeaderView, QFrame

from devoud import __name__, __version__, __license__, __author__, IS_PYINSTALLER
from devoud import rpath, restart
from devoud.browser.page.embedded.view import EmbeddedView
from devoud.browser.page.web import search_engines
from devoud.browser.utils import human_bytes, get_folder_size, open_in_file_manager
from devoud.browser.utils.shortcuts import make_shortcut
from devoud.browser.utils.versions import last_version
from devoud.browser.widgets.container import ContainerWidget
from devoud.browser.widgets.context_menu import BrowserContextMenu
from devoud.browser.widgets.line_edit import LineEdit
from devoud.browser.widgets.tree_widget import TreeWidget


class ControlPage(EmbeddedView):
    section_tags = {'devoud://control.py#settings': 0,
                    'devoud://control.py#history': 1,
                    'devoud://control.py#bookmarks': 2,
                    'devoud://control.py#downloads': 3}

    def __init__(self, abstract_page, *args):
        super().__init__(abstract_page, *args)
        self.title = 'Панель управления'
        self.FS = abstract_page.FS
        self.settings = abstract_page.settings
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 5)
        self.main_layout.setSpacing(0)

        self.sections_panel = self.SectionsPanel(self)

        self.stacked_widget = QStackedWidget(self)  # всё что справа от панели вкладок
        self.stacked_widget.setObjectName('stacked_widget')
        self.sections_panel.setCurrentRow(self.section_tags.get(self.abstract_page.url, 0))
        self.sections_panel.currentRowChanged.connect(self.section_changed)
        self.main_layout.addWidget(self.stacked_widget)

        self.settings_section = self.Section(self.stacked_widget, 'custom:settings.svg')
        self.history_section = self.Section(self.stacked_widget, 'custom:history.svg')
        self.bookmarks_section = self.Section(self.stacked_widget, 'custom:bookmark_empty(sections).svg')
        self.download_section = self.Section(self.stacked_widget, 'custom:downloads.svg')

        # Виджет "О программе"
        self.about_widget = ContainerWidget(self, 'О программе')
        self.settings_section.add_widget(self.about_widget)
        self.browser_icon = QLabel(self.about_widget)
        self.browser_icon.setPixmap(QPixmap('icons:devoud.svg'))
        self.browser_icon.mousePressEvent = lambda e: self.browser_icon.setPixmap(QPixmap('icons:warning.svg'))
        self.browser_icon.setFixedSize(QSize(85, 85))
        self.browser_icon.setScaledContents(True)
        self.about_widget.content_layout.addWidget(self.browser_icon, 0, 0)
        self.about_widget.content_layout.addWidget(QLabel(self.about_widget,
                                                          text=f'{__name__} {__version__}'
                                                               f'{" (Pyinstaller)" if IS_PYINSTALLER else ""} для {system()}'
                                                               f'\nРазработал {__author__}\nс '
                                                               f'использованием PySide6 под лицензией {__license__}'),
                                                   0, 1)
        if system() != 'Windows' and not IS_PYINSTALLER:
            # FIXME: Windows не дает перезаписывать используемые файлы
            self.update_program_button = QPushButton(self.about_widget, text='Проверить обновления')
            self.update_program_button.setFixedSize(165, 22)
            self.update_program_button.setObjectName('container_title_button')
            self.update_program_button.clicked.connect(self.update_program)
            self.about_widget.title_layout.addWidget(self.update_program_button)

        if not IS_PYINSTALLER:
            self.create_shortcut_button = QPushButton(self.about_widget, text='Создать ярлык')
            self.create_shortcut_button.setFixedSize(110, 22)
            self.create_shortcut_button.setObjectName('container_title_button')
            self.create_shortcut_button.clicked.connect(self.create_shortcut)
            self.about_widget.title_layout.addWidget(self.create_shortcut_button)

        self.project_site_button = QPushButton(self.about_widget, text='Страница проекта')
        self.project_site_button.setFixedSize(130, 22)
        self.project_site_button.setObjectName('container_title_button')
        self.project_site_button.clicked.connect(
            lambda: self.window.tab_widget.create_tab(url='https://codeberg.org/OneEyedDancer/Devoud', end=False))
        self.about_widget.title_layout.addWidget(self.project_site_button)

        # Виджет настроек
        self.settings_widget = ContainerWidget(self, 'Настройки')
        self.user_dir_button = QPushButton(self.settings_widget, icon=QIcon('custom:folder.svg'))
        self.user_dir_button.setFixedSize(30, 22)
        self.user_dir_button.setObjectName('container_title_button')
        self.user_dir_button.setToolTip('Открыть каталог с пользовательскими данными')
        self.user_dir_button.clicked.connect(lambda: open_in_file_manager(self.window.FS.user_dir()))
        self.settings_widget.title_layout.addWidget(self.user_dir_button)
        self.settings_section.add_widget(self.settings_widget)

        # Кнопка перезапуска
        self.restart_button = QPushButton(self.settings_widget, icon=QIcon('custom:restart.svg'), text='Перезапустить')
        self.restart_button.setFixedSize(140, 22)
        self.restart_button.setObjectName('container_title_button')
        self.restart_button.setToolTip('Для применения настроек требуется перезапуск')
        self.restart_button.setHidden(True)
        self.restart_button.clicked.connect(self.window.restart)
        self.settings_widget.title_layout.addWidget(self.restart_button)

        # Чекбоксы
        self.history_checkbox = self.SettingsCheckBox(parent=self,
                                                      text='Сохранять историю',
                                                      option='saveHistory',
                                                      command=self.history_checkbox_command,
                                                      command_exec='before',
                                                      tooltip='При выключении удаляет историю',
                                                      block=self.window.private)
        self.settings_widget.content_layout.addWidget(self.history_checkbox, 0, 0)
        self.restore_tabs_checkbox = self.SettingsCheckBox(parent=self,
                                                           text='Восстанавливать вкладки',
                                                           option='restoreSession',
                                                           tooltip='Восстанавливает последнюю сессию браузера',
                                                           block=self.window.private)
        self.settings_widget.content_layout.addWidget(self.restore_tabs_checkbox, 1, 0)
        self.adblock_checkbox = self.SettingsCheckBox(parent=self,
                                                      text='Блокировщик рекламы',
                                                      option='adblock',
                                                      restart=True)
        self.settings_widget.content_layout.addWidget(self.adblock_checkbox, 2, 0)
        self.cookie_checkbox = self.SettingsCheckBox(parent=self,
                                                     text='Хранить Cookie',
                                                     option='cookies',
                                                     tooltip='При отключении Cookie-файлы больше не будут храниться на диске',
                                                     command=self.cookie_checkbox_command,
                                                     command_exec='before',
                                                     restart=True,
                                                     block=self.window.private)
        self.settings_widget.content_layout.addWidget(self.cookie_checkbox, 3, 0)
        self.javascript_checkbox = self.SettingsCheckBox(parent=self,
                                                         text='JavaScript',
                                                         option='javascript',
                                                         restart=True)
        self.settings_widget.content_layout.addWidget(self.javascript_checkbox, 4, 0)
        self.systemframe_checkbox = self.SettingsCheckBox(parent=self,
                                                          text='Системная рамка окна',
                                                          option='systemWindowFrame',
                                                          restart=True)
        self.settings_widget.content_layout.addWidget(self.systemframe_checkbox, 5, 0)
        self.smooth_scroll_checkbox = self.SettingsCheckBox(parent=self,
                                                            text='Плавная прокрутка страниц',
                                                            option='smoothScroll',
                                                            restart=True)
        self.settings_widget.content_layout.addWidget(self.smooth_scroll_checkbox, 6, 0)

        self.home_frame = QFrame(self)
        self.home_frame.setLayout(QHBoxLayout())
        self.home_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.home_lineedit = LineEdit(self)
        self.home_lineedit.setFixedSize(QSize(215, 24))
        self.home_lineedit.setFocusPolicy(Qt.ClickFocus)
        self.home_lineedit.textEdited.connect(lambda: self.settings.set('homePage', self.home_lineedit.text()))
        self.home_lineedit.setText(self.settings.get('homePage'))
        self.home_frame.layout().addWidget(self.home_lineedit)
        self.home_frame.layout().addWidget(QLabel(self.settings_widget, text='Домашняя страница'))
        self.settings_widget.content_layout.addWidget(self.home_frame, 7, 0)

        self.new_page_frame = QFrame(self)
        self.new_page_frame.setLayout(QHBoxLayout())
        self.new_page_box = QComboBox(self.settings_widget)
        self.new_page_frame.layout().setContentsMargins(0, 0, 0, 0)
        [self.new_page_box.addItem(title) for title in ['Заставка с часами', 'Поисковик', 'Домашняя страница']]
        self.new_page_box.setFixedSize(QSize(215, 24))
        self.new_page_box.setFocusPolicy(Qt.ClickFocus)
        self.new_page_box.setCurrentText(self.settings.get('newPage')['title'])
        self.new_page_box.currentIndexChanged.connect(self.change_new_page)
        self.new_page_frame.layout().addWidget(self.new_page_box)
        self.new_page_frame.layout().addWidget(QLabel("Новая страница"))
        self.settings_widget.content_layout.addWidget(self.new_page_frame, 8, 0)

        self.search_frame = QFrame(self)
        self.search_frame.setLayout(QHBoxLayout())
        self.search_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.search_box = QComboBox(self.settings_widget)
        [self.search_box.addItem(QIcon(search_engines[title]['icon']), title) for title in search_engines.keys()]
        self.search_box.setFixedSize(QSize(215, 24))
        self.search_box.setFocusPolicy(Qt.ClickFocus)
        self.search_box.setCurrentText(self.settings.get('searchEngine'))
        self.search_box.currentIndexChanged.connect(self.change_default_search)
        self.search_frame.layout().addWidget(self.search_box)
        self.search_frame.layout().addWidget(QLabel('Поисковая система по умолчанию'))
        self.settings_widget.content_layout.addWidget(self.search_frame, 9, 0)

        self.tab_bar_position_frame = QFrame(self)
        self.tab_bar_position_frame.setLayout(QHBoxLayout())
        self.tab_bar_position_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.tab_bar_position_box = QComboBox(self.settings_widget)
        self.tab_bar_position_box.addItem('Снизу')
        self.tab_bar_position_box.addItem('Сверху')
        self.tab_bar_position_box.setCurrentText(self.settings.get('TabBarPosition'))
        self.tab_bar_position_box.setFixedSize(QSize(215, 24))
        self.tab_bar_position_box.setFocusPolicy(Qt.ClickFocus)
        self.tab_bar_position_frame.layout().addWidget(self.tab_bar_position_box)
        self.tab_bar_position_frame.layout().addWidget(QLabel("Положение панели вкладок"))
        self.settings_widget.content_layout.addWidget(self.tab_bar_position_frame, 10, 0)
        self.tab_bar_position_box.currentIndexChanged.connect(
            lambda: self.change_tab_bar_position(self.tab_bar_position_box.currentText()))

        self.cache_frame = QFrame(self)
        self.cache_frame.setLayout(QHBoxLayout())
        self.cache_label = QLabel(f'Кеш: {human_bytes(get_folder_size(f"{self.FS.user_dir()}/cache"))}')
        self.clear_cache_button = QPushButton('Очистить')
        self.clear_cache_button.clicked.connect(self.clear_cache)
        self.clear_cache_button.setFixedWidth(100)
        self.cache_frame.layout().addWidget(self.cache_label)
        self.cache_frame.layout().addWidget(self.clear_cache_button)
        self.settings_widget.content_layout.addWidget(self.cache_frame, 11, 0, alignment=Qt.AlignLeft)

        # Виджет тем
        self.themes_widget = ContainerWidget(self, 'Темы')
        self.settings_section.add_widget(self.themes_widget)
        self.themes_buttons_list = []
        self.create_themes_buttons()
        self.themes_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.themes_widget.content_layout.addItem(self.themes_spacer, 0, 5)

        # Settings section spacer
        self.settings_section.add_spacer(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # История
        self.history_widget = ContainerWidget(self, 'История')
        self.history_widget.content_layout.setContentsMargins(0, 0, 0, 5)
        self.history_section.add_widget(self.history_widget)
        self.history_list_widget = self.HistoryListWidget(self.history_widget)
        self.history_widget.content_layout.addWidget(self.history_list_widget)
        self.window.history.history_add.connect(self.history_list_widget.add)
        self.window.history.history_remove.connect(self.history_list_widget.remove)
        self.window.history.history_remove_all.connect(self.history_list_widget.clear)
        for item in self.window.history.get_all():
            self.history_list_widget.add(item)

        # Закладки
        self.bookmarks_widget = ContainerWidget(self, 'Закладки')
        self.bookmarks_widget.content_layout.setContentsMargins(0, 0, 0, 5)
        self.bookmarks_list_widget = self.BookmarksListWidget(self.bookmarks_widget)
        self.bookmarks_widget.content_layout.addWidget(self.bookmarks_list_widget)
        self.bookmarks_section.add_widget(self.bookmarks_widget)
        self.window.bookmarks.bookmark_add.connect(self.bookmarks_list_widget.add)
        self.window.bookmarks.bookmark_remove.connect(self.bookmarks_list_widget.remove)
        self.window.bookmarks.bookmark_remove_all.connect(self.bookmarks_list_widget.clear)
        for item in self.window.bookmarks.get_all():
            self.bookmarks_list_widget.add(item)

        # Загрузки
        self.download_widget = ContainerWidget(self, 'Загрузки')
        self.download_widget.content_layout.setContentsMargins(0, 0, 0, 5)
        self.download_list_widget = self.DownloadListWidget(self.download_widget)
        self.download_widget.content_layout.addWidget(self.download_list_widget)
        self.download_section.add_widget(self.download_widget)

        for item in self.window.downloads.get_all():
            self.download_list_widget.add(item)
        self.window.downloads.download_add.connect(self.download_list_widget.add)
        self.window.downloads.download_remove.connect(self.download_list_widget.remove)
        self.window.downloads.download_remove_all.connect(self.download_list_widget.clear)

        self.sections_panel.setCurrentRow(self.section_tags.get(self.abstract_page.url, 0))

    def deleteLater(self) -> None:
        self.window.bookmarks.bookmark_add.disconnect(self.bookmarks_list_widget.add)
        self.window.bookmarks.bookmark_remove.disconnect(self.bookmarks_list_widget.remove)
        self.window.bookmarks.bookmark_remove_all.disconnect(self.bookmarks_list_widget.clear)
        self.window.downloads.download_add.disconnect(self.download_list_widget.add)
        self.window.downloads.download_remove.disconnect(self.download_list_widget.remove)
        self.window.downloads.download_remove_all.disconnect(self.download_list_widget.clear)
        self.window.history.history_add.disconnect(self.history_list_widget.add)
        self.window.history.history_remove.disconnect(self.history_list_widget.remove)
        self.window.history.history_remove_all.disconnect(self.history_list_widget.clear)
        super().deleteLater()

    @Slot(int)
    def section_changed(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.abstract_page.url = {value: key for key, value in self.section_tags.items()}.get(index, 0)

    def create_themes_buttons(self):
        for path, dirs, files in os.walk(rpath("ui/themes")):
            for count, filename in enumerate(files):
                with open(f"{path}/{filename}", 'r') as theme_file:
                    data = json.load(theme_file)
                    btn = QPushButton(self)
                    btn.setFixedSize(20, 20)
                    btn.setObjectName(filename.rpartition('.')[0])
                    btn.setStyleSheet(f"""
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                            stop:0 {data['tab_widget']['select_bg']}, 
                            stop:1 {data['tab_widget']['bg']});
                            border-radius: 10px;
                            border: 0;""")
                    btn.clicked.connect(self.apply_theme)
                    self.themes_buttons_list.append(btn)
                    self.themes_widget.content_layout.addWidget(btn, 0, count)

        self.set_select_icon(self.settings.get('theme'))

    def set_select_icon(self, select_theme=None):
        if select_theme is None:
            select_theme = self.FS.default_settings['theme']
        for button in self.themes_buttons_list:
            if button.objectName() == select_theme:
                button.setIcon(QIcon('custom:select.svg'))
            else:
                button.setIcon(QIcon('custom:void.png'))

    def apply_theme(self):
        selected_theme = self.sender().objectName()
        self.settings.set('theme', selected_theme)
        self.window.change_style()
        self.set_select_icon(selected_theme)
        self.window.session.update_control_pages()
        print('[Стили]: Применена тема', selected_theme)

    def change_default_search(self):
        current = self.search_box.currentText()
        self.settings.set('searchEngine', current)
        self.window.address_panel.search_box.setCurrentText(self.settings.get('searchEngine'))
        if self.settings.get('newPage')['title'] == 'Поисковик':
            self.settings.set('newPage', {'title': 'Поисковик', 'site': search_engines[current]['site']})

    def change_new_page(self):
        new_page_dict = {'Заставка с часами': 'https://web.tabliss.io/',
                         'Поисковик': search_engines[self.settings.get('searchEngine')]['site'],
                         'Домашняя страница': self.settings.get('homePage')}
        title = self.new_page_box.currentText()
        self.settings.set('newPage', {'title': title, 'site': new_page_dict[title]})

    def change_tab_bar_position(self, position):
        self.settings.set('TabBarPosition', position)
        self.window.tab_widget.set_tab_bar_position(position)

    def clear_cache(self):
        if QMessageBox.question(self.abstract_page, 'Подтверждение операции',
                                'Это действие удалит весь кеш программы. Продолжить?') == QMessageBox.Yes:
            self.FS.clear_cache()
            QTimer.singleShot(100, lambda: self.cache_label.setText(f'Кеш: {human_bytes(get_folder_size(f"{self.FS.user_dir()}/cache"))}'))

    @Slot()
    def update_program(self):
        msg = QMessageBox(self.window)
        msg.setWindowTitle('Обновление')

        last = last_version(__name__)
        current = __version__
        if current == last:
            msg.setIcon(QMessageBox.Information)
            msg.setText('У вас установлена последняя версия программы')
            msg.setStandardButtons(QMessageBox.Ok)
        else:
            msg.setText(f'Последняя версия: {last}\nТекущая версия: {current}')
            msg.setIcon(QMessageBox.Question)
            msg.setInformativeText('Обновить?')
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg.exec() == QMessageBox.Yes:
                os.system(f'pip3 install {__name__} --upgrade')
                if QMessageBox.question(self.window, 'Операция завершена', 'Перезапустить?') == QMessageBox.Yes:
                    restart()

    @Slot()
    def create_shortcut(self):
        if QMessageBox.question(self.abstract_page, 'Подтверждение операции',
                                'Пересоздать ярлык запуска программы в системе?') == QMessageBox.Yes:
            make_shortcut()

    def history_checkbox_command(self):
        if self.history_checkbox.isChecked():
            if QMessageBox.question(self.abstract_page, 'Подтверждение операции',
                                    'Это действие удалит всю вашу историю. Продолжить?') == QMessageBox.Yes:
                self.window.history.remove_all()
                self.history_list_widget.empty_info_label.setText('История отключена в настройках')
                return True
            else:
                return False
        self.history_list_widget.empty_info_label.setText('Список истории пуст')
        return True

    def cookie_checkbox_command(self):
        if self.cookie_checkbox.isChecked():
            if QMessageBox.question(self.abstract_page, 'Подтверждение операции',
                                    'Это действие удалит все текущие Cookie-файлы. Продолжить?') == QMessageBox.Yes:
                self.window.profile.cookieStore().deleteAllCookies()
                print('[Веб-Профиль]: Все cookie удалены')
                return True
            else:
                return False
        return True

    class SectionsPanel(QListWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self.setObjectName('sections_panel')
            self.setIconSize(QSize(25, 25))
            self.setFrameShape(QListWidget.NoFrame)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            parent.layout().addWidget(self)

        def add(self, icon):
            item = QListWidgetItem(icon, "", self)
            item.setSizeHint(QSize(16777215, 40))

    class Section(QWidget):
        def __init__(self, parent, icon: str):
            super().__init__(parent)
            self.setLayout(QVBoxLayout())
            self.layout().setContentsMargins(10, 0, 10, 0)

            self.scroll_area = QScrollArea(self)
            self.layout().addWidget(self.scroll_area)
            self.scroll_area.setWidgetResizable(True)
            self.scroll_content = QWidget()
            self.scroll_content_layout = QVBoxLayout()
            self.scroll_content_layout.setContentsMargins(0, 0, 0, 0)
            self.scroll_content.setLayout(self.scroll_content_layout)
            self.scroll_area.setWidget(self.scroll_content)

            parent.layout().addWidget(self)

            self.icon = QIcon(icon)
            parent.parent().sections_panel.add(self.icon)

        def add_widget(self, widget):
            self.scroll_content_layout.addWidget(widget)

        def add_spacer(self, spacer):
            self.scroll_content_layout.addItem(spacer)

    class SettingsCheckBox(QCheckBox):
        def __init__(self, parent, text, option, command=None, command_exec='after', restart: bool = False,
                     tooltip=None, block=False):
            super().__init__(parent)
            self.setText(text)
            self.setMinimumSize(QSize(0, 25))
            self.setChecked(parent.settings.get(option))
            self.parent = parent
            self.option = option
            self.restart = restart
            self.command = command
            self.command_exec = command_exec
            self.clicked.connect(self.checked)
            self.setDisabled(block)
            if tooltip is not None:
                self.setToolTip(tooltip)

        def checked(self):
            if self.command is not None:
                if self.command_exec == 'after':
                    self.parent.settings.set(self.option)
                    self.setChecked(self.parent.settings.get(self.option))
                    if self.restart:
                        self.parent.restart_button.show()
                    self.command()
                else:
                    self.setChecked(self.parent.settings.get(self.option))
                    if self.command():
                        self.parent.settings.set(self.option)
                        self.setChecked(self.parent.settings.get(self.option))
                        if self.restart:
                            self.parent.restart_button.show()
            else:
                self.parent.settings.set(self.option)
                self.setChecked(self.parent.settings.get(self.option))
                if self.restart:
                    self.parent.restart_button.show()

    class DownloadListWidget(TreeWidget):
        def __init__(self, parent):
            super().__init__(parent, ['Имя файла', 'Действия', 'Информация'])
            self.header().resizeSection(0, 400)
            self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

            self.empty_info_label.setText('Список загрузок пуст')

        @Slot(object)
        def add(self, item):
            old_item = self.findItems(item.name, Qt.MatchContains, 0)
            if old_item:
                print('REMOVE OLD DOWNLOAD', old_item[0])
                self.takeTopLevelItem(self.indexOfTopLevelItem(old_item[0]))
            widget_item = QTreeWidgetItem([item.name, None, None])
            widget_item.download = item
            self.insertTopLevelItem(0, widget_item)
            self.count += 1
            download_item_size = QTreeWidgetItem()
            download_item_size.setText(0, 'Размер')
            download_item_size.setText(2, human_bytes(item.total_bytes))
            widget_item.addChild(download_item_size)

            download_item_date = QTreeWidgetItem()
            download_item_date.setText(0, 'Дата')
            download_item_date.setText(2, item.date.strftime("%d-%m-%Y %H:%M"))
            widget_item.addChild(download_item_date)

            download_item_source = QTreeWidgetItem()
            download_item_source.setText(0, 'Источник')
            download_item_source.setText(2, item.url)
            widget_item.addChild(download_item_source)

            download_item_buttons = QWidget()
            download_item_buttons.setLayout(QHBoxLayout())
            download_item_buttons.layout().setContentsMargins(0, 0, 0, 0)

            folder_button = QPushButton()
            folder_button.setObjectName('downloads_item_folder')
            folder_button.setToolTip('Открыть каталог, где был сохранен файл')
            folder_button.clicked.connect(lambda: open_in_file_manager(item.path))
            folder_button.setFixedSize(30, 30)
            download_item_buttons.layout().addWidget(folder_button)

            self.setItemWidget(widget_item, 1, download_item_buttons)

            item_progress_bar = QProgressBar()
            self.setItemWidget(widget_item, 2, item_progress_bar)

            if hasattr(item, 'request'):
                item.request.isFinishedChanged.connect(
                    lambda: self._download_finished(item, item_progress_bar, download_item_size))
                item.request.receivedBytesChanged.connect(
                    lambda: self._received_bytes_changed(item, item_progress_bar, download_item_size)),
                item.request.totalBytesChanged.connect(
                    lambda: download_item_size.setText(2, human_bytes(item.total_bytes)))
            else:
                item_progress_bar.setValue(int(item.received_bytes * 100 / item.total_bytes))
                item_progress_bar.setFormat(item.status)
            self.show_empty_message()

        def context_menu(self, event):
            menu = BrowserContextMenu(self.window())
            index = self.indexAt(event)

            if not index.isValid():
                return

            item = self.itemAt(event)
            if not item.parent():
                if hasattr(item.download, 'request'):
                    deleted_text = 'Отменить загрузку'
                    remove_action = item.download.request.cancel
                else:
                    deleted_text = 'Убрать'
                    remove_action = lambda: self.window().downloads.remove(item.download)
                menu.addAction(deleted_text, remove_action)
            menu.popup(self.mapToGlobal(event))

        @Slot()
        def _received_bytes_changed(self, item, progress_bar, size_label):
            try:
                progress_bar.setValue(int(item.request.receivedBytes() * 100 / item.total_bytes))
            except OverflowError:
                pass
            size_label.setText(2, human_bytes(item.total_bytes))

        @Slot()
        def _download_finished(self, item, progress_bar, size_label):
            status_text = self.window().downloads.state_dict.get(item.request.state(), {
                'notify_title': 'Файл не был загружен',
                'status': 'Неизвестно'
            })['status']
            progress_bar.setValue(int(item.request.receivedBytes() * 100 / item.total_bytes))
            size_label.setText(2, human_bytes(item.total_bytes))
            progress_bar.setFormat(status_text)

        @Slot(object)
        def remove(self, item):
            items = self.findItems(item.name, Qt.MatchContains, 0)
            for i in items:
                self.takeTopLevelItem(self.indexOfTopLevelItem(i))
                self.count -= 1
            self.show_empty_message()

        @Slot()
        def remove_all(self):
            msg = QMessageBox(self.window())
            msg.setWindowTitle('Подтверждение операции')
            msg.setText('Очистить список?')
            msg.setIcon(QMessageBox.Question)
            msg.setInformativeText('Загружаемые файлы будут отменены')
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg.exec() == QMessageBox.Yes:
                self.window().downloads.remove_all()

    class BookmarksListWidget(TreeWidget):
        def __init__(self, parent):
            super().__init__(parent, ['Название', 'Адрес'])
            self.header().resizeSection(0, 700)
            self.itemDoubleClicked.connect(lambda i, c: self.window().tab_widget.create_tab(url=i.text(1), end=False))
            self.empty_info_label.setText('Нет сохраненных закладок')

        def context_menu(self, event):
            menu = BrowserContextMenu(self.window())
            index = self.indexAt(event)

            if not index.isValid():
                return

            url = self.itemAt(event).text(1)

            menu.addAction('Открыть в новой вкладке', lambda: self.window().tab_widget.create_tab(url=url, end=False))
            menu.addAction('Открыть в новом окне', lambda: self.window().create_new_window(url=url))
            menu.addSeparator()
            menu.addAction('Удалить', lambda: self.window().bookmarks.remove(url))
            menu.popup(self.mapToGlobal(event))

        @Slot(object)
        def add(self, item):
            bookmark_item = QTreeWidgetItem([item.title, item.url])
            bookmark_item.setToolTip(0, item.title)
            bookmark_item.setToolTip(1, item.url)
            self.insertTopLevelItem(0, bookmark_item)
            self.count += 1
            self.show_empty_message()

        @Slot(str)
        def remove(self, url):
            items = self.findItems(url, Qt.MatchContains, 1)
            for i in items:
                self.takeTopLevelItem(self.indexOfTopLevelItem(i))
                self.count -= 1
            self.show_empty_message()

        @Slot()
        def remove_all(self):
            msg = QMessageBox(self.window())
            msg.setWindowTitle('Подтверждение операции')
            msg.setText('Удалить все закладки?')
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg.exec() == QMessageBox.Yes:
                self.window().bookmarks.remove_all()

    class HistoryListWidget(TreeWidget):
        def __init__(self, container):
            super().__init__(container, ['Дата', 'Заголовок', 'Адрес'])
            self.header().resizeSection(0, 200)
            self.header().resizeSection(1, 500)
            if self.window().private:
                empty_text = 'Включен приватный режим'
            elif not self.window().settings.get('saveHistory'):
                empty_text = 'История отключена в настройках'
            else:
                empty_text = 'Список истории пуст'
            self.empty_info_label.setText(empty_text)

        def context_menu(self, event):
            menu = BrowserContextMenu(self.window())
            index = self.indexAt(event)

            if not index.isValid():
                return

            item = self.itemAt(event)
            id_ = item.h_item.id
            url = item.h_item.url

            menu.addAction('Открыть в новой вкладке', lambda: self.window().tab_widget.create_tab(url=url, end=False))
            menu.addAction('Открыть в новом окне', lambda: self.window().create_new_window(url=url))
            menu.addSeparator()
            menu.addAction('Удалить', lambda: self.window().history.remove(id_))
            menu.popup(self.mapToGlobal(event))

        @Slot(object)
        def add(self, item):
            tree_item = QTreeWidgetItem([item.date.strftime("%d-%m-%Y %H:%M"), item.title, item.url])
            tree_item.h_item = item
            tree_item.setToolTip(1, item.title)
            tree_item.setToolTip(2, item.url)
            self.insertTopLevelItem(0, tree_item)
            self.count += 1
            self.show_empty_message()

        @Slot(str)
        def remove(self, id_):
            for i in range(self.count):
                if self.topLevelItem(i).h_item.id == id_:
                    self.takeTopLevelItem(i)
                    self.count -= 1
                    return self.show_empty_message()

        @Slot()
        def remove_all(self):
            msg = QMessageBox(self.window())
            msg.setWindowTitle('Подтверждение операции')
            msg.setText('Очистить историю посещений?')
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if msg.exec() == QMessageBox.Yes:
                self.window().history.remove_all()
