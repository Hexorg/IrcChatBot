class BaseAIModel:
    __description__ = 'Base Model. Always triggers and says "triggered"'

    def __init__(self, corpus_filename, myname):
        self.name = myname
        self.corpus_filename = corpus_filename
        self.blacklist = ['gonzobot']

    def trigger(self, username, input_string):
        return 'model triggered'

    def stats(self, args):
        return '{} has no stats'.format(self.__class__.__name__)

    def trigger_conditions(self):
        return '{} triggers every time'.format(self.__class__.__name__)
