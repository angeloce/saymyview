#coding:utf-8


import sys
import tornado.ioloop
import tornado.autoreload
from application import application



def main():
    method = sys.argv[1]
    if method == 'run':
        if len(sys.argv) > 2:
            port = int(sys.argv[2])
        else:
            port = 8000
        print port
        application.listen(port)
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.start()

    elif method == 'createdb':
        application.database.create_db()



if __name__ == '__main__':
    main()
