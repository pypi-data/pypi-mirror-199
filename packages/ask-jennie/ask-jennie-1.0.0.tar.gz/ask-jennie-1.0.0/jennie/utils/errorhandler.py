class RaiseError():
    def know_errors(self):
        return ["Automation name cannot be less than 2 characters"]
    def invalid_automation_config(self, name):
        raise ValueError("There is some error in Automation configration for {}"
            "\ncontact dextrop@ask-jennie.com for support".format(name)
        )

    def invalid_automation_app_name(self, name):
        raise ValueError("Automation name cannot be less than 2 characters")