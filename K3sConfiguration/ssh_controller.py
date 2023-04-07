import paramiko
import datetime as dt
import time


class NodeSshController:
    def __init__(self, ip, username, password):
        print("Initializing SSH controller...")
        self.ip = ip
        self.password = password
        self.username = username
        self.status_ok = True

        # SSH connection
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh.connect(ip, username=username, password=password)
        except (paramiko.ssh_exception.NoValidConnectionsError, TimeoutError):
            print(f"\tWARNING: Could not connect to the host {self.ip} - will be skipped")
            self._ssh = None
            self.status_ok = False

    def get_connection_successful(self):
        return self.status_ok

    def sudo_command(self, command, bypass_sudo_password=False):
        stdin, stdout, stderr = self._ssh.exec_command(f"sudo {command}", get_pty=True)
        # Small delay for password prompt to appear:
        time.sleep(1)
        if not bypass_sudo_password:
            stdin.write(f"{self.password}\n")
            stdin.flush()

        # Blocking and waiting for command output so we know it has completed.
        result = stdout.readlines()

        return result

    def command(self, command):
        return self._ssh.exec_command(command)

    def reconnect(self, delay):
        # close the connection and give rpi some time for reboot. Then restore connection.
        self._ssh.close()
        time.sleep(delay)
        self._ssh.connect(self.ip, username=self.username, password=self.password)
        print("Reconnected")

    def __del__(self):
        if self._ssh is None:
            return
        print(f"Closing connection to remote {self.ip}")
        self._ssh.close()
