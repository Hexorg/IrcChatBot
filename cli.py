#!/usr/bin/env python3

import ai

class CLI:
    def __init__(self):
        self.is_running = True
        self.ai = ai.AI('Rorick')

    def loop(self):
        while self.is_running:
            try:
                msg = input(">>> ")
            except EOFError:
                return
            ret = self.ai.command('Heg', msg)
            if ret is not None:
                print('<{}>: '.format(self.ai.name) +ret)
            else:
                print('No response')

            

if __name__ == '__main__':
    cli = CLI()
    cli.loop()
