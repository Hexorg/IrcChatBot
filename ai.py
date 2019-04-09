class AI:
    def __init__(self):
        self.permissions = {'Hexorg': '*'}
        self.commands = {'test': self.cmd_test, 
                        'force_learn': self.cmd_force_learn
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

    def cmd_force_learn(self, nick, args):
        self.learn(nick, ' '.join(args))
        return 'OK'

    def learn(self, nick, text):
        with open('chat_log.txt', 'a') as f:
            f.write('<{}>: {}\n'.format(nick, ''.join(text)))
