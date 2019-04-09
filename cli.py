#!/usr/bin/env python3

import ai

class CLI:
    def __init__(self):
        self.is_running = True
        self.ai = ai.AI()

    def loop(self):
        while self.is_running:
            msg = input(">>> ")
            print('Response: '+self.ai.command('Hexorg', msg))

            

if __name__ == '__main__':
    cli = CLI()
    cli.loop()
