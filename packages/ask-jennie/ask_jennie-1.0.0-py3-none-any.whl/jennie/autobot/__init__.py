import os
from jennie.autobot.constants import ENTRY_SPEECH, EXIT_SPEECH, INPUT_TEXT
from jennie.autobot.autobotnlp import ASKJennie
from jennie.utils.colorprinting import ColorPrinting

class AutoBot():
    def __init__(self, logger):
        self.clear_screen()
        self.logger = logger
        self.print = ColorPrinting()
        self.print.success (ENTRY_SPEECH)

    def clear_screen(self):
        os.system("clear")

    def take_user_input(self):
        return input(INPUT_TEXT)

    def start(self):
        while(True):
            user_input = self.do_exit(self.take_user_input())
            ASKJennie(self.logger).ask(user_input)

    def do_exit(self, input_speech):
        if (input_speech == "exit" or input_speech == "exit()"):
            self.print.error (EXIT_SPEECH)
            exit()

        return input_speech