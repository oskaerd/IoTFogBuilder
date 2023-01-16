    # TODO ranchr is not installed on rpi, this needs to be a separate class
    def helm_install_with_repositories(self):
        repo_commands = [
            "add rancher-latest https://releases.rancher.com/server-charts/latest",
            "add jetstack https://charts.jetstack.io",
            "update"
        ]
        print("\tInstalling helm and required repositories:", end='')
        streams = self.ssh.sudo_command("curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash")
        streams[1].readlines()

        for cmd in repo_commands:
            streams = self.ssh.command(f"helm repo {cmd}")
            streams[1].readlines()

        print(' Done.')

    def create_rancher_namespaces(self):
        rancher_namespaces = [
            "cattle-system",
            "cert-manager"
        ]

        print("\tCreating rancher namespaces.", end='')

        for ns in rancher_namespaces:
            streams = self.ssh.command(f"kubectl create namespace {ns}")
            streams[1].readlines()

        print(' Done')

    def install_cert_manager(self):
        commands = [
            "kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.2.0-alpha.2/cert-manager.crds.yaml",
            "helm install cert-manager jetstack/cert-manager --namespace cert-manager",
            "kubectl get pods --namespace cert-manager"
        ]
        print("\tInstalling cert manager:", end='')
        for cmd in commands:
            streams = self.ssh.command(cmd)
            result = streams[1].readlines()
        print(" Done.")