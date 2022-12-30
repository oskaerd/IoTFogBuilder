import paramiko
import datetime as dt


class NodeSshController:
    def __init__(self, ip, password = "rpi"):
        print("Initializing SSH controller...")
        self.ip = ip
        self.password = password

        # SSH connection
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(ip, username="rpi", password=password)
        except paramiko.ssh_exception.NoValidConnectionsError:
            print(f"\tCould not connect to the host {self.ip}")
            self.ssh = None
            return

        self.session = self.ssh.get_transport().open_session()
        # Combine the streams to have errors printed on std.
        self.session.set_combine_stderr(True)
        # Request pseudo-terminal from the raspberry.
        # It is required to type back the password to enter sudo commands.
        self.session.get_pty()

    def sudo_command(self, command):
        self.session.exec_command(f"sudo bash -c \"{command}\"")
        stdin = self.session.makefile("wb", -1)
        stdout = self.session.makefile("rb", -1)

        # TODO check if promped for password
        print(stdout.read())
        stdin.write(f"{self.password}\n")
        stdin.flush()
        print(stdout.read().decode("utf-8"))

    def __del__(self):
        if self.ssh is None:
            return
        print(f"Closing connection to remote {self.ip}")
        self.ssh.close()
