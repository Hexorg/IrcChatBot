#!/usr/bin/env python3

def f(data):
    l = {}
    top = 0
    for key in data:
        l[key] = len(data[key])
        if l[key] > top:
            top = l[key]

    count = 0
    top2 = 0
    while count < 15:
        for key in l:
            if l[key] > top2:
                if l[key] != top:
                    top2 = l[key]
                else:
                    print('%s: %s' % (key, l[key]))
                    top = top2
                    top2 = 0
                    count += 1


