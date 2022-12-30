import paramiko
import datetime as dt


class NodeSshController:
    def __init__(self, password = "rpi"):
        print("Initializing controller...")
        self.password = password

    def sudo_command(self, command):
        pass
