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

## 3. Install linux-modes-extra-raspi module:
- sudo apt install linux-modes-extra-raspi
