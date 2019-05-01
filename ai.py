from baseModel import BaseAIModel
from Markov import OneGramMarkov

class AIBaseCommand:
    __keyword__ = 'ping'
    __description__ = 'Base class. Returns "pong"'

    def __init__(self, ai):
        self.ai = ai

    def action(self, nick, args):
        return 'pong'

    def get_help(self, nick):
        return 'Syntax: {} '.format(self.__keyword__)+self.__description__

class AIShowCommandsCommand(AIBaseCommand):
    __keyword__ = 'commands'
    __description__ = 'Prints available commands'


    def action(self, nick, args):
        return 'Command list:\n'+'\n'.join(['{} - {}'.format(cmd.__keyword__, cmd.__description__) for cmd in self.ai.command_objects])

class AIShowModelStatsCommand(AIBaseCommand):
    __keyword__ = 'stats'
    __description__ = 'Show stats of currently loaded model'

    def action(self, nick, args):
        return self.ai.model.stats(args)

class AIShowModelsCommand(AIBaseCommand):
    __keyword__ = 'models'
    __description__ = 'Show available speech models'

    def action(self, nick, args):
        return 'Available models:\n'+'\n'.join(['{} - {}'.format(model.__name__, model.__description__) for model in self.ai.model_classes])

class AIShowCurrentModelCommand(AIBaseCommand):
    __keyword__ = 'model'
    __description__ = 'Get current model name'

    def action(self, nick, args):
        return self.ai.model.__class__.__name__

class AIShowTriggerConditions(AIBaseCommand):
    __keyword__ = 'trigger'
    __description__ = 'Find out current model\'s speech trigger pattern'

    def action(self, nick, args):
        return 'As long as {} is in the sentance, '.format(self.ai.name)+self.ai.model.trigger_conditions()

class AIShowCommand(AIBaseCommand):
    __keyword__ = 'show'
    __description__ = 'Prints useful into about subcomponents'

    def __init__(self, ai):
        super().__init__(ai)
        self.subcommand_objects = [AIShowCommandsCommand(ai), AIShowCurrentModelCommand(ai), AIShowModelsCommand(ai), AIShowModelStatsCommand(ai), AIShowTriggerConditions(ai)]
        self.subcommands = {cmd.__keyword__:cmd for cmd in self.subcommand_objects}

    def action(self, nick, args):
        if len(args) > 0:
            if args[0] in self.subcommands:
                return self.subcommands[args[0]].action(nick, args[1:])
            else:
                return "I can't show {}".format(args[0])
        else:
            return self.ai.commands[AIHelpCommand.__keyword__].action(nick, [self.__keyword__])

    def get_help(self, nick):
        return 'Syntax: {} <items>: {}\n'.format(self.__keyword__, self.__description__)+'Possible calls:\n'+'\n'.join(['{} {} - {}'.format(self.__keyword__, cmd.__keyword__, cmd.__description__) for cmd in self.subcommand_objects])


class AIHelpCommand(AIBaseCommand):
    __keyword__ = 'help'
    __description__ = 'Shows usage and command help'

    def action(self, nick, args):
        if len(args) == 0:
            return 'Private message case-sensitive command syntax: <Command>[ <arg1>[ <arg2>[...]]]\nUse: help <command> to get specific command help\n'+self.ai.commands[AIShowCommand.__keyword__].action(nick, [AIShowCommandsCommand.__keyword__])
        else:
            if args[0] in self.ai.commands:
                return self.ai.commands[args[0]].get_help(nick)
            else:
                return 'Unknown command {}\n'.format(args[0])+self.ai.commands[AIShowCommand.__keyword__].action(nick, [AIShowCommandsCommand.__keyword__])


class AIUseCommand(AIBaseCommand):
    __keyword__ = 'use'
    __description__ = 'Tells AI to use a new speech model'

    def action(self, nick, args):
        if len(args) == 1:
            if args[0] in self.ai.models:
                self.ai.model = self.ai.models[args[0]](self.ai.chat_log_filename, self.ai.name)
                with open(self.ai.chat_log_filename, 'r') as f:
                    for line in f:
                        data = line.split(':')
                        nick = data[0][1:-1]
                        text = (':'.join(data[1:]))[:-1]
                        self.ai.model.learn_line(nick, text)
                return 'Model {} loaded'.format(args[0])
            else:
                return 'Can\'t find model {}'.format(args[0])
        else:
            return 'Usage: {} <ModelName>'.format(self.__keyword__)


class AIPubmsgCommand(AIBaseCommand):
    __keyword__ = 'pubmsg'
    __description__ = 'Command to test AI\'s parsing of public messages'

    def action(self, nick, args):
        return self.ai.pubmsg(nick, ' '.join(args))

class AI:
    def __init__(self, name):
        self.name = name
        self.chat_log_filename = 'chat_log.txt'

        self.command_objects = [AIBaseCommand(self), AIHelpCommand(self), AIShowCommand(self), AIUseCommand(self), AIPubmsgCommand(self)]
        self.commands = {cmd.__keyword__:cmd for cmd in self.command_objects}
        self.permissions = {'Hexorg': '*'}

        self.model_classes = [BaseAIModel, OneGramMarkov]
        self.models = {cls.__name__:cls for cls in self.model_classes}
        self.model = self.model_classes[0](self.chat_log_filename, self.name)

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

        return self.commands[command].action(nick, args)


    def pubmsg(self, nick, text):
        if self.name in text:
            return self.model.trigger(nick, text)
        else:
            with open(self.chat_log_filename, 'a') as f:
                f.write('<{}>: {}\n'.format(nick, ''.join(text)))
            self.model.learn_line(nick, ''.join(text))
            return None
