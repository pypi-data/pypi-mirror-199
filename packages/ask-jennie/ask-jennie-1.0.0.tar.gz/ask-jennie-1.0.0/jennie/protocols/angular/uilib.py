import os
from jennie.constants.protocol import *
from jennie.utils.helper import create_readme_without_config
from jennie.utils.colorprinting import ColorPrinting
from jennie.utils.apicallhandler import APICalls
from jennie.events.rule_engine import RuleEngine
from jennie.utils.helper import take_user_input, add_module_to_downloaded_config, \
    get_basic_conf, read_json_file, get_all_images, write_json_file, download_image

class AngularUILibProtocol():
    def __init__(self, user_info, logger, commands, files, out):
        self.user_info = user_info
        self.logger = logger
        self.commands = commands
        self.files = files
        self.out = out
        self.print_logs = ColorPrinting()
        self.event = self.commands[0]
        self.type = KEY_STACK_ANGULAR_UI_LIB
        self.api_calls = APICalls(logger=logger)

        self.module_name = ""
        self.app_name = None
        if len(self.commands) > 1:
            self.app_name = self.commands[1]

        if len(self.commands) > 2:
            self.module_name = self.commands[2]

        self.logger.set_class("AngularUILibProtocol")

    @property
    def execute(self):
        if self.event == KEY_EVENT_CREATE_README:
            return self.create_readme

        elif self.event == KEY_EVENT_DOWNLOAD:
            return self.download

        elif self.event == KEY_EVENT_UPLOAD:
            return self.upload

        elif self.event == KEY_EVENT_UPDATE:
            return self.update

        elif self.event == KEY_EVENT_DELETE:
            return self.delete

        elif self.event == KEY_EVENT_SYNC:
            return self.sync_library

        else:
            print("Unknown UI library Event")

    @property
    def create_readme(self):
        self.app_name = self.out.split("/")[-1]
        create_readme_without_config(
            self.app_name, KEY_STACK_ANGULAR_UI_LIB
        )
        self.logger.add("Create Readme for Angular UI Library")
        return True

    @property
    def download(self):
        """
        Check if directory is an angular  project
        if angular project:
            if type === "angular-ui-lib":
                - download automation configuration
                - execute downloaded configuration

        :return:
        """

        self.print_logs.info("Downloading Angular UI library")
        self.module_name = ""
        if not self.app_name:
            self.app_name = take_user_input(
                {"app_name": "Input automation name require to download"}
            )["app_name"]

        self.logger.add("Downloading Angular UI library", app_name=self.app_name)
        automation_conf = self.api_calls.download_automation(self.app_name, self.type)["automation_conf"]
        automation_conf = add_module_to_downloaded_config(self.module_name, automation_conf)
        self.logger.add("Execute events for Angular UI library", automation_conf=automation_conf)
        if (self.user_info):
            token = self.user_info["token"]
        else:
            token = ""
        RuleEngine(
            app_name=self.app_name,
            app_type=self.type,
            logger=self.logger,
            token=token
        ).execute_events(automation_conf)
        self.logger.add("Angular UI Library Downloaded Successfully Angular UI library")
        message = "Declare html component to use library\n<app-{0}></app-{0}>".format(self.app_name)
        self.print_logs.success("Angular UI library Downloaded Successfully\n" + message + "\n")
        return True

    @property
    def upload(self):
        self.print_logs.success("Uploading Angular UI library ...")
        self.app_name = self.out.split("/")[-1]
        status = self.api_calls.validate_automation_api_call(KEY_STACK_ANGULAR_UI_LIB, self.app_name)
        self.logger.add("Uploading Angular UI library", app_name=self.app_name)
        if status:
            raise Exception("Library Already Exits")

        app_conf = get_basic_conf(
            app_name=self.app_name, type=self.type, stack="angular",
            api_call_obj=self.api_calls, default_inputs=None
        )
        self.logger.add("Created App configration", app_conf=app_conf)
        app_conf["automation_conf"] = self.build_angular_ui_module_automation_conf()
        self.logger.add("Created Events", automation_conf=app_conf["automation_conf"])
        response = self.api_calls.upload_automation(self.type, app_conf, False)
        write_json_file("jennie.conf.json", response)
        self.logger.add("Uploaded Library Events", response=response)
        self.print_logs.success("Angular UI library Uploaded Successfully")
        return True

    @property
    def update(self):
        self.print_logs.success("Uploading Angular UI library ...")
        self.app_name = self.out.split("/")[-1]
        status = self.api_calls.validate_automation_api_call(KEY_STACK_ANGULAR_UI_LIB, self.app_name)
        self.logger.add("Updating Angular UI library", app_name=self.app_name)
        if not status:
            raise Exception("Library Does not Exits")

        app_conf = get_basic_conf(
            app_name=self.app_name, type=self.type, stack="angular",
            api_call_obj=self.api_calls, default_inputs=read_json_file("jennie.conf.json")
        )
        app_conf["automation_conf"] = self.build_angular_ui_module_automation_conf(True)
        response = self.api_calls.upload_automation(self.type, app_conf, False)
        write_json_file("jennie.conf.json", response)
        self.logger.add("Updated Angular UI library", app_name=self.app_name)
        self.print_logs.success("Angular UI library Uploaded Successfully")
        return True

    @property
    def delete(self):
        if not self.app_name:
            self.app_name = take_user_input({"app_name": "Input application name require to delete"})["app_name"]

        choice = input("Are your sure you want to delete {} module from server? press C to cancel".format(self.app_name))
        if choice.lower() != "c":
            self.api_calls.delete_automation_api_call(self.type, self.app_name)
            self.print_logs.success("UI module deleted successfully")
            self.logger.add("Angular UI module deleted successfully", app_name=self.app_name)
        return True

    @property
    def sync_library(self):
        if not self.app_name:
            self.app_name = take_user_input({"app_name": "Input application name require to sync"})["app_name"]

        ui_library_conf = self.api_calls.download_automation(
            self.app_name, self.type
        )
        automation_conf = ui_library_conf["automation_conf"]
        RuleEngine(
            app_name=self.app_name,
            app_type=self.type,
            logger=self.logger,
            token=self.user_info["token"]
        ).execute_events(automation_conf)
        self.sync_library_files(ui_library_conf)
        self.logger.add("Angular UI module synced successfully", app_name=self.app_name, automation_conf=automation_conf)
        return True

    def build_angular_ui_module_automation_conf(self, is_update=False):
        """
        Upload CSS, HTML, TS file to server and build automation
        configuration for angular application.
        :return: automation_conf
        """
        if is_update:
            choice = input("Do you want to update automation configration (y/n)?")
            if choice.lower().replace(" ", "") != "y":
                return read_json_file("jennie.conf.json")["automation_conf"]

        automation_conf = []
        automation_conf.append(
            {
                KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_COMPONENT,
                KEY_COMPONENT_NAME: "ui-lib/" + self.app_name
            }
        )
        files = [
            self.app_name + ".component.css",
            self.app_name + ".component.ts",
            self.app_name + ".component.html",
        ]

        response = self.api_calls.upload_files(
            filepaths=files,
            app_name=self.app_name,
            type=self.type
        )
        automation_conf.append(
            {
                KEY_EVENT_TYPE: EVENT_DOWNLOAD_FILES,
                "files": [
                    {
                        KEY_FILE_LINK: response[0],
                        KEY_OUT_PATH: "src/app/ui-lib/{0}/{0}.component.css".format(self.app_name)
                    },
                    {
                        KEY_FILE_LINK: response[1],
                        KEY_OUT_PATH: "src/app/ui-lib/{0}/{0}.component.ts".format(self.app_name)
                    },
                    {
                        KEY_FILE_LINK: response[2],
                        KEY_OUT_PATH: "src/app/ui-lib/{0}/{0}.component.html".format(self.app_name)
                    }
                ]
            }
        )
        images = get_all_images(self.app_name + ".component.html")
        for key in images:
            image_path = os.getcwd().split("/src/")[0] + "/src/" + key
            response_images = self.api_calls.upload_image(image_path)
            automation_conf[1]["files"].append(
                {
                    KEY_FILE_LINK: response_images,
                    KEY_OUT_PATH: "src/" + key
                }
            )
        return automation_conf

    def sync_library_files(self, ui_library_conf):
        write_json_file(
            "src/app/ui-lib/{}/jennie.conf.json".format(ui_library_conf["app_name"]), ui_library_conf
        )

        if ui_library_conf["readme"] != "":
            readme_file_link = ui_library_conf["readme"]
            readme_file_path = "src/app/ui-lib/{}/readme.md".format(ui_library_conf["app_name"])

            file_content = self.api_calls.download_file(readme_file_link)
            open(readme_file_path, "w").write(file_content)

        if ui_library_conf["app_image"] != "":
            image_file_link = ui_library_conf["app_image"]
            image_file_path = "src/app/ui-lib/{}/{}".format(ui_library_conf["app_name"], image_file_link.split("/")[-1])
            download_image(image_file_path, image_file_link)

        return True