Python utility to configure RPi with freshly flashed SD card to work as an K3s node.

# Notes to the input JSON file:
1. The controller node should be listed as the first one so its key is known for the workers.
2. There should be no more than one controller in the JSON. Otherwise further controllers
will be used and the tool will end up creating more clusters depending on the order in the file.

# Instructions for preparing the raspberry for K3s cluster:
Each of the following paragraphs is considered a phase in the setup process.
First one is extracted bacause it requires a reboot and additional handling of
reconnecting to the Raspberry module. Other ones are abstacted in a way that some
components can be removed (like K3s itself) and recreated using the tool.

## OS preparation phase
This phase prepares Ubuntu image and sets it to work with the K3s.

### 0. Prepare Ubuntu image in imager software:
This step is manual. Prepare SD card using Raspberry Pi Imager (v1.7.3 as of the moment of writing).
In the software pick:
- Ubuntu 32/64-bit version depending on the RPi model
    - using version 22.04 LTS
- In additional settings:
    - enable ssh
    - provide WLAN credentials if wireless connection is required
        - do not set WiFi credentials for modules that do not support wireless connection. There were problems connecting with wired connection on Raspberry Pi 2 if these were set.
- Set username and password. Assumption is to default to some common password across the nodes and change it after the setup.
- Write SD card

### 1. Modify firmware configuration files:
- /boot/firmware/config.txt -> append "add arm_64bit=1" in new line to the file
- /boot/firmware/cmdline.txt -> append "cgroup_memory=1 cgroup_enable=memory" to the only line in the file

### 2. Set legacy IP tables
- sudo iptables -F
- sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
- sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy

### 3. Install linux-modes-extra-raspi module:
- sudo apt install linux-modes-extra-raspi
- reboot, the tool shall reconnect on its own

## K3s configuration and download phase
### 1. Prepare config directory and export its location:
- mkdir ~/.kube
- echo "export KUBECONFIG=/home/{username}/.kube/config" >> ~/.bashrc
### 2. Download and install K3s
1. 
    a.Controller:
        - curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="k3s-version-from-json" K3S_KUBECONFIG_MODE="644" sh -s -
        - get the node token from controller node:
            sudo cat /var/lib/rancher/k3s/server/node-token

    b. Worker:
        - curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="k3s-version-from-json" K3S_TOKEN="CONTROLLER_TOKEN" K3S_URL="https://[controller ip]:6443" K3S_NODE_NAME="some-node-name" sh -

K3s version is parametrized in the JSON and mandatory to provide. The format is version string as in the K3s repository:
https://github.com/k3s-io/k3s/releases
Example: v1.24.9+k3s1

### 3. Copy and modify the config file for controller IP:
- cp /etc/rancher/k3s/k3s.yaml /home/{username}/.kube/config
- sed the IP


## Installing Prometheus and Grafana from helm chart
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts\n
helm install prometheus prometheus-community/kube-prometheus-stack

