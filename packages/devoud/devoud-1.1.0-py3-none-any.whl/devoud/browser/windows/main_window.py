from functools import cached_property
from platform import system
from string import Template

from PySide6.QtCore import QSize, QEvent, Slot
from PySide6.QtGui import QIcon, QFontDatabase, QFont, Qt, QShortcut, QKeySequence
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PySide6.QtWidgets import QWidget, QGridLayout, QFrame, QToolButton

from devoud import __name__, __version__, rpath
from devoud.browser.userbase import UserBase
from devoud.browser.bookmarks import Bookmarks
from devoud.browser.downloads import Downloads
from devoud.browser.filesystem import FileSystem
from devoud.browser.history import History
from devoud.browser.page.web import search_engines
from devoud.browser.page.web.adblocker import AdBlocker, RequestInterceptor
from devoud.browser.session import Session
from devoud.browser.settings import Settings
from devoud.browser.styles import Theme
from devoud.browser.widgets.address_panel import AddressPanel
from devoud.browser.widgets.find_on_page import FindOnPageWidget
from devoud.browser.widgets.tab_widget import BrowserTabWidget
from devoud.browser.widgets.title_bar import CustomTitleBar
from devoud.browser.windows.size_grip import SizeGrip

if system() == 'Windows':
    from devoud.browser.windows.win32_window import Win32Window as MainWindow
else:
    from PySide6.QtWidgets import QMainWindow as MainWindow


