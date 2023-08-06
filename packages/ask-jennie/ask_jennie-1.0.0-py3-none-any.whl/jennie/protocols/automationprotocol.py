import os.path
import requests
from jennie.constants.protocol import *
from jennie.utils.apicallhandler import APICalls
from jennie.utils.colorprinting import ColorPrinting
from jennie.utils.helper import create_readme_with_config, \
    take_user_input, read_json_file, write_json_file, get_basic_conf, get_app_name
from jennie.events.rule_engine import RuleEngine

JENNIE_CONF_FILE_NAME = "jennie.conf.json"

class AutomationProtocol():
    def __init__(self, user_info, logger):
        self.user_info = user_info
        self.logger = logger
        self.api_calls = APICalls(logger=logger)
        self.print_logs = ColorPrinting()
        
    def execute(self, commands, type):
        stack = commands[0]
        event = commands[1]
        self.logger.add("Execute Event", commands=commands, type=type)
        if event == KEY_EVENT_CREATE_README:
            return self.create_readme_file()

        elif event == KEY_EVENT_DOWNLOAD:
            return self.download_automation(
                commands, type
            )

        elif event == KEY_EVENT_UPLOAD:
            return self.upload_automation(
                is_update=False
            )

        elif event == KEY_EVENT_UPDATE:
            return self.upload_automation(
                is_update=True
            )

        elif event == KEY_EVENT_DELETE:
            return self.delete_automations(
                commands=commands, type=type
            )

        elif event == KEY_EVENT_SYNC:
            return self.sync_automation(
                commands=commands, type=type
            )

        elif event == KEY_EVENT_CREATE:
            return self.create_automation(
                commands, type, stack
            )

        elif event == KEY_EVENT_ADD_EVENT:
            return self.add_event(commands)

        else:
            raise ValueError("Unknown Angular Automation Event")

    def raise_error_invalid_config(self, name):
        raise ValueError("There is some error in Automation configration for {}"
            "\ncontact dextrop@ask-jennie.com for support".format(name)
        )

    def get_app_name(self, commands):
        self.logger.add("get_app_name", commands=commands)
        app_name = None
        if len(commands) > 2:
            app_name = commands[2]

        if app_name == None:
            app_name = take_user_input(
                {"app_name": "Input application name require to download"})["app_name"]

        return app_name

    def create_readme_file(self):
        self.logger.add("create_readme_file")
        app_title = create_readme_with_config(
            JENNIE_CONF_FILE_NAME
        )
        return True

    def build_app_basic_config(self, commands, stack, type, default_values=None):
        self.logger.add("build_app_basic_config", commands=commands,
                        stack=stack, type=type, default_values=default_values)
        is_create = False
        if default_values != None:
            is_create = True
            app_name = default_values["app_name"]
        else:
            app_name = self.get_app_name(commands)
        return get_basic_conf(
            app_name=app_name, type=type,
            stack=stack, api_call_obj=self.api_calls,
            is_create=is_create, default_inputs=default_values
        )

    def get_automation_from_api(self, app_name, type):
        self.logger.add("get_automation_from_api", app_name=app_name, type=type)
        conf = self.api_calls.download_automation(
            app_name, type
        )
        return conf

    def validate_events(self, automation_info):
        self.logger.add("validate_events", automation_info=automation_info)
        token = None
        if self.user_info != None:
            token = self.user_info["token"]
        rule_engine = RuleEngine(
            app_name=automation_info["app_name"],
            app_type=automation_info["type"],
            logger=self.logger,
            token=token
        )

        validated = rule_engine.validate_events(automation_info["automation_conf"])
        self.print_logs.success("Automation Validated Successfully ...")
        return rule_engine, validated

    def validate_and_execute_events(self, automation_info):
        self.logger.add("validate_and_execute_events", automation_info=automation_info)
        rule_engine, validated = self.validate_events(automation_info)
        if not validated:
            self.raise_error_invalid_config(automation_info["app_name"])
        rule_engine.execute_events(automation_info["automation_conf"])
        return True

    def validate_and_upload_automation(self, automation_info, is_update=False):
        self.logger.add("validate_and_execute_events", automation_info=automation_info, is_update=is_update)
        rule_engine, validated = self.validate_events(automation_info)
        if not validated:
            self.raise_error_invalid_config(automation_info["app_name"])

        response = self.api_calls.upload_automation(
            type=automation_info["type"], json_conf=automation_info, is_update=is_update
        )
        write_json_file(JENNIE_CONF_FILE_NAME, response)
        self.print_logs.success("Automation Uploaded Successfully ...")
        return response

    def get_config_file(self):
        self.logger.add("get_config_file")
        if not os.path.exists(JENNIE_CONF_FILE_NAME):
            raise ValueError("Missing file {}".format(JENNIE_CONF_FILE_NAME))
        return read_json_file(JENNIE_CONF_FILE_NAME)

    def sync_automation(self, commands, type):
        self.logger.add("sync_automation", commands=commands, type=type)
        app_name = self.get_app_name(commands)
        configuration = self.get_automation_from_api(
            app_name, type
        )

        os.system("mkdir {}".format(configuration["app_name"]))
        if configuration["readme"] != "":
            readme_file_link = configuration["readme"]
            readme_file_path = "{}/readme.md".format(configuration["app_name"])

            file_content = self.api_calls.download_file(readme_file_link)
            open(readme_file_path, "w").write(file_content)

        if configuration["app_image"] != "":
            image_file_link = configuration["app_image"]
            image_file_path = "{}/{}".format(configuration["app_name"], image_file_link.split("/")[-1])

            f = open(image_file_path, 'wb')
            f.write(requests.get(image_file_link).content)
            f.close()

        # @todo this part of code is not running.
        for event in configuration["automation_conf"]:
            if event[KEY_EVENT_TYPE] == EVENT_DOWNLOAD_FILES:
                for file in event[KEY_FILES]:
                    content = self.api_calls.download_file(
                        file[KEY_FILE_LINK]
                    )
                    filepath = "{}/{}".format(configuration["app_name"], file[KEY_FILE_LINK].split("/")[-1])
                    open(filepath, "w").write(content)
                    file[KEY_OUT_PATH] = filepath
                    del file[KEY_FILE_LINK]

        write_json_file(
            "{}/jennie.conf.json".format(configuration["app_name"]), configuration
        )
        return True

    def add_event(self, commands):
        self.logger.add("add_event", commands=commands)
        conf = self.get_config_file()
        event_type = None
        if len(commands) > 0:
            event_type = commands[0]

        event_info = RuleEngine(
            app_name=conf["app_name"],
            app_type=conf["type"],
            logger=self.logger,
            token=self.user_info["token"]
        ).add_event(event_type)
        conf["automation_conf"].append(event_info)
        write_json_file(JENNIE_CONF_FILE_NAME, conf)
        return True

    def create_automation(self, commands, type, stack):
        self.logger.add("create_automation", commands=commands, type=type, stack=stack)
        self.app_name = self.get_app_name(commands)
        config = get_basic_conf(
            app_name=self.app_name, type=type,
            stack=stack, api_call_obj=self.api_calls, is_create=True
        )

        os.system("mkdir {}".format(self.app_name))
        write_json_file("{}/jennie.conf.json".format(self.app_name), config)

    def upload_automation(self, is_update):
        self.logger.add("upload_automation", is_update=is_update)
        default_conf = self.get_config_file()
        if is_update:
            default_conf = get_basic_conf(
                app_name=default_conf["app_name"], type=default_conf["type"],
                stack=default_conf["stack"], api_call_obj=self.api_calls,
                default_inputs=default_conf
            )

        if default_conf:
            self.validate_and_upload_automation(
                default_conf
            )
            return True
        return False

    def download_automation(self, commands, type):
        self.logger.add("download_automation", commands=commands, type=type)
        app_name = self.get_app_name(commands)
        configration = self.get_automation_from_api(
            app_name, type
        )
        if configration:
            self.validate_and_execute_events(configration)
            return True
        return False

    def delete_automations(self, commands, type):
        self.logger.add("delete_automations", commands=commands, type=type)
        app_name = self.get_app_name(commands)
        choice = input("Are your sure you want to delete {} module from server? press C to cancel".format(app_name))
        if choice.lower() != "c":
            self.api_calls.delete_automation_api_call(type, app_name)
            print("Automation module deleted successfully")
            return True
        return False


