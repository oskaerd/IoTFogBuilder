from .ssh_controller import NodeSshController


class K3sNode:
    def __init__(self, username, node_name, ip):
        self.node_name = node_name
        self.ip = ip
        self.username = username
        self.connection_failed = False

        # SSH connection
        print(f"\tConnecting to target node {ip}.")
        self.ssh = NodeSshController(ip)
        if self.ssh is None:
            self.connection_failed = True

    def overwrite_config_files(self):
        print("\tAppending required flags to config files.")

    def install_required_modules(self):
        print("\tInstalling missing Ubuntu packages for raspberry:")

    def __str__(self):
        return f"IP: {self.ip}, name: {self.node_name} - node"



class K3sControllerNode(K3sNode):
    def __init__(self, username, node_name, ip):
        super().__init__(username, node_name, ip)

    def __str__(self):
        return f"IP: {self.ip}, name: {self.node_name} - controller"

    def get_master_key(self):
        pass