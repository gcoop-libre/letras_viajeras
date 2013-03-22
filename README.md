# Biblio Mobile

Biblio mobile es una sitio estatico para distribuir libros

## Componentes

El hardware objetivo de este desarrollo es el mr3020 <link>

Se utiliza un sitio html estatico usando *Flask* y *Frozen Flask*


## Regenerar el sitio estatico

 * Instalar virtualenv e iniciar
 * Instalar dependencias en requirements.txt
 * Copiar los archivos a servir dentro de app/static/ 
 * Ejecutar el script freezer.py, dentro de app/
 * Copiar el contenido de app/build en la raiz del pendrive

## Flashear un app

Se utilizan los scripts provistos dentro de utils se supone que tiene instalado google-chrome, modificar los scripts ip_fija e ip_fija2 si es necesario

 * entrar al directorio (los paths son relativos)
 * Conectar el router a la alimentacion y esperar que termine de bootear
 * Con un cable de red desde nuestro *eth0*  al puerto del router ejecutar **ip_fija** 
 * En la ventana del browser, ir a System Tools > Firmware Update y cargar el firmware que esta en el directorio *firmware/* y darle a upgrade
 * Esperar a que se actualize el Firmware
 * Correr el script **ip_fija2**, nos cambia la ip y se abre luci
 * Cambiar la clave de root, los estamos dejando con **xx** darle a save and apply
 * cuando termina, ejecutar el script copiar_por_ssh
 * Desconectar el router de la alimentacion y conectarlo a la red de gcoop, y nuestra compu tambien
 * Prender el router
 * esperar a que arranque y entrar por ssh, como tenemos dnsmasq en nuestra red, con hacer "ssh root@letraviajera" es suficiente
 * entrar al archivo /etc/config/dhcp y comentar la linea que empieza con "list address "
 * reiniciar dnsmasq /etc/init.d/dnsmasq restart (da un error porque no anda la wlan, pero igual reinicia)
 * ir al home de root y ejecutar:
 * **sh instalar_paquetes.sh**
 * **sh levantar_ws.sh**
 * **sh config_fstab.sh** 
 * Entrar al archivo */etc/config/wireless* y reemplazar la linea **option macaddr ...** de *radio0* por la de *radio1*
 * Borrar desde **config wifi-device  radio1** hasta el fin de archivo (100 dd en vim)
 * descomentar la linea comentada en /etc/config/dhcp
 * reiniciar el router y voala!!!

Una vez configurado, el app sirve un dhcp en el wifi, y su ip es 10.0.0.1, para entrar por la wan usar el nombre de dominio *letraviajera*
 
 
 
