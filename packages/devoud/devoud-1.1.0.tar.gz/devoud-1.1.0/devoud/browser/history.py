from datetime import datetime
from uuid import uuid4

from PySide6.QtCore import Signal, QObject
from sqlalchemy import String, Column, DateTime

from devoud.browser.userbase import UserBase


class _HistoryT(UserBase.db):
    __tablename__ = 'History'
    id = Column(String, default=lambda: str(uuid4()), primary_key=True)
    title = Column(String)
    url = Column(String)
    date = Column(DateTime, default=datetime.now)


class History(QObject):
    history_add = Signal(object)
    history_remove = Signal(str)
    history_remove_all = Signal()

    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.userbase = window.userbase
        self.session = self.userbase.session

    def get_all(self) -> list:
        """Возвращает список объектов из таблицы"""
        return self.session.query(_HistoryT).all()

    def add(self, data: dict) -> None:
        """Добавляет новую запись истории в таблицу"""
        if self.window.settings.get('saveHistory'):
            history_item = _HistoryT(title=data.get('title', 'Vasily ate cheese'),
                                     url=data.get('url', 'Vasily ate cheese'))
            self.session.add(history_item)
            self.session.commit()
            self.history_add.emit(history_item)

    def remove(self, id_: str) -> None:
        """Удаляет запись истории из таблицы"""
        history_item = self.session.query(_HistoryT).filter_by(id=id_).one()
        self.session.delete(history_item)
        self.session.commit()
        self.history_remove.emit(id_)

    def remove_all(self) -> None:
        """Удаляет все записи истории из таблицы"""
        self.session.query(_HistoryT).delete()
        self.history_remove_all.emit()
