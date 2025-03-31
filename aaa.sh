sudo apt-get remove brltty

nmcli dev wifi list

sudo nmcli dev wifi connect "Tienthinhunifi2021" password "Internet2021"

sudo nmcli dev wifi connect "TTH_VANPHONG_ARCHER_50GHz" password "abcd1234"

sudo ip addr add 200.200.200.190/24 dev eth0

systemctl cat start.service

systemctl list-units --type=service --all

systemctl cat startup-commands.service

sudo apt install watchdog

systemctl daemon-reload

modbus_mqtt.service

start_reboot.service: modbus tcp
start_reboot_lear.service: lear reader

openjdk-11-jdk: java



sudo mount -t cifs //192.168.1.76/4l_db /mnt/pcshare -o username=lj20180821,password=44