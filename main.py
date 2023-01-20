import json
from K3sConfiguration import k3s_configuration as k3r


class K3sRpiConfigurator:
    def __init__(self, json_file):
        # Keep the nodes in a list:
        self.nodes = []
        self.controller_key = None

        # Get the configurations from the JSON file:
        with open(json_file) as jf:
            json_data = json.load(jf)
            self.k3s_install_version = json_data['k3s_version']

            for rpi_config in json_data['machines']:
                k3s = k3r.K3sControllerFactory(rpi_config).get_node()
                self.nodes.append(k3s)

    def configure_nodes(self):
        print("Begin configuration of the nodes:")
        # TODO implement rest of the nodes
        for node in [self.nodes[0]]:
            if node.did_connection_fail():
                continue

            print(f"\tStarting configuration of node {node.node_name}:{node.ip}")
            # Phase 1: OS preparation phase - installing required modules
            #          and applying settings.
            if node.check_if_running_current_phase(1):
                # node.overwrite_firmware_config_files()
                # node.set_ip_tables()
                # node.install_required_modules()
                pass

            # Phase 2: K3s configuration file and download
            if node.check_if_running_current_phase(2):
                # node.prepare_k3s_config_file()
                # node.install_k3s(self.k3s_install_version)
                # node.write_final_k3s_config_file()
                # Get the token from the controller or pass it to the node:
                if self.controller_key is None:
                    self.controller_key = node.get_controller_key(None)
                    print(self.controller_key)
                else:
                    node.get_controller_key(self.controller_key)
                
            print(f"\tFinished configuration of node {node.node_name}:{node.ip}")
        print("Finished configuration of all the nodes from the JSON file that were connected.")


if __name__ == "__main__":
    configurator = K3sRpiConfigurator('rpis.json')
    configurator.configure_nodes()
