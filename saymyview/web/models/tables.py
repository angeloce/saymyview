#coding:utf-8


from sqlalchemy import *


metadata = MetaData()

def create_table(name, *args, **kwargs):
    args = list(args)
    args.insert(0, Column('id', Integer, primary_key=True))
    kwargs['mysql_engine'] = 'InnoDB'
    return Table(name, metadata, *tuple(args), **kwargs)


UserTable = create_table('user',
    Column('username', String(20)),
    Column('nickname', String(20)),
    Column('password', String(128)),
    Column('wherefrom', Integer),
)


WebPageTable = create_table('web_page',
    Column('url', String(255)),
    Column('update_date', DateTime),
    Column('create_date', DateTime),
)


WebPageScriptTable = create_table('web_page_script',
    Column('url', String(255)),
    Column('script', Text),
    Column('update_date', DateTime),
)


RequestSessionTable = create_table('request_session',
    Column('session_id', String(32)),
    Column('session_data', Text),
    Column('expires', DateTime),
)


