class BaseAIModel:
    __description__ = 'Base Model. Always triggers and says "triggered"'

    def __init__(self, myname):
        self.name = myname
        self.blacklist = ['gonzobot']

    def learn_line(self, nick, line):
        raise Exception("Not Implemented")

    def trigger(self, username, input_string):
        return 'model triggered'

    def stats(self, args):
        return '{} has no stats'.format(self.__class__.__name__)

    def trigger_conditions(self):
        return '{} triggers every time'.format(self.__class__.__name__)
