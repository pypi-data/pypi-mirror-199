import os
from jennie.protocols.automationprotocol import AutomationProtocol
from jennie.utils.checks import check_if_django_project
from jennie.constants.protocol import KEY_EVENT_DOWNLOAD, KEY_EVENT_UPLOAD, \
    KEY_EVENT_UPDATE, KEY_EVENT_CREATE_README, KEY_EVENT_ADD_EVENT, KEY_STACK_DJANGO_AUTOMATIONS

class DjangoAutomations():
    def __init__(self, user_info, logger, commands):
        self.user = user_info
        self.logger = logger
        self.commands = commands
        self.init_variables(self.commands)
        self.validate(event=self.event)
        self.logger.set_class("DjangoAutomations")

    def init_variables(self, commands):
        self.files = None
        self.out = os.getcwd()
        self.stack = commands[0]
        self.event = commands[1]
        if len(commands) > 2:
            self._name = commands[2]

        if self.out[:-1] != "/":
            self.out += "/"

    def validate(self, event):
        """
        Validate is
        :param event:
        :return:
        """
        main_dir = [
            KEY_EVENT_DOWNLOAD
        ]

        automation_dir = [
            KEY_EVENT_ADD_EVENT, KEY_EVENT_CREATE_README, KEY_EVENT_UPLOAD,
            KEY_EVENT_UPDATE
        ]

        if event in main_dir:
            status = check_if_django_project(self.out)
            if not status:
                os.system("ls")
                raise ValueError("Not a valid Django project to perform {} event".format(event))

        elif event in automation_dir:
            status = os.path.exists(self.out + "jennie.conf.json")
            if not status:
                raise ValueError("Not a valid automation folder to perform {} event", event)

    @property
    def execute(self):
        if self.stack == "automations":
            self.logger.set_class("Running Django automation protocol")
            AutomationProtocol(
                self.user, self.logger
            ).execute(
                self.commands, KEY_STACK_DJANGO_AUTOMATIONS
            )
        else:
            raise ValueError("Invalid Protocol Stack!")