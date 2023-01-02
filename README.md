Python utility to configure RPi with freshly flashed SD card to work as an K3s node.

# Instructions for preparing the raspberry for K3s cluster:
Each of the following paragraphs is considered a phase in the setup process.
First one is extracted bacause it requires a reboot and additional handling of
reconnecting to the Raspberry module. Other ones are abstacted in a way that some
components can be removed (like K3s itself) and recreated using the tool.

## OS preparation phase
This phase prepares Ubuntu image and sets it to work with the K3s.

### 1. Prepare Ubuntu image in imager software:
This step is manual. Prepare SD card using Raspberry Pi Imager (v1.7.3 as of the moment of writing).
In the software pick:
- Ubuntu 32/64-bit version depending on the RPi model
    - using version 22.04 LTS
- In additional settings:
    - enable ssh
    - provide WLAN credentials if wireless connection is required
        - do not set WiFi credentials for modules that do not support wireless connection. There were problems connecting with wired connection on Raspberry Pi 2 if these were set.
- Set username and password. Recommendation is to default to some common password and change it after the setup.
- Write SD card

### 2. Modify firmware configuration files:
- /boot/firmware/config.txt -> append "add arm_64bit=1" in new line to the file
- /boot/firmware/cmdline.txt -> append "cgroup_memory=1 cgroup_enable=memory" to the only line in the file

### 3. Prepare config file and export its location:
TODO: Will be moved to another phase
It's empty at this point, its content will be copied over after K3s installation.
- mkdir ~/.kube
- touch ~/.kube/config

### 4. Set legacy IP tables
- sudo iptables -F
- sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
- sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy

### 5. Install linux-modes-extra-raspi module:
- sudo apt install linux-modes-extra-raspi
- reboot, the tool shall reconnect (still TODO)

## K3s configuration and download

## Rancher configuration and download
