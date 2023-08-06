def main():
    from devoud.browser.utils.shortcuts import make_shortcut  # НИКОГДА НЕ ПЕРЕСТАВЛЯЙ ЭТУ ВЕЩЬ!!!!!!!!!!!
    from pkg_resources import parse_version
    from time import perf_counter
    start_time = perf_counter()
    import sys
    import argparse

    from PySide6.QtWidgets import QApplication

    from devoud import IS_PYINSTALLER, __name__, __version__, __author__
    from devoud.browser.windows.main_window import BrowserWindow
    from devoud.browser.utils.versions import version_label, cli_update
    from devoud.browser.page import is_url

    parser = argparse.ArgumentParser(description='Помощь по командам')
    parser.add_argument("--url", default='', type=str, help="Открыть браузер с этой ссылкой в новой вкладке")
    parser.add_argument("--private", help="Открыть приватное окно", action='store_true')
    parser.add_argument("--version", help="Показать текущую версию программы", action='store_true')
    parser.add_argument("--shortcut", help='Пересоздать ярлык запуска', action='store_true')
    parser.add_argument("--update", help='Проверить и установить обновления', action='store_true')
    args = parser.parse_args()

    if args.version:
        return version_label()
    elif args.shortcut:
        return make_shortcut()
    elif args.update:
        return cli_update(__name__)

    default_qt_args = []
    if sys.platform == 'win32':
        default_qt_args += ['-platform', 'windows:darkmode=2']

    print(fr'''---------------------------------------------
  Добро пожаловать в
  _____  ________      ______  _    _ _____  
 |  __ \|  ____\ \    / / __ \| |  | |  __ \ 
 | |  | | |__   \ \  / / |  | | |  | | |  | |
 | |  | |  __|   \ \/ /| |  | | |  | | |  | |
 | |__| | |____   \  / | |__| | |__| | |__| |
 |_____/|______|   \/   \____/ \____/|_____/ 
    ({__version__}{'Pyinstaller' if IS_PYINSTALLER else ''}) by {__author__}
---------------------------------------------''')
    app = QApplication(sys.argv + default_qt_args)
    app.setApplicationName(__name__)
    app.setApplicationDisplayName(__name__)
    app.setDesktopFileName(__name__)
    app.setOrganizationName(__author__)
    app.setOrganizationDomain(__author__.lower())
    app.setApplicationVersion(__version__)

    window = BrowserWindow(private=args.private)

    if is_url(args.url):
        window.tab_widget.create_tab(url=args.url)

    window.show()
    window.change_style()
    print(f'[Время]: Запуск занял {perf_counter() - start_time:.4f} секунд')

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
