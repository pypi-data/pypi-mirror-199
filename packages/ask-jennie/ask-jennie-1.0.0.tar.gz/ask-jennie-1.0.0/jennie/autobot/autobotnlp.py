import os
import time
import requests, webbrowser
from jennie.utils.colorprinting import ColorPrinting

class ASKJennie():
    def __init__(self, logger):
        self.logger = logger

    def ask(self, statement):
        self.create_search_entry(statement)

    def create_search_entry(self, statement):
        resp = requests.post("https://api.ask-jennie.com/v1/jennie/nlp/", json={
            "statement": statement
        })
        self.open_browser(resp.json()["payload"])
        self.keep_waiting(resp.json()["payload"])

    def open_browser(self, hash):
        webbrowser.open("https://automations.ask-jennie.com/automations/" + hash)

    def keep_waiting(self, hash):
        url = "https://api.ask-jennie.com/v1/jennie/nlp/?get_status=true&search_hash=" + hash
        time.sleep(2)
        resp = requests.get(url)
        if resp.status_code == 400:
            self.keep_waiting(hash)
        else:
            payload = resp.json()["payload"]
            if len(payload) > 0:
                print ("Continue to download automation .....")
                self.run_automation_conf(payload[0])
            else:
                self.keep_waiting(hash)

    def run_automation_conf(self, info):
        type_to_command = {
            "angular-ui-lib": "jennie angular ui-lib download ",
            "angular-automations": "jennie angular automations download ",
            "django-automations": "jennie django automations download ",
            "terraform-automations": "jennie terraform automations download ",
            "packer-automations": "jennie packer automations download ",
            "docker-automations": "jennie docker automations download ",
        }
        command = type_to_command[info["type"]] + info["app_name"]
        os.system("xdotool search --class gnome-terminal windowactivate --sync")
        ColorPrinting().info("Downloading Automation : " +  command)
        os.system(command)
