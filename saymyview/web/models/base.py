#coding:utf-8


from sqlalchemy import create_engine

from sqlalchemy import select
from sqlalchemy import Column, Integer


class BaseModel(object):

    def __init__(self, connection):
        self.connection = connection

    def execute(self, *args, **kw):
        return self.connection.execute(*args, **kw)

    def select(self, columns, *args, **kwargs):
        if not isinstance(columns, (tuple, list)):
            columns = [columns]
        return select(columns, *args, **kwargs)


class DataBase(object):
    def __init__(self, **settings):
        self._settings = settings

    @property
    def engine(self):
        if not hasattr(self, '_engine'):
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
        self._connection = self._engine.connect()
        return self._connection


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
