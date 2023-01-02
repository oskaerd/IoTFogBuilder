from .ssh_controller import NodeSshController
import time
from abc import ABC, abstractmethod





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

        # filename, check for, modify command:
        file_tuples = [
            # /boot/firmware/config.txt
            ("config.txt", 'add arm_64bit=1', "echo \'add arm_64bit=1\' | tee -a config.txt"),
            # /boot/firmware/cmdline.txt
            ("cmdline.txt", "cgroup_enable=memory", "echo $(cat cmdline.txt) cgroup_memory=1 cgroup_enable=memory > cmdline.txt")
        ]

        for file_tuple in file_tuples:
            print(f"\tModifying {config_files_dir}/{file_tuple[0]}")
            # check if flags have not been already set in the file:
            streams = self.ssh.command(f"grep \'{file_tuple[1]}\' {config_files_dir}/{file_tuple[0]}")
            if streams[1].read().decode('utf-8') == '':
                self.ssh.command(f"cp {config_files_dir}/{file_tuple[0]} .")
                self.ssh.command(f"{file_tuple[2]}")
                streams = self.ssh.sudo_command(f"mv {file_tuple[0]} {config_files_dir}")
                # This read is needed for file to be moved.
                streams[1].read().decode('utf-8')
            else:
                print(f"Flags already present. Skipping.")

    def prepare_k3s_config_file(self):
        # Not applicable for the worker node.
        pass

    def set_ip_tables(self):
        print("\tConfiguring legacy IP tables.")
        self.ssh.sudo_command("iptables -F")
        self.ssh.sudo_command("update-alternatives --set iptables /usr/sbin/iptables-legacy")
        self.ssh.sudo_command("update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy")

    def install_required_modules(self, verbose = True):
        print("\tInstalling missing Ubuntu kernel packages for raspberry (takes up to 10 minutes).")
        # Don't really need to check if these are already installed.
        # If so, the package will just get skipped so we're fine.
        # -y to skip prompt if one wants to install the package
        # Takes some noticable time (~6 minutes) to complete.
        streams = self.ssh.sudo_command("apt install -y linux-modules-extra-raspi")

        time.sleep(8 * 60)
        streams[0].write("\n")
        streams[0].flush()

        # Blocking until the command is completed
        for line in streams[1].readlines():
            if verbose:
                print(line)
        # while True:
        #     print(streams[1].read())
        #     if streams[1].channel.exit_status_ready():
        #         break

    def reboot_and_reconnect(self):
        # self.ssh.sudo_command("reboot")
        # TODO how to reconnect?
        pass

    def get_controller_key(self):
        # TODO: This needs to reach out to K3sRpiConfigurator to get the controller key
        pass

    def __str__(self):
        return f"IP: {self.ip}, name: {self.node_name} - node"



class K3sControllerNode(K3sNode):
    def __init__(self, username, node_name, ip):
        super().__init__(username, node_name, ip)

    def prepare_k3s_config_file(self):
        print("\tPreparing K3s config directory and file.")
        self.ssh.command("mkdir .kube")
        self.ssh.command("touch .kube/config")
        # Append export of K3s config path to the .bashrc file.
        self.ssh.command(f"echo \"export KUBECONFIG=/home/{self.username}/.kube/config\" >> ~/.bashrc")

    def __str__(self):
        return f"IP: {self.ip}, name: {self.node_name} - controller"

    def get_controller_key(self):
        pass