class AI:
    def __init__(self, name):
        self.name = name
        self.permissions = {'Hexorg': '*'}
        self.commands = {'test': self.cmd_test, 
                        'fake_pubmsg': self.cmd_fake_pubmsg,
                        '{},'.format(self.name): self.cmd_recall
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

    def cmd_test(self, nick, args):
        return "test!"

    def cmd_fake_pubmsg(self, nick, args):
        self.pubmsg(nick, ' '.join(args))
        return 'OK'

    def cmd_recall(self, nick, args):
        return 'I know nothing!'

    def pubmsg(self, nick, text):
        if text.startswith('{}, '.format(self.name)):
            print(self.command(nick, text))
        else:
            with open('chat_log.txt', 'a') as f:
                f.write('<{}>: {}\n'.format(nick, ''.join(text)))
