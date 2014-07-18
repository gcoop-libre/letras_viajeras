/etc/init.d/uhttpd stop
/etc/init.d/uhttpd disable
opkg remove --force-removal-of-dependent-packages uhttpd
/etc/init.d/mini_httpd enable
/etc/init.d/mini_httpd start
