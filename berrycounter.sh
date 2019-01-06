#!/bin/sh

start() {
  echo "Starting!"
  cd /home/pi
  rclone sync dropbox_brecht:Berrycounter/logging /home/pi/rpi-sync/Berrycounter  --config=/home/pi/.config/rclone/rclone.conf
  cd berrycounter
  git pull
  start-stop-daemon --background --start --exec '/usr/bin/python3' \
    --make-pidfile --pidfile /home/pi/django.pid -- /home/pi/berrycounter/berrycounter/manage.py runserver  0.0.0.0:8000
  start-stop-daemon --background --start --exec '/usr/bin/python3' \
    --make-pidfile --pidfile /home/pi/pulsecounter.pid -- /home/pi/berrycounter/berrycounter/count_pulses.py

}

stop() {
    start-stop-daemon --stop --exec "/usr/bin/python3" \
    --pidfile /home/pi/django.pid
    start-stop-daemon --stop --exec "/usr/bin/python3" \
    --pidfile /home/pi/pulsecounter.pid

  echo "stopped!!"
}

case $1 in
  start|stop) "$1" ;;
esac

