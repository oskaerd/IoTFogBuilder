import json
from .k3s_controller_factory import K3sControllerFactory


class K3sRpiConfigurator:
    def __init__(self, json_file, password):
        # Keep the nodes in a list:
        self.nodes = []
        self.controller_token = None
        self.controller_ip = None

        # Get the configurations from the JSON file:
        with open(json_file) as jf:
            json_data = json.load(jf)
            self.k3s_install_version = json_data['k3s_version']

            for rpi_config in json_data['machines']:
                k3s = K3sControllerFactory(rpi_config, password).get_node()
                self.nodes.append(k3s)

    def configure_nodes(self):
        print("Begin configuration of the nodes:")
        for node in self.nodes:
            if node.did_connection_fail():
                print(f"Skipping node {node.ip} due to failed SSH connection.")
                continue

            print(f"\tStarting configuration of node {node.node_name}:{node.ip}")
            # Phase 1: OS preparation phase - installing required modules
            #          and applying settings.
            if node.check_if_running_current_phase(1):
                node.install_required_modules()

            # Phase 2: K3s configuration file and download
            if node.check_if_running_current_phase(2):
                node.prepare_k3s_config_file()
                node.install_k3s(self.k3s_install_version, self.controller_ip, self.controller_token)
                node.write_final_k3s_config_file()
                # Get the token and IP from the controller to pass it to the nodes:
                if self.controller_token is None:
                    self.controller_token = node.get_controller_token(None)
                    self.controller_ip = node.get_controller_ip()
            # Phase 3: Copying aliases file to nodes: 
            if node.check_if_running_current_phase(3):
                node.send_and_source_aliases()

            # Phase 4: Install helm on controller node and send deployment files
            if node.check_if_running_current_phase(4):
                #node.helm_install()
                node.send_deployment_files()

            print(f"\tFinished configuration of node {node.node_name}:{node.ip}")
        print("Finished configuration of all the nodes from the JSON file that were connected.")
