import collections

trail_marker = ' :'


class Message(collections.namedtuple('Message', 'prefix command params text')):
    def get_nick(self):
        try:
            return self.prefix.split('!')[0]
        except IndexError:
            return None


def parse_message(message):
    message = message.decode().strip()
    prefix, data = get_prefix(message)
    command = get_command(data)
    params = get_params(data)
    text = get_text(data)
    return Message(prefix, command, params, text)


def get_prefix(data):
    if data.startswith(':'):
        space_index = data.index(' ')
        return data[1:space_index], data[space_index:].strip()
    return None, data


def get_command(data):
    return data.split(' ')[0]


def get_text(data):
    if ' :' not in data:
        return None
    return data.split(trail_marker)[-1]


def get_params(data):
    trail_index = -1
    if trail_marker in data:
        trail_index = data.index(trail_marker)
    lines = data[:trail_index].split(' ')
    if len(lines) > 1:
        return lines[1:]
    return None
