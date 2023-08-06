"""
event_name : create-reactjs-component
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
from jennie.utils.colorprinting import ColorPrinting
from jennie.constants.protocol import *
from jennie.constants.responses import *
from jennie.constants.inputmessage import *
from jennie.events.reactjs.create_react_js_component import create_react_js_component

class event_create_reactjs_component():
    def __init__(self, user_key, app_name, type):
        self.print_logs = ColorPrinting()
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_CREATE_REACTJS_COMPONENT,
            KEY_COMPONENT_NAME: "component_name"
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        Create React JS Compatible
        - Create Folder with (component name).lower().
        - Create Component JS files with sample Code. The JS file should contain exported class.
        - Create CSS File.
        :param event: event information, refer event_create_reactjs_component().sample_conf
        :return: True / False
        """
        for key in event_info[KEY_COMPONENT_NAME]:
            create_react_js_component(key)
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_CREATE_REACTJS_COMPONENT
        }
        name = input(INPUT_COMPONENT_NAME).replace(" ", "")
        if len(name) < 3:
            self.print_logs.error("Component name cannot be less than 3 characters")
            return self.build_event()

        if "," in name:
            event_info[KEY_COMPONENT_NAME] = name.split(",")
        else:
            event_info[KEY_COMPONENT_NAME] = [name]
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """

        if KEY_COMPONENT_NAME not in event_info:
            print(ERR_COMPONENT_NAMES_NOT_PRESENT)
            return False

        if str(type(event_info[KEY_FILES])) != "<class 'list'>":
            print(ERR_COMPONENT_NAMES_SHOULD_BE_LIST)
            return False

        return event_info

