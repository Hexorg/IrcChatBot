#!/usr/bin/env python3

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import Markov
import ai
import os

class MarkovBot(irc.bot.SingleServerIRCBot):
        def __init__(self, channel, nickname, server, port=6667):
            irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
            self.channel = channel
            self.nick = nickname
            self.ai = ai.AI(nickname)

        def on_nicknameinuse(self, c, e):
            self.nick = c.get_nickname() + "_"
            c.nick(self.nick)

        def on_welcome(self, c, e):
            c.join(self.channel)

        def sanitize_output(self, ret):
            if ret is not None:
                output_lines = []
                lines = ret.split('\n')
                for line in lines:
                    if len(line) > 500:
                        index = line.rfind(' ')
                        if index == -1:
                            output_lines.append(line[:500])
                            output_lines.append(line(500:]))
                        else:
                            output_lines.append(line[:index])
                            output_lines.append(line[index+1:])
                    else:
                        output_lines.append(line)
                return output_lines
        
        def on_privmsg(self, c, e):
            if len(e.arguments) > 0:
                ret = self.sanitize_output(self.ai.command(e.source.nick, e.arguments[0]))
                if ret is not None:
                    for line in ret:
                        c.privmsg(e.source.nick, line)
                        

        def on_pubmsg(self, c, e):
            if len(e.arguments) > 0:
                ret = self.sanitize_output(elf.ai.pubmsg(e.source.nick, e.arguments[0]))
                if ret is not None:
                    for line in ret:
                        c.privmsg(self.channel, line)

if __name__ == '__main__': 
    bot = MarkovBot('#hexbottest', 'Hexbotter', 'irc.snoonet.org')
    bot.start()
