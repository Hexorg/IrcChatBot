#!/usr/bin/env python3

import random
from collections import deque
from baseModel import BaseAIModel
class OneGramMarkov(BaseAIModel):

    def __init__(self, chat_log_filename, myname):
        super().__init__(chat_log_filename, myname)
        self._chain = {}
        self.learn()

    def learn(self):
        with open(self.corpus_filename, 'r') as f:
            for line in f:
                data = line.split(':')
                owner = data[0][1:-1]
                text = ':'.join(data[1:])
                if owner not in self.blacklist:
                    if not text.startswith('.'):
                        tokens = text.split(' ')
                        lastToken = None
                        for i in range(len(tokens)):
                            if len(tokens[i]) > 0:
                                if lastToken is None:
                                    lastToken = tokens[i]
                                elif lastToken != tokens[i]:
                                    self.extend(owner, lastToken, tokens[i])
                                lastToken = tokens[i]

    def trigger(self, owner, text):
        if text.startswith('.{}'.format(self.name)) and ' ' in text:
            user, start = text.split(' ')[1:3]
            if user in self._chain:
                sentance = [w for w in self.follow_chain(user, start)]
                if len(sentance) > 1:
                    return ' '.join(sentance)
                elif len(sentance) == 1:
                    return '{} never said {}'.format(user, sentance[0])
        return 'Usage: .{} NICK START_WORD'.format(self.name)


    def stats(self, args):
        if len(args) == 0:
            top_users = []
            top_dicts = []
            for user in self._chain:
                if len(top_users) < 5:
                    top_users.append(user)
                    top_dicts.append(len(self._chain[user]))
                else:
                    cdictlen = len(self._chain[user])
                    lowest_talker_id = 0
                    lowest_talker_num = 999999
                    for i in range(len(top_users)):
                        if top_dicts[i] < lowest_talker_num:    
                            lowest_talker_id = i
                            lowest_talker_num = top_dicts[i]
                    if cdictlen > lowest_talker_num:
                        top_users[lowest_talker_id] = user
                        top_dicts[lowest_talker_id] = cdictlen
                        
            return 'Users: {}\nTop talkers: {}'.format(len(self._chain), ', '.join(['{} ({})'.format(top_users[i], top_dicts[i]) for i in range(len(top_users))]))
        else:
            if args[0] in self._chain:
                return '{} knows {} words:\n{}'.format(args[0], len(self._chain[args[0]]), ', '.join(self._chain[args[0]]))
            else:
                return 'User {} not in corpus'.format(args[0])

     

    def _random_choice(self, data):
        total = 0
        for key in data:
            total += data[key]
        r = random.uniform(0, total)
        for key in data:
            r -= data[key]
            if r <= 0:
                return key

    def extend(self, owner, item1, item2):
        if owner not in self._chain.keys():
            self._chain[owner] = {}

        if item1 in self._chain[owner].keys():
            if item2 in self._chain[owner][item1]:
                self._chain[owner][item1][item2] += 1
            else:
                self._chain[owner][item1][item2] = 1
        else:
            self._chain[owner][item1] = {item2: 1}

    def follow_chain(self, owner, start):
        p = start
        keys = self._chain[owner].keys()
        count = 0
        while p in keys:
            count += 1
            yield p
            c = p[-1:]
            if c == '.' or c == '?' or c == '!' or count > 30:
                break
            p = self._random_choice(self._chain[owner][p])
        yield p

