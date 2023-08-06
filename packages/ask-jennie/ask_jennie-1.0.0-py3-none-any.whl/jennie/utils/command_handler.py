from jennie.utils.helper import ask_to_select
from jennie.constants.protocol import *

AUTOMATION_COMMANDS = {
    "angular-automations": {
        "ui-lib": UI_LIB_EVENTS,
        "automations": AUTOMATION_EVENTS
    },
    "django": {
        "automations": AUTOMATION_EVENTS
    },
    "ubuntu": {
        "setup":  {
            "lemp": None,
            "phpmyadmin": None,
            "elk": None,
            "elasticsearch": None
        },
        "deploy": {
            "django": None,
            "web": None
        }
    },
    "logout": None,
    "version": None
}

def transverse_inside_commands(dictObj, current_command, commands):
    for key in dictObj:
        if str(type(dictObj[key])) == "<class 'dict'>":
            current_command = current_command + " " + key
            transverse_inside_commands(dictObj[key], current_command, commands)
        else:
            if dictObj[key] != None:
                append_command = current_command + " " + key + " <" + dictObj[key] + ">"
                commands.append(append_command)
            else:
                append_command = current_command + " " + key
                commands.append(append_command)
    return commands

def show_command_list(is_user_logger_in):
    if not is_user_logger_in:
        print ("Package is accessible only after login. To login use command"
               "\n\tjennie setup\nand login with email registered with ask jennie, "
               "To register continue to automations.ask-jennie.com/signup")

    else:
        current_command = "jennie"
        commands = []
        all_commands = transverse_inside_commands(AUTOMATION_COMMANDS, current_command, commands)
        counter = 1
        print ("\n\nList of commands available\n\n")
        for command in all_commands:
            print (str(counter) + ".", command)
            counter += 1
        print ("\n\n")
    return None, None

def map_inputs(arguments):
    args = arguments
    input_selected = AUTOMATION_COMMANDS
    commands = []
    for arg in args:
        if str(type(input_selected)) == "<class 'dict'>":
            if arg not in input_selected:
                print ("Invalid Command\n")
                return show_command_list(True)
            else:
                input_selected = input_selected[arg]
                commands.append(arg)

    while (str(type(input_selected)) == "<class 'dict'>"):
        print ("\n\n")
        input_selected, selected = ask_to_select(input_selected)
        commands.append(selected)

    if input_selected == "library_name" and len(args) > 3:
        commands.append(arguments[3])

    if len(args) > 4:
        for argument in args[4:]:
            commands.append(argument)
    return commands


class CommandHandler():
    def __init__(self, args):
        self.seprate_command_and_params(args)

    def seprate_command_and_params(self, args):
        self.other_params = []
        self.args = []
        for key in args:
            if "--" == key[:2] or len(self.args) > 3:
                self.other_params.append(key)
            else:
                self.args.append(key)

    @property
    def arrange(self):
        return map_inputs(self.args), self.other_params
