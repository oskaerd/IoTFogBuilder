from .ssh_controller import NodeSshController


class K3sNode:
    def __init__(self, username, node_name, ip):
        self.node_name = node_name
        self.ip = ip
        self.username = username
        self.connection_failed = False

        # SSH connection
        print(f"Connecting to target node {ip}.")
        self.ssh = NodeSshController(ip)
        if self.ssh is None:
            self.connection_failed = True


    def overwrite_config_files(self):
        pass

    def install_required_modules(self):
        pass

    def __str__(self):
        return f"IP: {self.ip}, name: {self.node_name} - node"



class K3sControllerNode(K3sNode):
    def __init__(self, username, node_name, ip):
        super().__init__(username, node_name, ip)

    def __str__(self):
        return f"IP: {self.ip}, name: {self.node_name} - controller"

    def get_master_key(self):
        pass