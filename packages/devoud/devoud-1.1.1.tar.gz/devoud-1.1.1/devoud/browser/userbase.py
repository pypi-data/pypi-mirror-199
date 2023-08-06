import sqlite3
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base


class UserBase:
    db = declarative_base()
    filename = 'userbase.db'

    def __init__(self, window):
        self.window = window
        self.__db_path = None
        self.engine = None
        self.session = None
        if not window.private:
            self.__db_path = Path(window.FS.user_dir(), self.filename)
            sqlite3.connect(self.__db_path)
        else:
            self.__db_path = ':memory:'  # Будет храниться в оперативной памяти
        self.engine = create_engine(f'sqlite:///{self.__db_path}')
        self.session = Session(bind=self.engine)
        UserBase.db.metadata.create_all(self.engine)
