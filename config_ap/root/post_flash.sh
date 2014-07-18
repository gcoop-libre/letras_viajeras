#!/bin/sh

/etc/init.d/dnsmasq restart
cd /root /bin/sh instalar_paquetes.sh && /bin/sh levantar_ws.sh && /bin/sh config_fstab.sh && /bin/sh autoconfig.sh

