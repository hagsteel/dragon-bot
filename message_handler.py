import commands
import settings

"""
:hagsteel!~hagsteel@90.169.219.27 PRIVMSG #swampdragon :smint
Message(prefix='hagsteel!~hagsteel@90.169.219.27', command='PRIVMSG', params=['#swampdragon'], text='smint')

:hagsteel!~hagsteel@90.169.219.27 PRIVMSG dribble :hi lolsor
Message(prefix='hagsteel!~hagsteel@90.169.219.27', command='PRIVMSG', params=['dribble'], text='hi lolsor')
"""

def get_command(bot, message):
    if message.command == 'PING':
        return commands.PongCommand(bot, message)

    if message.command == 'NOTICE' and message.prefix == 'NickServ!NickServ@services.' and message.text.startswith('This nickname is registered'):
        return commands.IdentifyCommand(bot, message)

    if message.command == 'NOTICE' and message.prefix == 'NickServ!NickServ@services.' and message.text.startswith('You are now identified for'):
        return commands.JoinCommand(bot, message)

    if message.command == 'PRIVMSG':
        if message.params[0] == settings.CHANNEL:
            recipient = settings.CHANNEL
        else:
            recipient = message.get_nick()

        if 'hello' in message.text:
            return commands.SayHelloCommand(bot, message, recipient)
        if message.text.lower().startswith('!op me'):
            return commands.MakeOpCommand(bot, message, recipient)
        if message.text.lower().startswith('!kick '):
            return commands.KickCommand(bot, message, recipient)


def handle_message(bot, message):
    command = get_command(bot, message)
    if command:
        command.execute()
