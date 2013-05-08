# Guia de Instalación
## Generar el sitio estatico

El sitio se construye a partir de un archivo csv llamado **"datos.csv"**
localizado dentro de **app/**. Se recomienda observar el formato de dicho archivo.

Consideramos que se tiene instalado en el sistema **python-distribute**
 
 * Crear un virtualenv e ingresar al mismo:
    
        virtualenv env
        . env/bin/activate

 * Instalar dependencias:
    
        pip install -r requirements.txt

 * Copiar los archivos a servir (los libros) dentro de **app/static/**
    
        cp /home/usuario/mis_libros/* static

 * Ejecutar el script freezer.py, dentro de **app/**:
    
        python freezer.py

 * Copiar el contenido de **app/build** en la raiz del pendrive

        cp -r app/build/* /media/mi_pendrive
    
## Instalar el firmware en un router mr3020

Para instalar el firmware necesitamos un servidor dhcp instalado en la red, y acceso a internet.

### Desde la nuestra máquina

Los scripts localizados dentro de **utils/** suponen que se utilizará el navegador *google-chrome*, en caso de no tenerlo instalado, se pueden modificar los scripts ip_fija e ip_fija2, para que utilizen otro browser.

 * Ingresar al directorio *utils/*
    
        cd utils/

 * Conectar el router a la alimentacion y esperar que termine de bootear
 * Con un cable de red desde nuestro *eth0*  al puerto del router ejecutar ``ip_fija``
    
        ./ip_fija

 * Se abrirá el navegador apuntando al sitio de administracion del router. 
 * Los datos solicitados son: usuario: *admin* pass: *admin*
 * En la ventana del browser, ir a System Tools > Firmware Update y cargar el firmware que esta en el directorio *firmware/* y darle al botón upgrade.
    
   ![alt text](https://raw.github.com/gcoop-libre/letras_viajeras/master/data/captura_tplink_1.png "Paso 1")
   ![alt text](https://raw.github.com/gcoop-libre/letras_viajeras/master/data/captura_tplink_2.png "Paso 2")
   ![alt text](https://raw.github.com/gcoop-libre/letras_viajeras/master/data/captura_tplink_3.png "Paso 3")
 

 * Esperar a que se actualize el Firmware
 * Correr el script ``ip_fija2``, nos cambia la ip y se abre luci (El sitio de administracion web de Open-WRT)
    
        ./ip_fija2

 * Crear la clave de root, con la que sea de nuestro agrado, presionar el botón **Save and Apply**
 
 * Cuando termine de guardar y aplicar los cambios, ejecutar el script ``copiar_por_ssh``, que modificará los archivos de configuracion.

        ./copiar_por_ssh

 * Desconectar el router de la alimentacion y conectarlo a la red con servidor DHCP, y nuestra computadora tambien.
 
 * Prender el router
 * Esperar a que termine de bootear y entrar por ssh, si tenemos **dnsmasq** en nuestra red, con hacer **ssh root@letraviajera** es suficiente, sino, en el servidor DHCP, tendremos que ver cual es la ip asignada al host **letraviajera**
    
        ssh root@letraviajera

### Dentro del filesystem del router

 
 * Reiniciar *dnsmasq*: (da un error porque no anda la wlan, pero igual reinicia)
    
        /etc/init.d/dnsmasq restart

 * Ir al home de root y ejecutar los siguientes scripts:
    
        cd /root
        sh instalar_paquetes.sh
        sh levantar_ws.sh
        sh config_fstab.sh

 * Entrar al archivo */etc/config/wireless* y reemplazar la linea **option macaddr ...** de *radio0* por la de *radio1*

        config wifi-device 'radio0'
                option type 'mac80211'
                option channel '11'
                option macaddr '64:70:02:41:79:dc' #<----- reemplazar esta linea
                option hwmode '11ng'
                option htmode 'HT20'
                list ht_capab 'SHORT-GI-20'
                list ht_capab 'SHORT-GI-40'
                list ht_capab 'RX-STBC1'
                list ht_capab 'DSSS_CCK-40'
                option disabled '0'
        config wifi-iface
                option device 'radio0'
                option mode 'ap'
                option ssid 'LetraViajera'
                option encryption 'none'
                option network 'lan'
        config wifi-device  radio1
                option type     mac80211
                option channel  11
                option macaddr  90:f6:52:c5:07:27 #<--- Por esta linea (la mac adress será distinta en tu AP)
                option hwmode   11ng
                option htmode   HT20
                list ht_capab   SHORT-GI-20
                list ht_capab
                SHORT-GI-40
                list ht_capab   RX-STBC1
                list ht_capab   DSSS_CCK-40
                # REMOVE THIS LINE TO ENABLE WIFI:
                option disabled 1
        config wifi-iface
                option device   radio1
                option network  lan
                option mode     ap
                option ssid     OpenWrt
   
    
 * Borrar desde **config wifi-device  radio1** hasta el fin de archivo (100 dd en vim), el archivo tiene que quedar asi (la macaddress será distinta):

        config wifi-device 'radio0'
                option type 'mac80211'
                option channel '11'
                option macaddr  90:f6:52:c5:07:27 
                option hwmode '11ng'
                option htmode 'HT20'
                list ht_capab 'SHORT-GI-20'
                list ht_capab 'SHORT-GI-40'
                list ht_capab 'RX-STBC1'
                list ht_capab 'DSSS_CCK-40'
                option disabled '0'
        config wifi-iface
                option device 'radio0'
                option mode 'ap'
                option ssid 'LetraViajera'
                option encryption 'none'
                option network 'lan'

 * Descomentar la linea comentada en ``/etc/config/dhcp``:

        config dnsmasq
            option domainneeded '1'
            option boguspriv '1'
            option filterwin2k '0'
            option localise_queries '1'
            option rebind_protection '1'
            option rebind_localhost '1'
            option local '/lan/'
            option domain 'lan'
            option expandhosts '1'
            option nonegcache '0'
            option authoritative '1'
            option readethers '1'
            option leasefile '/tmp/dhcp.leases'
            option resolvfile '/tmp/resolv.conf.auto'
            #list address '/#/10.0.0.1'     #<----- Descomenta esta linea

        config dhcp 'wan'
            option interface 'wan'
            option ignore '1'

        config dhcp
            option start '100'
            option leasetime '12h'
            option limit '150'
            option interface 'lan'

 * Enchufar el pendrive con el contenido generado, y reiniciar el router.

Una vez configurado, el router levanta un servidor dhcp en el wifi, y su ip es 10.0.0.1, para entrar por la **wan** usar el nombre de dominio *letraviajera*.
