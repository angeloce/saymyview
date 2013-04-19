#coding:utf-8


from sqlalchemy import *


metadata = MetaData()

def create_table(name, *args, **kwargs):
    args = list(args)
    args.insert(0, Column('id', Integer, primary_key=True))
    kwargs['mysql_engine'] = 'InnoDB'
    return Table(name, metadata, *tuple(args), **kwargs)


user_table = create_table('user',
    Column('username', String(20), unique=True),
    Column('password', String(128)),
)


web_page_table = create_table('web_page',
    Column('url', String(255), unique=True),
    Column('update_date', DateTime),
    Column('create_date', DateTime),
)


web_page_script_table = create_table('web_page_script',
    Column('url', String(255), unique=True),
    Column('script', Text),
    Column('update_date', DateTime),
)


session_table = create_table('request_session',
    Column('session_id', String(32), unique=True),
    Column('session_data', Text, ),
    Column('expires', DateTime),
)

