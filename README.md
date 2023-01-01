Python utility to configure RPi with freshly flashed SD card to work as an K3s node.

# Instructions for preparing the raspberry for K3s cluster:

## 1. Prepare Ubuntu image in imager software:
- Ubuntu 32/64-bit version depending on the RPi model
    - using version 22.04 LTS
- In additional settings:
    - enable ssh
    - provide WLAN credentials if desired
- Write SD card

## 2. Modify firmware configuration files:
- /boot/firmware/config.txt -> append "add arm_64bit=1" in new line to the file
- /boot/firmware/cmdline.txt -> append "cgroup_memory=1 cgroup_enable=memory" to the only line in the file

## 3. Prepare config file and export its location:
It's empty at this point, its content will be copied over after K3s installation.
- mkdir ~/.kube
- touch ~/.kube/config

## 4. Set legacy IP tables
- sudo iptables -F
- sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
- sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy

## 5. Install linux-modes-extra-raspi module:
- sudo apt install linux-modes-extra-raspi
- reboot, the tool shall reconnect (still TODO)
