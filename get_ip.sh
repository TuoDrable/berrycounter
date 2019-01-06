#!/bin/sh
curl 'https://api.ipify.org?format=json' > /home/pi/rpi-sync/Berrycounter/current_ip.json
rclone sync /home/pi/rpi-sync/Berrycounter dropbox_brecht:Berrycounter/logging --config=/home/pi/.config/rclone/rclone.conf
