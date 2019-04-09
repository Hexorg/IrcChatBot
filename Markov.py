#!/usr/bin/env python3

import random, yaml

class Chain():
    def __init__(self):
        self._chain = {}

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

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(yaml.dump(self._chain))

    def load(self, filename):
        with open(filename, 'r') as f:
            self._chain = yaml.load(f)
            
