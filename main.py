import json
from K3sConfiguration import k3s_configuration as k3r


class K3sRpiConfigurator:
    def __init__(self, json_file):
        # Keep the nodes in a list:
        self.nodes = []

        # Get the configurations from the JSON file:
        with open(json_file) as jf:
            json_data = json.load(jf)

            for rpi_config in json_data['machines']:
                k3s = k3r.K3sControllerFactory(rpi_config).get_node()
                self.nodes.append(k3s)

    def configure_nodes(self):
        for node in self.nodes:
            print(node)


if __name__ == "__main__":
    configurator = K3sRpiConfigurator('rpis.json')


# test the connection
# now = str(dt.datetime.now())
# print(now.replace(' ', '-')[:now.find('.')])


# session.exec_command("sudo bash -c \"mkdir /etc/test\"")
# stdin = session.makefile("wb", -1)
# stdout = session.makefile("rb", -1)

# stdin.write(f"{password}\n")
# stdin.flush()
# print(stdout.read().decode("utf-8"))

# #stdin, stdout, stderr = ssh.exec_command(f"touch /etc/test/{}")

# # response = stdout.readlines()

# # for line in response:
# #     print(line)

# ssh.close()
