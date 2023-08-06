import os
from jennie.protocols.angular.uilib import AngularUILibProtocol
from jennie.protocols.automationprotocol import AutomationProtocol
from jennie.utils.checks import check_angular_ui_module_directory, check_if_angular_project
from jennie.constants.protocol import KEY_EVENT_DOWNLOAD, KEY_EVENT_SYNC, KEY_EVENT_UPLOAD, \
    KEY_EVENT_UPDATE, KEY_EVENT_CREATE_README, KEY_EVENT_ADD_EVENT, KEY_STACK_ANGULAR_AUTOMATION

class AngularAutomations():
    def __init__(self, user_info, logger, commands):
        self.user = user_info
        self.logger = logger
        self.commands = commands
        self.init_variables(self.commands)
        self.validate(event=self.event)
        self.logger.set_class("AngularAutomations")

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
            KEY_EVENT_DOWNLOAD,
            KEY_EVENT_SYNC
        ]
        component_dir = [
            KEY_EVENT_CREATE_README
        ]
        automation_dir = [
            KEY_EVENT_ADD_EVENT
        ]
        print (self.stack)
        if self.stack == "ui-lib":
            component_dir.append(KEY_EVENT_UPLOAD)
            component_dir.append(KEY_EVENT_UPDATE)
        else:
            automation_dir.append(KEY_EVENT_UPLOAD)
            automation_dir.append(KEY_EVENT_UPDATE)

        if event in component_dir:
            self.files = check_angular_ui_module_directory(self.out)
            if not self.files:
                raise ValueError("Not a valid angular component to perform {} event", event)

        elif event in main_dir:
            status = check_if_angular_project(self.out)
            if not status:
                os.system("ls")
                raise ValueError("Not a valid angular project to perform {} event".format(event))

        elif event in automation_dir:
            status = os.path.exists(self.out + "jennie.conf.json")
            if not status:
                raise ValueError("Not a valid automation folder to perform {} event", event)

    @property
    def execute(self):
        if self.stack == "ui-lib":
            self.logger.add("Execute Angular UI lib protocol")
            return AngularUILibProtocol(
                user_info=self.user,
                logger=self.logger,
                commands=self.commands[1:],
                files=self.files,
                out=self.out
            ).execute
        elif self.stack == "automations":
            self.logger.add("Execute Angular automation protocol")
            return AutomationProtocol(
                self.user, self.logger
            ).execute(
                self.commands, KEY_STACK_ANGULAR_AUTOMATION
            )
        else:
            raise ValueError("Invalid Protocol Stack!")