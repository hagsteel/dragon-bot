#!/usr/bin/env python
from tornado.ioloop import IOLoop
from dribble import DribbleBot


def run():
    bot = DribbleBot()
    bot.connect()
    IOLoop.instance().start()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass
