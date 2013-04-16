# Letras Viajeras

Letras viajeras es un generador de un sitio **html** estatico para distribuir libros,
 utilizando routers wifi de bajo costo.

## Componentes

Para generar el sitio estático se utiliza el microframework **Flask**,
y la extensión **Frozen Flask**

Para servir esos contenidos, se utiliza un Router **TP-Link mr3020** y el firmware **Open-WRT**.

La guia de instalación está enfocada a usuarios con experiencia en sistemas **POSIX**, y conocimientos de networking.

## Generar el sitio estatico

El sitio se construye a partir de un archivo csv llamado **"datos.csv"**
localizado dentro de **app/**. Se recomienda observar el formato de dicho archivo.

Consideramos que se tiene instalado en el sistema **python-distribute**
 
 * Crear un virtualenv e ingresar al mismo.
 * Instalar dependencias utilizando **pip install -r requirements.txt**.
 * Copiar los archivos a servir (los libros) dentro de **app/static/**
 * Ejecutar el script freezer.py, dentro de **app/**
 * Copiar el contenido de **app/build** en la raiz del pendrive

## Instalar el firmware en un router mr3020

Para instalar el firmware necesitamos un servidor dhcp instalado en la red, y acceso a internet.

Los scripts localizados dentro de **utils/** suponen que se utilizará el navegador *google-chrome", en caso de no tenerlo instalado, se pueden modificar los scripts ip_fija e ip_fija2, para que utilizen otro browser.

 * Ingresar al directorio *utils/*
 * Conectar el router a la alimentacion y esperar que termine de bootear
 * Con un cable de red desde nuestro *eth0*  al puerto del router ejecutar **ip_fija**
 * Se abrirá el navegador apuntando al sitio de administracion del router. 
 * Los datos solicitados son: usuario: *admin* pass: *admin*
 * En la ventana del browser, ir a System Tools > Firmware Update y cargar el firmware que esta en el directorio *firmware/* y darle al botón upgrade.
 * Esperar a que se actualize el Firmware
 * Correr el script **ip_fija2**, nos cambia la ip y se abre luci (El sitio de administracion web de Open-WRT)
 * Crear la clave de root, con la que sea de nuestro agrado, presionar el botón **Save and Apply**
 * Cuando termine de guardar y aplicar los cambios, ejecutar el script **copiar_por_ssh**, que modificará los archivos de configuracion.

 * Desconectar el router de la alimentacion y conectarlo a la red con servidor DHCP, y nuestra computadora tambien.
 
 * Prender el router
 * Esperar a que termine de bootear y entrar por ssh, si tenemos **dnsmasq** en nuestra red, con hacer **ssh root@letraviajera** es suficiente, sino, en el servidor DHCP, tendremos que ver cual es la ip asignada al host **letraviajera**

Dentro del filesystem del router

 * Entrar al archivo /etc/config/dhcp y comentar la linea que empieza con "list address "
 * Reiniciar *dnsmasq*: **/etc/init.d/dnsmasq restart** (da un error porque no anda la wlan, pero igual reinicia)
 * Ir al home de root y ejecutar:
 * **sh instalar_paquetes.sh**
 * **sh levantar_ws.sh**
 * **sh config_fstab.sh** 
 * Entrar al archivo */etc/config/wireless* y reemplazar la linea **option macaddr ...** de *radio0* por la de *radio1*
 * Borrar desde **config wifi-device  radio1** hasta el fin de archivo (100 dd en vim)
 * Descomentar la linea comentada en /etc/config/dhcp
 * Enchufar el pendrive con el contenido generado, y reiniciar el router.

Una vez configurado, el router levanta un servidor dhcp en el wifi, y su ip es 10.0.0.1, para entrar por la wan usar el nombre de dominio *letraviajera*.
 
 
 
