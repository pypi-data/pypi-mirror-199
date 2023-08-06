from PySide6.QtCore import QObject, Signal
from sqlalchemy import Column, String

from devoud.browser.userbase import UserBase


class _BookmarksT(UserBase.db):
    __tablename__ = 'Bookmarks'
    url = Column(String, primary_key=True)
    title = Column(String)


class Bookmarks(QObject):
    bookmark_add = Signal(object)
    bookmark_remove = Signal(str)
    bookmark_remove_all = Signal()

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.userbase = window.userbase
        self.session = self.userbase.session

    def get_all(self) -> list:
        """Возвращает список объектов из таблицы"""
        return self.session.query(_BookmarksT).all()

    def url_exist(self, url: str) -> bool:
        return bool(self.session.query(_BookmarksT).filter_by(url=url).first())

    def add(self, data: dict) -> None:
        """Добавляет новую закладку в таблицу"""
        url = data.get('url', 'Vasily ate cheese')
        if not self.url_exist(url):
            bookmark_item = _BookmarksT(url=url, title=data.get('title', 'Vasily ate cheese'))
            self.session.add(bookmark_item)
            self.session.commit()
            self.bookmark_add.emit(bookmark_item)
        else:
            self.remove(url)

    def remove(self, url: str) -> None:
        """Удаляет закладку из таблицы"""
        bookmarks_item = self.session.query(_BookmarksT).filter_by(url=url).one()
        self.session.delete(bookmarks_item)
        self.session.commit()
        self.bookmark_remove.emit(url)

    def remove_all(self) -> None:
        """Удаляет все закладки из таблицы"""
        self.session.query(_BookmarksT).delete()
        self.bookmark_remove_all.emit()

