class AI:
    def __init__(self, name):
        self.name = name
        self.chat_log_filename = 'chat_log.txt'
        self.permissions = {'Hexorg': '*'}
        self.commands = {'ping': self.cmd_ping, 
                        'fake_pubmsg': self.cmd_fake_pubmsg,
                        '{},'.format(self.name): self.cmd_public
                        }

    def command(self, nick, command):
        if len(command) > 0:
            command = command.split(' ')
            args = command[1:]
            command = command[0]
        else:
            return None
        if nick not in self.permissions:
            return "I shouldn't talk to strangers"
        else:
            if self.permissions[nick] != '*' and command not in self.permissions[nick]:
                return "{} can't perform '{}'".format(nick, command)
        if command not in self.commands:
            return "Unknown command {}".format(command)

        return self.commands[command](nick, args)

    def cmd_ping(self, nick, args):
        return "pong!"

    def cmd_fake_pubmsg(self, nick, args):
        return self.pubmsg(nick, ' '.join(args))

    def cmd_public(self, nick, args):
        return 'I know nothing!'

    def pubmsg(self, nick, text):
        if text.startswith('{}, '.format(self.name)):
            return self.command(nick, text)
        else:
            with open(self.chat_log_filename, 'a') as f:
                f.write('<{}>: {}\n'.format(nick, ''.join(text)))
            return None
