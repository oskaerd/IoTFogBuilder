from .ssh_controller import NodeSshController
import time

class K3sNode:
    def __init__(self, username, node_name, ip):
        self.node_name = node_name
        self.ip = ip
        self.username = username
        self.connection_failed = False

        # SSH connection
        print(f"\tConnecting to target node {ip}")
        self.ssh = NodeSshController(ip)
        if self.ssh is None:
            self.connection_failed = True

    def overwrite_firmware_config_files(self, config_files_dir = '/boot/firmware'):
        print("\tAppending required flags to config files.")

        # check if flags have not been already set in the file:
        streams = self.ssh.command(f"grep \'add arm_64bit=1\' {config_files_dir}/config.txt")
        if streams[1].read().decode('utf-8') == '':
            self.ssh.command(f"cp {config_files_dir}/config.txt .")
            self.ssh.command("echo \'add arm_64bit=1\' | tee -a config.txt")
            streams = self.ssh.sudo_command(f"mv config.txt {config_files_dir}")
        else:
            print(f"\t{config_files_dir}/config.txt flags already present. Skipping.")
        # This read is needed for file to be moved.
        streams[1].read().decode('utf-8')

        # cmdline.txt
        streams = self.ssh.command(f"grep \"cgroup_enable=memory\" {config_files_dir}/cmdline.txt")
        # check if flags have not been already set in the file:
        if streams[1].read().decode('utf-8') == '':
            self.ssh.command(f"cp {config_files_dir}/cmdline.txt .")
            self.ssh.command("echo $(cat cmdline.txt) cgroup_memory=1 cgroup_enable=memory > cmdline.txt")
            streams = self.ssh.sudo_command(f"mv cmdline.txt {config_files_dir}")
        else:
            print(f"\t{config_files_dir}/cmdline.txt flags already present. Skipping.")
        # This read is needed for file to be moved.
        streams[1].read().decode('utf-8')

    def install_required_modules(self):
        print("\tInstalling missing Ubuntu packages for raspberry:")
        # Don't really need to check if these are already installed.
        # If so, the package will just get skipped so we're fine.

    def __str__(self):
        return f"IP: {self.ip}, name: {self.node_name} - node"



class K3sControllerNode(K3sNode):
    def __init__(self, username, node_name, ip):
        super().__init__(username, node_name, ip)

    def __str__(self):
        return f"IP: {self.ip}, name: {self.node_name} - controller"

    def get_master_key(self):
        pass