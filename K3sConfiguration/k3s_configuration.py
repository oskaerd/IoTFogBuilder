from k3s_node import K3sControllerNode, K3sNode

class K3sControllerFactory:
    def __init__(self, json_data):
        if json_data['is_controller']:
            print("Creating controller node.")
            k3s_class = K3sControllerNode
        else:
            print("Creating worker node.")
            k3s_class = K3sNode

        ip = json_data['ip']
        name = json_data['name']
        self.k3s = k3s_class(name, ip)

    def get_node(self):
        return self.k3s




