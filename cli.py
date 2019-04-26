#!/usr/bin/env python3

import ai

class CLI:
    def __init__(self):
        self.is_running = True
        self.ai = ai.AI('Rorick')

    def loop(self):
        while self.is_running:
            msg = input(">>> ")
            ret = self.ai.command('hexorg', msg)
            if ret is not None:
                print('Response: '+ret)
            else:
                print('No response')

            

if __name__ == '__main__':
    cli = CLI()
    cli.loop()
