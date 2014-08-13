#!/bin/sh

# This script comes with ABSOLUTELY NO WARRANTY, use at own risk
# Copyright (C) 2014 Osiris Alejandro Gomez <osiris@gcoop.coop>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

LAN_IP=$(uci show network.lan.ipaddr)
SYS_HOST=$(uci show system | grep hostname)
WAN_HOST=$(uci show network.wan.hostname | cut -d= -f2)
WAN_IP=$(ifconfig eth0 | grep "inet addr")
SRV_IP=192.168.10.180

log()
{
	echo $WAN_HOST $1
}

log_error()
{
	echo $WAN_HOST $1
	exit 1
}

process_running()
{
	PID=$(pidof $1)
	OK=$(echo $?)
	if [ $OK -eq 0 ]
	then
		log_error 'ERROR '$1' running '$PID
	fi
}

cd /www
FILES=$(wc -l index.md5 | awk '{print $1}')
FILES_OK=$(md5sum -c index.md5 | grep ": OK" | wc -l | awk '{print $1}')
OK=$(echo $?)
cd /

if [ $FILES -eq $FILES_OK ]
then
	log 'MD5 OK'
	process_running 'wget'
	process_running 'tar'
	exit 0
else
	log 'ERROR MD5'
fi

process_running 'wget'
process_running 'tar'

PID=$(pidof mini_httpd)
OK=$(echo $?)

if [ $OK -eq 0 ]
then
	/etc/init.d/mini_httpd stop
fi

PS=$(ps | grep sda1)
OK=$(echo $?)

if [ $OK -eq 0 ]
then
	umount /www
fi

MOUNT=$(mount /dev/sda1 /www)
OK=$(echo $?)

if [ $OK -ne 0 ]
then
	log_error 'ERROR mount sda1 1'
fi

MOUNT=$(mount | grep sda1)
OK=$(echo $?)

if [ $OK -ne 0 ]
then
	log_error 'ERROR mount sda1 2'
fi

cd /www
OK=$(echo $?)

if [ $OK -ne 0 ]
then
	log_error 'ERROR www'
fi

TOUCH=$(touch test_rw)
OK=$(echo $?)

if [ $OK -ne 0 ]
then
	log_error 'ERROR touch'
else
	rm test_rw
fi

echo 'WGET...'
wget -q -c -O - http://$SRV_IP/letras-viajeras.tar.gz | tar xzf - &

