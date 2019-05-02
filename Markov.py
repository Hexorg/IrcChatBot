#!/usr/bin/env python3

import random
from collections import deque
from baseModel import BaseAIModel

# Word2Vec:: model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True) 
# model.similar_by_vector(model['cats'] - model['cat'])

class MarkovNode:
    def __init__(self, token, is_start=False, is_end=False): 
        self.prev = []
        self.next = {}
        self.is_start = is_start
        self.is_end = is_end
        self.token = token
        self.key = MarkovNode.token_to_key(token)
        self._max_next = 0

    def add_next(self, node):
        if node.key in self.next:
            self.next[node.key][0] += 1
        else:
            self.next[node.key] = [1, node]
        self._max_next += 1

    def next_random(self):
        r = random.uniform(0, self._max_next)
        key = None
        for key in self.next:
            r -= self.next[key][0]
            if r <= 0:
                return self.next[key][1]
        if key is not None:
            return self.next[key][1]

    def __str__(self):
        return self.token

    def __repr__(self):
        flags = []
        if self.is_start:
            flags.append('start')
        if self.is_end:
            flags.append('end')
        return '{} ({}): {}'.format(self.token, ','.join(flags), ','.join([str(self.next[key][1]) for key in self.next]))

    @staticmethod
    def token_to_key(token):
        t = token.lower()
        if not t[-1].isalpha():
            return t[:-1]
        else:
            return t

class OneGramMarkov(BaseAIModel):
    __description__ = 'Markov chain of space separated tokens'

    def __init__(self, myname):
        super().__init__(myname)
        self._chain = {}

    def learn_line(self, nick, line):
        if nick not in self.blacklist and not line.startswith('.'):
            userid = nick 
            if userid not in self._chain:
                self._chain[userid] = {}

            tokens = line.split(' ')
            if len(tokens) <= 2:
                return
            isNewSentance = True
            lastNode = None
            for i in range(len(tokens)):
                if len(tokens[i]) > 0:
                    c = tokens[i][-1]
                    isEndOfSentance = False
                    if c == '.' or c == '!' or c == '?' or i == len(tokens)-1:
                        isEndOfSentance = True
                    node = MarkovNode(tokens[i], is_start=isNewSentance, is_end=isEndOfSentance)
                    if node.key in self._chain[userid]:
                        node = self._chain[userid][node.key]
                        if isNewSentance:
                            node.is_start = True
                        if isEndOfSentance:
                            node.is_end = True
                    else:
                        self._chain[userid][node.key] = node

                    if lastNode is not None:
                        lastNode.add_next(node)
                        node.prev.append(lastNode)

                    lastNode = node
                
    def trigger_conditions(self):
        return '{}, what would <nick> say about <topic>'.format(self.name)

    def trigger(self, owner, text):
        start_trigger = '{}, what would '.format(self.name)
        if text.startswith(start_trigger):
            text = text[len(start_trigger):]
            if ' ' in text:
                tokens = text.split(' ')
                if len(tokens) > 3:
                    if tokens[1] == 'say' and tokens[2] == 'about':
                        user = tokens[0]
                        if user not in self._chain:
                            return 'Username {} not recognized'.format(user)
                        entry_key = MarkovNode.token_to_key(tokens[3])
                        if not entry_key in self._chain[user]:
                            return '{} never mentioned {}'.format(user, tokens[3])
                        node = self._chain[user][entry_key]
                        output = '<{}> {}'.format(user, self.find_start(node))
                        while node is not None and len(output) < 450:
                            node = node.next_random()
                            if node is not None:
                                output += ' ' + node.token
                            else:
                                break
                            if node.is_end and len(output) > 30:
                                break
                                
                        return output


    def find_start(self, node):
        return node.token
