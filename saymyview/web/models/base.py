#coding:utf-8


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


session = sessionmaker()
session = scoped_session(session)


class DataBase(object):
    def __init__(self, settings):
        self._settings = settings
        self.session = session
        self.session.configure(bind=self.engine)

    @property
    def engine(self):
        if not hasattr(self, '_engine'):
            enable_echo = self._settings.get('debug', False)
            self._engine = create_engine(make_engine_url(self._settings), echo=False)
        return self._engine

    @property
    def connection(self):
        if not hasattr(self, '_connection'):
            self.connect()
        if self._connection.closed:
            self.connect()
        return self._connection

    def connect(self):
        self._connection = self.engine.connect()
        return self._connection

    def execute(self, *args, **kwargs):
        return self.connection.execute(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.connection, name)


class Model(object):
    session = session

    @classmethod
    def select(cls):
        return cls.session.query(cls)

    def update(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.session.commit()
        return self

    def insert(self):
        self.session.add(self)
        self.session.commit()
        return self

    def delete(self):
        self.session.delete(self)
        self.session.commit()

BaseModel = declarative_base(cls=Model)


def make_engine_url(configs):
    db_engine = configs.get('db_engine', 'mysql')
    db_host = configs.get('db_host', 'localhost')
    db_port = str(configs.get('db_port', ''))
    db_username = configs.get('db_username')
    db_password = configs.get('db_password', '')
    db_name = configs.get('db_name', 'saymyview')

    url = db_engine + '://'
    if db_username or db_password:
        if not db_username:
            raise ValueError("db_username must be exist if db_password is given")
        url += db_username + (db_password and ':' + db_password) + '@'
    url += db_host + (db_port and ':' + db_port)
    if db_name:
        url += '/' + db_name
    return url
