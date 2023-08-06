from jennie.protocols.terraform import TerraformAutomations
from jennie.protocols.nodejs import NodeJSAutomations
from jennie.protocols.angular import AngularAutomations
from jennie.protocols.reactjs import ReactJSAutomations
from jennie.protocols.django import DjangoAutomations
from jennie.protocols.docker import DockerAutomations
from jennie.protocols.packer import PackerAutomations
from jennie.protocols.ubuntu import UbuntuAutomations
from jennie.utils.colorprinting import ColorPrinting

PROTOCOL_MAPPING = {
    "angular": AngularAutomations,
    "django": DjangoAutomations,
    "ubuntu": UbuntuAutomations,
    "docker": DockerAutomations,
    "packer": PackerAutomations,
    "terraform": TerraformAutomations,
    "nodejs": NodeJSAutomations,
    "reactjs": ReactJSAutomations,
}

class JennieProtocols():
    def __init__(self, commands, userinfo, logger):
        self.commands = commands
        self.userinfo = userinfo
        self.logger = logger
        self.platform = self.commands[0]
        self.logger.set_class("JennieProtocols")

    @property
    def execute(self):
        if not self.platform in PROTOCOL_MAPPING:
            raise ValueError("Protocol Not found ...")

        if len(self.commands) > 2 and self.commands[2] != "download" and self.userinfo == None:
            ColorPrinting().error("To {} library on jennie server you need to login first\n refer https://automations.ask-jennie.com/documentation")
            return False

        self.logger.add("Running Jennie Protocol", platform=self.platform)
        status = PROTOCOL_MAPPING[self.platform](
            user_info=self.userinfo,
            commands=self.commands[1:],
            logger=self.logger
        ).execute
        self.logger.add("Executed jennie automation command successfully")
        self.logger.save_logs()
        return status
