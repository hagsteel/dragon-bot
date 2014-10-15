import socket
from tornado.iostream import IOStream
from message_handler import handle_message
from message_parser import parse_message
import settings


class DribbleBot(object):
    stream = None

    def send(self, data, callback=None):
        data = '{}\r\n'.format(data)
        self.stream.write(data.encode())
        self.wait_for_message(callback)

    def send_message(self, recipient, message, callback=None):
        msg = 'PRIVMSG {} :{}'.format(recipient, message)
        print('--> {}'.format(msg))
        self.send(msg, callback)

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = IOStream(sock)
        self.stream.connect((settings.SERVER, settings.PORT), self.connected)

    def connected(self):
        self.wait_for_message()
        self.set_nick()

    def wait_for_message(self, callback=None):
        if self.stream._read_callback:
            return
        if not callback:
            callback = self.process_message
        self.stream.read_until(b'\r\n', callback)

    def process_message(self, message):
        if settings.DEBUG:
            print(message)
        msg = parse_message(message)
        handle_message(self, msg)
        self.wait_for_message()

    def set_nick(self):
        message = 'USER {nick} 0 * :{name}'.format(**{
            'nick': settings.NICK,
            'name': settings.NAME
        })
        print('-> {}'.format(message))
        self.send(message)
        self.send('NICK {}'.format(settings.NICK))
