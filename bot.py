#!/usr/bin/env python3

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import Markov
import ai
import os
import yaml

class MarkovBot(irc.bot.SingleServerIRCBot):
        def __init__(self, channel, nickname, server, port=6667):
            irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
            self.channel = channel
            self.nick = nickname
            self.chain = Markov.Chain()
            self.chain_file = 'askemen.chain'
            self.ai = ai.AI()
            if os.path.exists(self.chain_file):
                self.chain.load(self.chain_file)
            self._load_whitelist()

        def on_nicknameinuse(self, c, e):
            self.nick = c.get_nickname() + "_"
            c.nick(self.nick)

        def on_welcome(self, c, e):
            c.join(self.channel)
        
        def _load_whitelist(self):
            self._whitelist = yaml.load(open('whitelist.yaml', 'r'), Loader=yaml.CLoader)['list']

        def on_privmsg(self, c, e):
            self.ai.command(e.source.nick, e.arguments)
            '''try:
                if len(e.arguments) > 0 and e.arguments[0] == 'Save':
                    self.chain.save(self.chain_file)
                elif len(e.arguments) > 0 and e.arguments[0] == 'Load':
                    self._load_whitelist()
                else:
                    owner, start = self.is_command(e.arguments[0])
                    if owner is not None:
                        says = []
                        for w in self.chain.follow_chain(owner, start):
                            says.append(w)
                        c.privmsg(e.source.nick, ' '.join(says))
                        print(e.source.nick)
                        print(' '.join(says))
                    else:
                        print("Owner is None")
            except Exception as e:
                print(e)
            '''
                        

        def on_pubmsg(self, c, e):
            self.ai.learn(e.source.nick, e.arguments)
            '''
            try:  
                tokens = None
                if len(e.arguments) > 0:
                    owner, start = self.is_command(e.arguments[0])
                    if owner is None:
                        tokens = self._tokenize(e.arguments[0])
                        if tokens is not None:
                            for i, word in enumerate(tokens):
                                if i+1 < len(tokens):
                                    self.chain.extend(e.source.nick, word, tokens[i+1])
                                else:
                                    c = word[-1:]
                                    if c != '.' or c != '?' or c != '!':
                                        self.chain.extend(e.source.nick, word, '.')
                    else:
                        if e.source.nick in self._whitelist:
                            says = []
                            for w in self.chain.follow_chain(owner, start):
                                says.append(w)
                            c.privmsg(self.channel, "They would probably say:")
                            c.privmsg(self.channel, ' '.join(says))
            except:
                self.chain.save(self.chain_file)
'''

if __name__ == '__main__': 
    bot = MarkovBot('#hexbottesting', 'Rorick', 'irc.snoonet.org')
    bot.start()