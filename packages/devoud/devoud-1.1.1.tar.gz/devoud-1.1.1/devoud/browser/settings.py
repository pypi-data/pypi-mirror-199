from pathlib import Path
import json
from sys import platform


class Settings:
    filename = 'settings.json'
    default = {"saveHistory": False,
               "restoreSession": False,
               "adblock": True,
               "cookies": True,
               "javascript": True,
               "systemWindowFrame": False if platform != 'darwin' else True,
               "smoothScroll": False,
               "theme": "night",
               "homePage": "https://web.tabliss.io/",
               "searchEngine": "Yandex",
               "newPage": {"title": "Заставка с часами", "site": "https://web.tabliss.io/"},
               "TabBarPosition": "Сверху"}

    def __init__(self, parent):
        self.parent = parent
        self.FS = parent.FS
        self._dict = {}

    def use(self, settings: dict):
        if settings:
            self._dict = settings
        else:
            with Path(self.FS.user_dir(), self.filename).open() as settings_file:
                try:
                    self._dict = json.load(settings_file)
                except json.decoder.JSONDecodeError:
                    print(
                        f'[Закладки]: Произошла ошибка при чтении {self.filename}, ошибка: {json.decoder.JSONDecodeError}')
                    self._restore_file()

    def settings(self) -> dict:
        return self._dict

    def set(self, option, arg=None):
        """Если arg не установлен, то значение инвертируется"""
        if arg is None:
            try:
                self._dict[option] = not self._dict[option]
            except KeyError:
                try:
                    self._dict[option] = not self.default[option]
                except KeyError:
                    return print(f'[Настройки]: Параметра {option} не существует в настройках!')
        else:
            self._dict[option] = arg
        if not self.parent.private:
            with Path(self.FS.user_dir(), self.filename).open('w') as settings_file:
                json.dump(self._dict, settings_file, indent=4, ensure_ascii=False)

    def get(self, option):
        try:
            default = self.default[option]
            data = self._dict.get(option, default)
            if isinstance(data, type(default)):
                return data
            else:
                print('[Настройки]: Неверный тип данных для опции, идёт восстановление')
                self._dict[option] = default
                with Path(self.FS.user_dir(), self.filename).open('w') as settings_file:
                    json.dump(self._dict, settings_file, indent=4, ensure_ascii=False)
                return default
        except KeyError:
            print(f'[Настройки]: Параметра {option} не существует в настройках!')
            return None

    def _restore_file(self) -> None:
        print('[Настройки]: Идёт восстановление настроек')
        self._dict = self.default
        if not self.parent.private:
            with Path(self.FS.user_dir(), self.filename).open('w') as settings_file:
                json.dump(self._dict, settings_file, indent=4, ensure_ascii=False)
