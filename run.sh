#!/bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install git -y

echo "remove folder if any"
sudo rm -r Tunneling
sudo rm -r Work
git clone https://github.com/HassanRehman11/Tunneling.git
mv Tunneling Work

cd Work

pip3 install flask -t .
sudo chmod 600 dahuatunnel.pem
sudo systemctl stop portal.service
sudo systemctl disable portal.service
sudo rm /etc/systemd/system/portal.service
sudo cp portal.service /etc/systemd/system/
sudo chmod 666 /etc/systemd/system/portal.service
sudo chmod +x /etc/systemd/system/portal.service


sudo systemctl daemon-reload
sudo systemctl enable portal.service
sudo systemctl start portal.service
echo "portal updated and service restarted."
sudo systemctl stop start_forwarding.service
sudo systemctl disable start_forwarding.service
sudo rm /etc/systemd/system/start_forwarding.service
sudo cp start_forwarding.service /etc/systemd/system/
sudo chmod 666 /etc/systemd/system/start_forwarding.service
sudo chmod +x /etc/systemd/system/start_forwarding.service

sudo systemctl daemon-reload
sudo systemctl enable start_forwarding.service
sudo systemctl start start_forwarding.service
echo "start forwarding updated and service restarted."

sudo rm /etc/ssh/sshd_config
sudo cp sshd_config /etc/ssh/
sudo chmod 666 /etc/systemd/system/start_forwarding.service
sudo chmod +x /etc/systemd/system/start_forwarding.service

sudo systemctl restart ssh
echo "sshd_config updated and SSH service restarted."
