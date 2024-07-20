sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-serial python3-rpi.gpio
sudo apt-get install ppp minicom

sudo apt-get update
sudo apt-get install minicom

sudo minicom -D /dev/ttyS0 -b 115200
