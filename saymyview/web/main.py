#coding:utf-8


import sys
import tornado.ioloop
import tornado.autoreload
from application import application



def main():
    method = sys.path[1]
    if method == 'run':
        if len(sys.path) > 2:
            port = int(sys.path[2])
        else:
            port = 8000
        application.listen(port)
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.start()

    elif method == 'createdb':
        application.database.create_db()



if __name__ == '__main__':
    main()
