import os
import sys, traceback
from jennie.utils.exceptionhandler import ExceptionHanlder
from jennie.setup import Setup
from jennie.utils.colorprinting import ColorPrinting
from jennie.utils.logger import LogginMixin
from jennie.utils.loghandler import LogHandler
from jennie.utils.command_handler import map_inputs
from jennie.protocols import JennieProtocols
from jennie.autobot import AutoBot

def check_login_state(logger):
    setup_controller = Setup(logger)
    is_user_logger_in = False
    userinfo = setup_controller.get_logged_in_user()
    if userinfo != None:
        is_user_logger_in = True
    return userinfo, is_user_logger_in, setup_controller

def init_session():
    commands = sys.argv[1:]
    final_command_list = []
    logger = LogHandler()
    for command in commands:
        if command == "--v" or command == "--verbose":
            logger.set_debug(True)
        else:
            final_command_list.append(command)

    return logger, final_command_list

def perform_login(commands, setup_controller):
    SDKKEY = None
    if len(commands) > 1:
        SDKKEY = commands[1]
        if len(SDKKEY) != 35:
            ColorPrinting().error("Invalid SDK Key " + SDKKEY)
            return False
    return setup_controller.setup(SDKKEY)

def execute():
    try:
        if sys.argv[1] == "autobot":
            autobot()
    except Exception as e:
        pass
    logger, commands = init_session()
    userinfo, is_user_logger_in, setup_controller = check_login_state(logger)
    exception = None
    try:
        if is_user_logger_in:
            exception = ExceptionHanlder(userinfo["token"])
            if len(commands) > 0 and (commands[0] == "setup"):
                ColorPrinting().error("Already logged in, try using the software.")
                return False
            elif commands[0] == "version":
                return setup_controller.show_version()
            else:
                return JennieProtocols(commands, userinfo, logger).execute
        else:
            if commands[0] == "setup":
                return perform_login(commands, setup_controller)
            elif commands[0] == "version" or commands[0] == "-version":
                return setup_controller.show_version()
            else:
                print (os.getcwd())
                return JennieProtocols(commands, None, logger).execute
    except Exception as e:
        logger.set_debug(True)
        logger.save_logs()
        if exception !=None:
            exception.handle_error(e, traceback.format_exc(), commands)
        else:
            ColorPrinting().error(str(e))
        return False


def autobot():
    logger = LogHandler()
    AutoBot(logger).start()