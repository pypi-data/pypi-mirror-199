import re

import devoud.browser.page.web as web
from devoud.browser.page.embedded.view import EmbeddedView
from devoud.browser.page.embedded.pages.control import ControlPage
from devoud.browser.page.embedded.pages.notfound import NotFoundPage
from devoud.browser.page.embedded.pages.void import VoidPage

embedded_pages = {'devoud://control.py': ControlPage,
                  'devoud://control.py#settings': ControlPage,
                  'devoud://control.py#history': ControlPage,
                  'devoud://control.py#bookmarks': ControlPage,
                  'devoud://control.py#downloads': ControlPage,
                  'devoud://notfound.py': NotFoundPage,
                  'devoud://void.py': VoidPage}

redirects = {'about:blank': NotFoundPage.url,
             'web://desktop': 'https://dustinbrett.com/',
             'web://macos': 'https://macos9.app/'}

url_protocol_pattern = re.compile(r'^(?:http|https|ftp|ftps|devoud|file)://', re.IGNORECASE)
url_pattern = re.compile("^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")


def is_url(url):
    """По протоколу либо по домену"""
    if url:
        return (re.match(url_protocol_pattern, url) is not None) or (re.match(url_pattern, url) is not None)


def url_type(url):
    """Возвращает тип страницы"""
    return EmbeddedView if url[:9].lower() == 'devoud://' else web.view.BrowserWebView


def get_view(url):
    return web.view.BrowserWebView if url_type(url) is web.view.BrowserWebView else embedded_pages.get(url, NotFoundPage)
