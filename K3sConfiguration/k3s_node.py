from ssh_controller import NodeSshController


class K3sNode:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        print("Connecting to target node.")
        self.ssh = NodeSshController()

    def overwrite_config_files(self):
        pass

    def install_required_modules(self):
        pass

    def __str__(self):
        return f"IP: {self.ip}, name: {self.name} - node"



class K3sControllerNode(K3sNode):
    def __init__(self, name, ip):
        super().__init__(name, ip)

    def __str__(self):
        return f"IP: {self.ip}, name: {self.name} - controller"