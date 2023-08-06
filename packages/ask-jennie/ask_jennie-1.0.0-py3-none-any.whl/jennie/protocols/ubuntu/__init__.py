class UbuntuAutomations():
    def __init__(self, user_info, logger, commands):
        self.user = user_info
        self.logger = logger
        self.commands = commands

    def execute(self, event, _name):
        return True