import glob
import shutil
from platform import system, release
from pathlib import Path

from PySide6.QtCore import QDir

from devoud import root, rpath
from devoud.browser.settings import Settings
from devoud.browser.session import Session
from devoud.browser.utils.shortcuts import make_shortcut


class FileSystem:
    def __init__(self, window):
        self.window = window
        print('[Файлы]: Инициализация файловой системы')
        self.__local_user_dir = Path(root(), 'user')
        print(f'[Файлы]: Текущая операционная система {system()} {release()}')
        self.__user_dir = {'Linux': Path(f'{Path.home()}/.local/share/devoud/user'),
                           'Darwin': Path(f'{Path.home()}/Library/Application Support'),
                           'Windows': Path(f'{Path.home()}/AppData/Roaming/devoud/user')}.get(system(),
                                                                                              self.__local_user_dir)
        print(f'[Файлы]: Рабочий каталог ({Path.cwd()})')
        self.check_program_files()

        # добавить ссылки для ресурсов
        QDir.addSearchPath('custom', f'{self.user_dir()}/generated_icons')
        QDir.addSearchPath('icons', rpath('ui/icons'))

    def user_dir(self):
        """Возвращает путь до каталога с пользовательскими данными"""
        return self.__user_dir

    def check_program_files(self):
        """Проверяет необходимые файлы для работы программы"""
        print(f'[Файлы]: Проверка необходимых файлов')
        if not Path.exists(self.user_dir()):
            print('[Файлы]: Каталог для пользовательских данных не найден, идёт его создание')
            Path.mkdir(self.user_dir(), parents=True, exist_ok=True)
            make_shortcut()
        print(f'[Файлы]: Пользовательские данные лежат в ({self.user_dir()})')

        for directory in ('generated_icons', 'web_storage', 'cache', 'cache/favicon'):
            Path(self.user_dir(), directory).mkdir(parents=True, exist_ok=True)

        for user_file in (Settings.filename, Session.filename):
            if not Path.exists(Path(self.user_dir(), user_file)):
                print(f'[Файлы]: Создается отсутствующий файл {user_file}')
                Path(self.user_dir(), user_file).touch()

    def clear_cache(self):
        """Удаляет данные из каталога с кешем"""
        try:
            self.window.profile.clearHttpCache()
            files = glob.glob(f'{self.user_dir()}/cache/*')
            for dir_ in files:
                if Path(dir_).name != 'Cache':
                    shutil.rmtree(dir_)
        except Exception as error:
            print(f'[Файлы]: Не удалось удалить кеш, ошибка: {error}')
