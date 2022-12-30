import paramiko
import datetime as dt


class NodeSshController:
    def __init__(self, ip, password = "rpi"):
        print("Initializing controller...")
        self.ip = ip
        self.password = password

        # SSH connection
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(ip, username="rpi", password=password)
        except paramiko.ssh_exception.NoValidConnectionsError:
            print(f"Could not connect to the host {self.ip}")
            self.ssh = None
            return

        session = self.ssh.get_transport().open_session()
        # Combine the streams to have errors printed on std.
        session.set_combine_stderr(True)
        # Request pseudo-terminal from the raspberry.
        # It is required to type back the password to enter sudo commands.
        session.get_pty()

    def sudo_command(self, command):
        pass

    def __del__(self):
        if self.ssh is None:
            return
        print(f"Deleting SSH controller. Closing connection to remote {self.ip}")
        self.ssh.close()
