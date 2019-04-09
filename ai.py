class AI:
    def __init__(self):
        self.chat_log = open('chat_log.txt', 'a')

    def command(self, nick, command):
        print("CMD: {}: {}".format(nick, command))

    def learn(self, nick, text):
        print("learn: {}: {}".format(nick, text))
        self.chat_log.write('<{}>: {}\n'.format(nick, ''.join(text)))
