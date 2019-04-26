class BaseAIModel:
    def __init__(self, chat_log_filename, myname):
        self.corpus_filename = chat_log_filename
        self.name = myname
        self.blacklist = ['gonzobot']

    def trigger(self, username, input_string):
        return 'model triggered'
