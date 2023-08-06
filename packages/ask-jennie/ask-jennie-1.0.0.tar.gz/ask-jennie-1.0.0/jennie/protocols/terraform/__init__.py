from jennie.protocols.automationprotocol import AutomationProtocol
from jennie.events.common.download_files import event_download_files
from jennie.utils.helper import *

class TerraformAutomations():
    def __init__(self, user_info, logger, commands):
        self.user = user_info
        self.logger = logger
        self.commands = commands
        self.event = commands[0]
        self.type = KEY_STACK_TERRAFORM_AUTOMATIONS
        self.automation_protocol = AutomationProtocol(user_info, logger)
        self.logger.set_class("TerraformAutomations")

    @property
    def execute(self):
        stack = self.commands[0]
        event = self.commands[1]
        self.logger.add("Execute Event", stack="terraform", event=event, type=self.type)
        self.logger.set_class("TerraformAutomations")
        if event == KEY_EVENT_CREATE_README:
            return self.automation_protocol.create_readme_file()

        elif event == KEY_EVENT_DOWNLOAD:
            return self.automation_protocol.download_automation(
                self.commands, self.type
            )

        elif event == KEY_EVENT_UPLOAD:
            return self.upload(
                update=False
            )

        elif event == KEY_EVENT_UPDATE:
            return self.upload(
                update=True
            )

        elif event == KEY_EVENT_DELETE:
            return self.automation_protocol.delete_automations(
                commands=self.commands, type=self.type
            )

        elif event == KEY_EVENT_SYNC:
            return self.automation_protocol.sync_automation(
                commands=self.commands, type=self.type
            )
        else:
            raise ValueError("Unknown Docker Automation Event")

    def build_automation_conf(self, app_name):
        terraform_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if
                  f.split(".")[0] in ['tf', 'tfvars']]

        if len(terraform_files) == 0:
            raise ValueError("No Terraform File found")

        self.logger.add("Collected files", terraform_files=terraform_files)
        files = []
        for file in terraform_files:
            files.append(
                {
                    KEY_OUT_PATH: file,
                    KEY_FILE_PATH: file
                }
            )

        self.logger.add("Upload files", files=files)
        return event_download_files(
            self.user["token"], app_name, KEY_STACK_DOCKER_AUTOMATIONS
        ).build_event(files)

    def upload(self, update):
        default_values = None
        if update:
            default_values = self.automation_protocol.get_config_file()
        self.logger.add("Upload Automation", default_values=default_values)
        config = self.automation_protocol.build_app_basic_config(
            commands=self.commands[1:], stack="terraform",
            type=self.type, default_values=default_values
        )
        self.logger.add("Build upload configration", config=config)
        files_event = self.build_automation_conf(
            config["app_name"]
        )
        config["automation_conf"] = [files_event]
        self.logger.add("Build automation configration", automation_conf=config["automation_conf"])
        self.automation_protocol.validate_and_upload_automation(
            config, update
        )


