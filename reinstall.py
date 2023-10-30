import sys
from K3sConfiguration import k3s_configurator

if len(sys.argv) < 3:
    print("Run as: main.py config-file rpi-password")
    sys.exit(1)

ips_to_repair = input("Input IPs to reinstall K3s on, separated by commas: ")
ips_to_repair = ips_to_repair.split(',')

print(ips_to_repair)

configurator = k3s_configurator.K3sRpiConfigurator(sys.argv[1], sys.argv[2])
token = configurator.nodes[0].get_controller_token(None)

for node in configurator.nodes[1:]:
    if node.ip in ips_to_repair:
        node.ssh.sudo_command("unagent")
        node.install_k3s(configurator.nodes[0].ip, token)


