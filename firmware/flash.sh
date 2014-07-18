#!/bin/bash

# Pass the firmware image file to be flashed as the first and only
# command line argument.
#
# The second curl call will time out, but it is expected. Once the
# script exits, you can unplug the ethernet cable and proceed to the
# next router, but do KEEP each router ON POWER until the new image is
# fully written! When flashing is done the router reboots
# automatically (as shown by all the leds flashing once).

export http_proxy=''
export https_proxy=''

curl \
--user admin:admin \
--user-agent 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0' \
--referer 'http://192.168.0.254/userRpm/SoftwareUpgradeRpm.htm' \
--form "Filename=@$1" -F 'Upgrade=Upgrade' \
http://192.168.0.254/incoming/Firmware.htm > /dev/null

sleep 10

curl \
--max-time 2 \
--user admin:admin \
--user-agent 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0' \
--referer 'http://192.168.0.254/incoming/Firmware.htm' \
http://192.168.0.254/userRpm/FirmwareUpdateTemp.htm >  /dev/null

