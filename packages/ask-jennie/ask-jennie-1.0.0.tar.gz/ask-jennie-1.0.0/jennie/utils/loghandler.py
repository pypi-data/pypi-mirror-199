import json, inspect
from datetime import datetime

SEPARATOR = " :: "
class LogHandler():
    def __init__(self):
        self.logger_file = "jennie.automation.log"
        self.session_log = ""
        self.set_debug()

    def set_class(self, class_name):
        pass

    def set_debug(self, is_debug = False):
        self.is_debug = is_debug

    def add(self, msg, **kwargs):
        try:
            _stack = inspect.stack()
            fn_call_name = _stack[1][0].f_locals['self'].__class__.__name__ + "/" + _stack[1][3]
        except Exception as e:
            fn_call_name = ""

        current = str(datetime.now()) + SEPARATOR + fn_call_name + SEPARATOR + msg + SEPARATOR
        for key in kwargs:
            if (str(type(kwargs[key])) == "<class 'dict'>"):
                current += key + " = " + json.dumps(kwargs[key]) + ", "
            else:
                current += key + " = " + str(kwargs[key]) + ", "
        self.session_log += current[:-2] + "\n"
        return True

    def save_logs(self):
        if self.is_debug:
            print (self.session_log)
            # open(self.logger_file, "w").write(self.session_log)

