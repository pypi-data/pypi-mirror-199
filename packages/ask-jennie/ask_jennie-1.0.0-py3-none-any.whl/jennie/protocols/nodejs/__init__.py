class NodeJSAutomations():
    def __init__(self, user_info, logger):
        self.user = user_info
        self.logger = logger

    def execute(self, event, _name):
        return True