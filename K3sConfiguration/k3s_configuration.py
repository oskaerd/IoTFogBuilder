from .k3s_node import K3sNode
from .k3s_node_controller import K3sControllerNode


class K3sControllerFactory:
    def __init__(self, json_data):
        # Choose proper class:
        if json_data['is_controller']:
            print("Creating controller node.")
            k3s_class = K3sControllerNode
        else:
            print("Creating worker node.")
            k3s_class = K3sNode

        ip = json_data['ip']
        name = json_data['node_name']
        username = json_data['username']
        phases = json_data['phases']
        self.k3s = k3s_class(username, name, ip, phases)


    def get_node(self):
        return self.k3s