class BrowserWindow(MainWindow):
    def __init__(self, private: bool = False, session=None, settings: dict = None, profile=None):
        super().__init__()
        self.private = private
        self.FS = FileSystem(self)
        self.userbase = UserBase(self)

        self.settings = Settings(self)
        self.settings.use(settings)

        self.session = Session(self)
        self.session.use(session)

        self.history = History(self)
        self.bookmarks = Bookmarks(self)
        self.downloads = Downloads(self)
        self.theme = Theme(self)

        self.setWindowIcon(QIcon(self.theme.app_icons.get(system(), 'icons:devoud.png')))
        self.setWindowTitle(__name__)
        self.setMinimumSize(QSize(400, 300))
        size = self.screen().availableGeometry()
        self.resize(size.width() * 2 / 3, size.height() * 2 / 3)

        # профиль для веб-страниц
        if not private:
            if profile is None:
                self.profile = QWebEngineProfile('DevoudProfile')
                self.profile.setCachePath(f'{self.FS.user_dir()}/cache')
                self.profile.setPersistentStoragePath(f'{self.FS.user_dir()}/web_storage')
                self.profile.downloadRequested.connect(self.downloads.download_request)
            else:
                self.profile = profile
        else:
            self.profile = QWebEngineProfile.defaultProfile()
            self.profile.downloadRequested.connect(self.downloads.download_request)
            self.settings.set('saveHistory', False)
            self.settings.set('restoreSession', False)
            self.settings.set('cookies', False)
            print(f'[Окно]: Включен приватный режим, данные не сохраняются')

        self.profile.settings().setDefaultTextEncoding('utf-8')
        self.profile.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, self.settings.get('smoothScroll'))
        self.profile.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.profile.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.profile.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.profile.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, self.settings.get('javascript'))
        if not self.settings.get('cookies'):
            self.profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)

        # блокировщик рекламы
        self.ad_blocker = AdBlocker(self)
        if self.ad_blocker.is_enable():
            self.ad_blocker.add_rules()
            self.interceptor = RequestInterceptor(self.ad_blocker.rules)
            self.profile.setUrlRequestInterceptor(self.interceptor)

        # шрифт
        QFontDatabase.addApplicationFont(rpath('ui/fonts/ClearSans-Medium.ttf'))
        self.setFont(QFont('Clear Sans Medium'))

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.window_layout = QGridLayout(self.central_widget)
        self.window_layout.setSpacing(0)
        self.window_layout.setContentsMargins(0, 0, 0, 0)

        # всё кроме size grip
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName('main_frame')

        # FIXME: тени для окна с кастомной рамкой ломают рендер веб-страниц
        # self.window_shadow = QGraphicsDropShadowEffect(self)
        # self.window_shadow.setBlurRadius(17)
        # self.window_shadow.setXOffset(0)
        # self.window_shadow.setYOffset(0)
        # self.window_shadow.setColor(QColor(0, 0, 0, 150))
        # self.main_frame.setGraphicsEffect(self.window_shadow)

        self.window_layout.addWidget(self.main_frame, 1, 1)
        self.main_layout = QGridLayout(self.main_frame)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # выбор рамки окна
        self.title_bar = None
        if not self.settings.get('systemWindowFrame'):
            self.title_bar = CustomTitleBar(self)
            self.main_layout.addWidget(self.title_bar, 0, 0)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.enable_rounded_corners()

            # для растяжения окна с кастомной рамкой
            if system() != 'Windows':
                self.window_layout.addWidget(SizeGrip(side='right'), 1, 2)
                self.window_layout.addWidget(SizeGrip(side='left'), 1, 0)
                self.window_layout.addWidget(SizeGrip(side='top'), 0, 1)
                self.window_layout.addWidget(SizeGrip(side='bottom'), 2, 1)
                self.window_layout.addWidget(SizeGrip(side='top-right'), 0, 2)
                self.window_layout.addWidget(SizeGrip(side='top-left'), 0, 0)
                self.window_layout.addWidget(SizeGrip(side='bottom-right'), 2, 2)
                self.window_layout.addWidget(SizeGrip(side='bottom-left'), 2, 0)
            else:
                self.nativeEvent = self.native_event

            self.changeEvent = self.change_event

        # адресная панель
        self.address_panel = AddressPanel(self)
        self.main_layout.addWidget(self.address_panel, 1, 0, 1, 1)
        self.address_line_edit = self.address_panel.address_line_edit
        self.add_tab_button = self.address_panel.add_tab_button

        # виджет вкладок
        self.main_layout.addWidget(self.tab_widget, 3, 0)
        self.tab_widget.set_tab_bar_position()

        # комбинации клавиш
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.update_page)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.show_find_on_page)
        QShortcut(QKeySequence("Alt+H"), self).activated.connect(lambda: self.load_home_page(new_tab=False))
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(self.tab_widget.create_tab)
        QShortcut(QKeySequence("Ctrl+Shift+T"), self).activated.connect(self.session.restore_last_closed_page)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(
            lambda: self.bookmarks.append(self.page().data()))
        QShortcut(QKeySequence("Ctrl+Shift+O"), self).activated.connect(
            lambda: self.tab_widget.create_tab(url='devoud://control.py#bookmarks'))
        QShortcut(QKeySequence("Ctrl+H"), self).activated.connect(
            lambda: self.tab_widget.create_tab(url='devoud://control.py#history'))
        QShortcut(QKeySequence("Ctrl+J"), self).activated.connect(
            lambda: self.tab_widget.create_tab(url='devoud://control.py#downloads'))
        QShortcut(QKeySequence("Ctrl+W"), self).activated.connect(
            lambda: self.tab_widget.close_tab(self.tab_widget.currentIndex()))
        QShortcut(QKeySequence("Alt+Left"), self).activated.connect(self.back_page)
        QShortcut(QKeySequence("Alt+Right"), self).activated.connect(self.forward_page)

        self.session.restore()

    def change_event(self, event):
        if event.type() == QEvent.WindowStateChange:
            is_maximized = self.isMaximized()
            self.enable_rounded_corners(not is_maximized)
            for grip in self.findChildren(SizeGrip):
                grip.setHidden(is_maximized)

    def page(self):
        """Возвращает текущую страницу"""
        return self.tab_widget.current()

    def load(self, url):
        self.page().load(url)

    def reload(self):
        self.page().reload()

    def search(self, text_query: str, new_tab=False):
        url = f'{self.window().current_search_engine()["query"]}{text_query}'
        if new_tab:
            self.tab_widget.create_tab(url=url)
        else:
            self.page().load(url)

    def current_search_engine(self):
        return search_engines[self.address_panel.search_box.currentText()]

    def change_style(self, name=None):
        self.theme = Theme(self, name)
        self.setStyleSheet(self.theme.style())
        self.address_panel.update_ssl_button()
        self.address_line_edit.findChild(QToolButton).setIcon(QIcon('custom:close(address_line_frame).svg'))

    def enable_rounded_corners(self, rounded: bool = True):
        self.main_frame.setStyleSheet(Template("""
                #main_frame { 
                    border-radius: $radius;
                }""").substitute(radius='12px' if rounded else '0px'))

    def show_find_on_page(self):
        page = self.page()
        find_on_page_widget = page.findChild(FindOnPageWidget)
        if find_on_page_widget:
            if find_on_page_widget.isHidden():
                find_on_page_widget.show()
            else:
                find_on_page_widget.hide()
        elif not page.view.embedded:
            find_on_page_widget = FindOnPageWidget(page)
            page.layout().addWidget(find_on_page_widget)
            find_on_page_widget.show()

    def load_home_page(self, new_tab=True):
        if new_tab:
            self.tab_widget.create_tab(url=self.settings.get('homePage'))
        else:
            self.page().load(self.settings.get('homePage'))

    def set_title(self, text, icon: QIcon = None):
        title = f"{'[Приватный режим]' if self.private else ''} {text} – {__name__} {__version__}"
        self.setWindowTitle(title)
        if self.title_bar is not None:
            if icon:
                self.title_bar.icon.setPixmap(icon.pixmap(18, 18))
            self.title_bar.icon.setHidden(not icon)
            self.title_bar.label.setText(title)

    def back_page(self):
        self.page().back()

    def forward_page(self):
        self.page().forward()

    def stop_load_page(self):
        self.page().stop()

    def update_page(self):
        self.page().reload()

    @Slot()
    def create_new_window(self, private=None, url=None, settings=None):
        # TODO: Упростить код
        print('[Окно]: Создание нового окна')
        if private is None:
            private = self.private
        if url is not None:
            session = {"0": {
                "url": url
            }}
        else:
            if private:
                session = None
            else:
                session = self.session.session().copy()
        profile = None if private else self.profile
        if settings is None:
            settings = self.settings.settings().copy()  # обязательно передавать копию!!!
        window = BrowserWindow(private=private, session=session, settings=settings, profile=profile)
        window.show()
        window.change_style()

    def closeEvent(self, event):
        print('[Окно]: Закрытие')
        self.session.save()
        self.tab_widget.currentChanged.disconnect()
        self.session.clear_objects()
        self.deleteLater()
        return super().closeEvent(event)

    def restart(self):
        print('[Окно]: Перезапуск')
        self.session.save()
        self.close()
        self.create_new_window(self.private)

    @cached_property
    def tab_widget(self):
        return BrowserTabWidget()
