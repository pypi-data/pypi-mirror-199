import json
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon

from devoud.browser.page.abstract_page import AbstractPage
from devoud.browser.page.embedded.pages.control import ControlPage
from devoud.browser.widgets.tab_widget import BrowserTabWidget


class Session:
    filename = 'session.json'

    def __init__(self, parent):
        self.window = parent
        self.FS = parent.FS
        self.tab_widget: BrowserTabWidget = parent.tab_widget
        self.__dict = {}
        self.__objects = []
        self.__closed_pages = []
        self.save_timer = None

    def session(self) -> dict:
        return self.__dict

    def use(self, session: dict):
        if session:
            self.__dict = session
        else:
            if self.window.settings.get('restoreSession') and not self.window.private:
                with Path(self.FS.user_dir(), self.filename).open(encoding='utf-8') as session_file:
                    try:
                        self.__dict = json.load(session_file)
                    except Exception as error:
                        print(
                            f'[Вкладки]: Произошла ошибка при чтении {self.filename}, ошибка: {error}')
                        self._restore_file()

                # таймер для автоматического сохранения сессии раз в три минуты
                self.save_timer = QTimer(self.window)
                self.save_timer.setInterval(180000)
                self.save_timer.timeout.connect(self.save)
                self.save_timer.start()

    def pages(self) -> list:
        return self.__objects

    def urls(self) -> list:
        return list(map(lambda page: page.url, self.__objects))

    def add_page(self, page: AbstractPage):
        self.__objects.append(page)

    def remove_page(self, page: AbstractPage):
        self.__closed_pages.append(page.url)
        self.__objects.remove(page)

    def closed_pages(self):
        return self.__closed_pages

    def restore_last_closed_page(self):
        if self.__closed_pages:
            self.tab_widget.create_tab(url=self.__closed_pages.pop())

    def clear_objects(self):
        for page in self.__objects:
            page.deleteLater()
        self.__objects.clear()

    def update_control_pages(self):
        for page in self.__objects:
            if isinstance(page.view, ControlPage):
                page.reload()

    def restore(self):
        if self.__dict:
            try:
                self.tab_widget.currentChanged.disconnect()
                for key, data in self.__dict.items():
                    if key.isdigit():
                        url = data.get('url', self.window.settings.get('homePage'))
                        page = AbstractPage(self.tab_widget,
                                            url=url,
                                            title=data.get('title', url if url else 'Vasily ate cheese'))
                        self.tab_widget.create_tab(page=page, switch=False, load=False, index=int(key))
                        page.icon = QIcon(data.get('icon', None))
                self.tab_widget.currentChanged.connect(self.tab_widget.tab_changed)
                self.tab_widget.setCurrentIndex(self.__dict.get('lastPage', 0))
                if self.tab_widget.current().view is None:
                    self.window.reload()
                print('[Вкладки]: Предыдущая сессия восстановлена')
            except Exception as error:
                print(f'[Вкладки]: Не удалось восстановить прошлую сессию, ошибка: {error}')
                self.window.tab_widget.currentChanged.connect(self.window.tab_widget.tab_changed)
                self.window.load_home_page(new_tab=True)
        else:
            self.window.load_home_page()

    def save(self):
        if self.window.settings.get('restoreSession') and not self.window.private:
            self.__dict.clear()
            for tab_index in range(self.window.tab_widget.count()):
                page = self.window.tab_widget.widget(tab_index)
                icon_path = None
                if page.icon:
                    icon_path = f'{self.FS.user_dir()}/cache/favicon/{tab_index}.png'
                    page.icon.pixmap(32, 32).save(icon_path)
                self.__dict[str(tab_index)] = {
                    'url': page.url,
                    'title': page.title,
                    'icon': icon_path
                }
            self.__dict['lastPage'] = self.window.tab_widget.currentIndex()
            with Path(self.window.FS.user_dir(), self.filename).open('w', encoding='utf-8') as session_file:
                try:
                    json.dump(self.__dict, session_file, sort_keys=True, indent=4, ensure_ascii=False)
                except Exception as error:
                    print(f'[Вкладки]: Произошла ошибка при записи данных в {self.filename}, ошибка: {error}')
                else:
                    return print('[Вкладки]: Текущая сессия сохранена')
        print('[Вкладки]: Текущая сессия не сохранена')

    def _restore_file(self):
        print('[Вкладки]: Идёт восстановление файла сессии')
        self.__dict = {}
        with Path(self.FS.user_dir(), self.filename).open('w', encoding='utf-8') as session_file:
            json.dump(self.__dict, session_file, indent=4, ensure_ascii=False)
