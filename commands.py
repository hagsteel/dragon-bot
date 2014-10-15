from message_parser import parse_message
import settings


class BaseCommand(object):
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    def execute(self):
        raise NotImplementedError()


class PongCommand(BaseCommand):
    def execute(self):
        self.bot.send('PONG ping')


class JoinCommand(BaseCommand):
    def execute(self):
        self.bot.send('JOIN {}'.format(settings.CHANNEL))


class IdentifyCommand(BaseCommand):
    def execute(self):
        print('-> Identifying nick')
        message = 'identify {}'.format(settings.PASSWORD)
        self.bot.send_message('NickServ', message)


class BaseInteractionCommand(BaseCommand):
    def __init__(self, bot, message, recipient):
        super().__init__(bot, message)
        self.recipient = recipient

    def user_check(self):
        self.bot.send_message('NickServ', 'ACC {}'.format(self.message.get_nick()), callback=self.on_user_checked)

    def on_user_checked(self, message):
        msg = parse_message(message)
        if not msg.command == 'NOTICE' and msg.get_nick() != 'NickServ':
            return self.check_fail()
        expected = '{} ACC '.format(self.message.get_nick())
        try:
            if int(msg.text.split(expected)[1]) > 2:
                self.check_pass()
        except:
            self.check_fail()

    def check_fail(self):
        pass

    def check_pass(self):
        pass


class SayHelloCommand(BaseInteractionCommand):
    def execute(self):
        message = 'Hello to all'
        self.bot.send('PRIVMSG {} :{}'.format(self.recipient, message))


class MakeOpCommand(BaseInteractionCommand):
    def execute(self):
        self.user_check()

    def check_pass(self):
        if self.message.get_nick() in settings.ADMINS:
            self.bot.send('MODE {} +o {}'.format(settings.CHANNEL, self.message.get_nick()))
            self.bot.send_message(settings.CHANNEL, 'There you go...')

    def check_fail(self):
        self.bot.send_message(settings.CHANNEL, 'Oi {}, stop that!'.format(self.message.get_nick()))


class KickCommand(BaseInteractionCommand):
    def execute(self):
        self.user_check()

    def check_pass(self):
        if self.message.get_nick() in settings.ADMINS:
            self.bot.send('KICK {} {}'.format(settings.CHANNEL, self.message.get_nick()))

    def check_fail(self):
        self.bot.send_message(settings.CHANNEL, 'Oi {}, stop that!'.format(self.message.get_nick()))
