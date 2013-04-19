#coding:utf-8


import sys
import tornado.ioloop
import tornado.autoreload
from application import application



def run_shell(argv=None):
    def ipython():
        try:
            from IPython import embed
            embed()
        except ImportError:
            from IPython.Shell import IPShell
            shell = IPShell(argv=[])
            shell.mainloop()

    def plain_python():
        import code
        imported_objects = {}
        try:
            import readline
            import rlcompleter
            readline.set_completer(rlcompleter.Completer(imported_objects).complete)
            readline.parse_and_bind("tab:complete")
        except ImportError:
            pass
        code.interact(local=imported_objects)

    try:
        ipython()
    except ImportError:
        plain_python()


def main():
    method = sys.argv[1]
    argv = sys.argv[2:]
    if method == 'run':
        if len(sys.argv) > 2:
            port = int(sys.argv[2])
        else:
            port = 8000
        application.listen(port)
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.start()
    elif method == 'shell':
        run_shell(argv)



if __name__ == '__main__':
    main()
