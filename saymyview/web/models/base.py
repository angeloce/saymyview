#coding:utf-8



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer
from sqlalchemy.orm import sessionmaker, scoped_session

from saymyview.web.conf import local

_BaseModel = declarative_base()


class BaseDataBaseModel(object):
    id = Column(Integer, primary_key=True)  # all of tables have id

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @declared_attr
    def __table_args__(self):
        return {'mysql_engine': 'InnoDB'}

    @classmethod
    def create(cls, **kwargs):
        return database.session.add(cls(**kwargs))


class DataBase(object):
    def __init__(self, database, **kwargs):
        self._database = database

    @property
    def session(self):
        if not hasattr(self, '_session'):
            Session = sessionmaker(bind=self.engine)
            Session = scoped_session(Session)
            self._session = Session
        return self._session

    @property
    def engine(self):
        if not hasattr(self, '_engine'):
            self._engine = create_engine(self._database, echo=True)
        return self._engine

    @property
    def Model(self):
        if not hasattr(self, '_model'):
            self._model = declarative_base(cls=BaseDataBaseModel, name='BaseDataBaseModel')
            self._model.query = self.session.query_property()
            self._model.db = self
        return self._model

    def create_db(self):
        return self.Model.metadata.create_all(bind=self.engine)


def make_engine_url(**configs):
    db_engine = configs.get('db_engine', 'mysql')
    db_host = configs.get('db_host', 'localhost')
    db_port = str(configs.get('db_port', ''))
    db_username = configs.get('db_username')
    db_password = configs.get('db_password', '')
    db_name = configs.get('db_name', '')

    url = db_engine + '://'
    if db_username or db_password:
        if not db_username:
            raise ValueError("db_username must be exist if db_password is given")
        url += db_username + (db_password and ':' + db_password) + '@'
    url += db_host + (db_port and ':' + db_port)
    if db_name:
        url += '/' + db_name
    return url


database = DataBase(make_engine_url(**vars(local)))