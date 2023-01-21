from .k3s_node import K3sNode


class K3sControllerNode(K3sNode):
    def __init__(self, username, node_name, ip, phases):
        super().__init__(username, node_name, ip, phases)

    def prepare_k3s_config_file(self):
        print("\tPreparing K3s config directory and files.")
        self.ssh.command("mkdir .kube")
        # Append export of K3s config path to the .bashrc file.
        self.ssh.command(f"echo \"export KUBECONFIG=/home/{self.username}/.kube/config\" >> ~/.bashrc")
        # Source to have the variable available in current session
        self.ssh.command("source ~/.bashrc")

    def install_k3s(self, k3s_version, controller_ip, controller_token):
        print('\tInstalling K3s on the controller node.')
        self.ssh.sudo_command(f"curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=\"{k3s_version}\" K3S_KUBECONFIG_MODE=\"644\" sh -s -")

    def write_final_k3s_config_file(self):
        print("\tCopying k3s.yaml to config directory and setting node's IP address.")
        self.ssh.command(f"cp /etc/rancher/k3s/k3s.yaml /home/{self.username}/.kube/config")

        # sed the localhost IP address (127.0.0.1) and replace with the controller IP
        self.ssh.command(f"sed -i -r \'s/(\\b[0-9]{{1,3}}\\.){{3}}[0-9]{{1,3}}\\b\'/{self.ip}/ /home/{self.username}/.kube/config")

    def get_controller_token(self, controller_token):
        controller_token = self.ssh.sudo_command("cat /var/lib/rancher/k3s/server/node-token")[-1][:-1]
        return controller_token

    def get_controller_ip(self):
        return self.ip

    def __str__(self):
        return f"IP: {self.ip}, name: {self.node_name} - controller"
