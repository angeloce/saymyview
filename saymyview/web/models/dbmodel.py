#coding:utf-8

from base import database
from sqlalchemy import Column, Integer, String, DateTime, Text



class User(database.Model):
    __tablename__ = 'user'

    account = Column(String(20))
    nickname = Column(String(20))
    password = Column(String(128))
    wherefrom = Column(Integer)


class WebPage(database.Model):
    __tablename__ = "web_page"

    url = Column(String(255))
    update_date = Column(DateTime)
    create_date = Column(DateTime)


class WebPageScript(database.Model):
    __tablename__ = "web_page_script"

    url = Column(String(255))
    script = Column(Text)
    update_date = Column(DateTime)



if __name__ == '__main__':
    database.create_db()
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'create':
        database.create_db()