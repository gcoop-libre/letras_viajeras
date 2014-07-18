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

MAC=$(ifconfig | egrep br-lan.*HWaddr | awk '{print $5}')
HOST=$(echo $MAC | tr -d ":")
WAN_HOST=$HOST
#IP=$(uci get network.lan.ipaddr)
IP=10.0.0.1
SSID=LetraViajera
RUN_UCI=0
COMMIT_UCI=0
REBOOT=0

delete()
{
  if [ -z $1 ]
  then
    return
  fi

  OP=$(uci get $1)
  OK=$(echo $?)

  if [ $OK -eq 0 ]
  then
    uci delete $1
  fi
}

usage()
{
cat << EOF

Use: autoconfig.sh [options]
Example: autoconfig.sh -i 10.0.0.1 -ucr -w LetraViajera'

Options:                                   Default:
            
    -h show help                           -
    -m set mac address                     $MAC
    -w set wan hostname                    $WAN_HOST
    -n set hostname                        $HOST
    -i set ip adress                       $IP
    -s set ssid                            $SSID
    -u run uci set/delete                  no set/delete
    -c commit changes                      no commit
    -r reboot after changes if no errors   no reboot
EOF
}

while getopts "hm:n:i:s:ucr" OPTION
do
  case $OPTION in
    h)
      usage
      exit 0
      ;;
    m)
      MAC=$OPTARG
      ;;
    n)
      HOST=$OPTARG
      ;;
    i)
      IP=$OPTARG
      ;;
    s)
      SSID=$OPTARG
      ;;
    u)
      RUN_UCI=1
      ;;
    c)
      COMMIT_UCI=1
      ;;
    r)
      REBOOT=1
      ;;
    *)
      usage
      exit 1
  esac
done

IP_BC=$(echo $IP | sed s/".1$"/".255"/g)
echo $(date '+%F %T') Parámetros a Aplicar MAC=$MAC HOST=$HOST WAN_HOST=$WAN_HOST IP=$IP IP_BC=$IP_BC SSID=$SSID

if [ $RUN_UCI -eq 1 ]
then

#MAC_1=$(uci get wireless.radio1.macaddr)

if [ -z $MAC ]
then
  echo "empty MAC, abort"
  exit 1
fi

if [ -z $HOST ]
then
  echo "empty HOST, abort"
  exit 1
fi

if [ -z $SSID ]
then
  echo "empty SSID, abort"
  exit 1
fi

if [ -z $IP ]
then
  echo "empty IP, abort"
  exit 1
fi

echo "
set system.@system[0].hostname=$HOST
set network.wan.hostname=$WAN_HOST
set network.lan.ipaddr=$IP
set wireless.radio0.disabled=0
set wireless.@wifi-iface[0].ssid=$SSID
set firewall.@redirect[0].src_ip=!$IP
set firewall.@redirect[0].dest_ip=$IP
set firewall.@redirect[1].src_ip=!$IP
set firewall.@redirect[1].dest_ip=$IP
set wireless.radio0.macaddr=$MAC
add_list dhcp.@dnsmasq[0].address='/#/$IP'
" | uci batch

UCI_OK=$(echo $?)

delete 'wireless.radio1.type'
delete 'wireless.radio1.channel'
delete 'wireless.radio1.macaddr'
delete 'wireless.radio1.hwmode'
delete 'wireless.radio1.htmode'
delete 'wireless.radio1.ht_capab'
delete 'wireless.radio1.disabled'
delete 'wireless.radio1=wifi-device'
delete 'wireless.@wifi-iface[1].device'

fi

if [ $COMMIT_UCI -eq 1 ]
then
  if [ $UCI_OK -eq 0 ]
  then
        echo "uci commit"
        uci commit
        COMMIT_OK=$(echo $?)

        if [ $COMMIT_OK -eq 0 ]
        then
          if [ $REBOOT -eq 1 ]
          then
            echo "reboot!..."
            reboot
          fi
        fi
  else
      echo "uci error, no commit"
  fi
else
  echo "no commit"
fi

echo $(date '+%F %T') Parámetros Aplicados MAC=$MAC HOST=$HOST WAN_HOST=$WAN_HOST IP=$IP IP_BC=$IP_BC SSID=$SSID

