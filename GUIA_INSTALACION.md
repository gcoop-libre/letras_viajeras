# Guia de Instalación
## Generar el sitio estatico

El sitio se construye a partir de un archivo csv llamado **"datos.csv"**
localizado dentro de **app/**. Se recomienda observar el formato de
dicho archivo.

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

Para instalar el firmware necesitamos un servidor dhcp instalado en la
red, y acceso a internet.

### Desde la nuestra máquina

Los scripts localizados dentro de **utils/** suponen que se utilizará el
navegador *firefox*, en caso de no tenerlo instalado, se pueden
modificar los scripts ip_fija e ip_fija2, para que utilizen otro
browser.

 * Ingresar al directorio *utils/*

        cd utils/

 * Conectar el router a la alimentacion y esperar que termine de bootear
 * Con un cable de red desde nuestro *eth0*  al puerto del router
   ejecutar ``ip_fija``

        ./ip_fija

 * Se abrirá el navegador apuntando al sitio de administracion del
   router.
 * Los datos solicitados son: usuario: *admin* pass: *admin*
 * En la ventana del browser, ir a System Tools > Firmware Update y
   cargar el firmware que esta en el directorio *firmware/* y darle al
   botón upgrade.

   ![alt text](https://raw.github.com/gcoop-libre/letras_viajeras/master/data/captura_tplink_1.png "Paso 1")
   ![alt text](https://raw.github.com/gcoop-libre/letras_viajeras/master/data/captura_tplink_2.png "Paso 2")
   ![alt text](https://raw.github.com/gcoop-libre/letras_viajeras/master/data/captura_tplink_3.png "Paso 3")


 * Esperar a que se actualize el Firmware
 * Configurar una IP fija

    ifconfig eth0 192.168.1.2 up

 * Verificar la conexión

    ping 192.168.1.1 -c3

 * Establecer contraseña y habilitar SSH

    telnet 192.168.1.1
    passwd
    exit

 * Cuando termine de guardar y aplicar los cambios, ejecutar el script
   ``copiar_por_ssh``, que modificará los archivos de configuración.

        ./copiar_por_ssh

 * Desconectar el router de la alimentación y conectarlo a la red con
   servidor DHCP, y nuestra computadora también.

 * Prender el router

 * Esperar a que termine de bootear y entrar por ssh, si tenemos
   **dnsmasq** en nuestra red, con hacer **ssh root@letraviajera** es
   suficiente, sino, en el servidor DHCP, tendremos que ver cual es la
   ip asignada al host **letraviajera**

        ssh root@letraviajera

### Dentro del filesystem del router


 * Reiniciar *dnsmasq*: (da un error porque no anda la wlan, pero igual
   reinicia)

        /etc/init.d/dnsmasq restart

 * Ir al home de root y ejecutar los siguientes scripts:

        cd /root
        sh instalar_paquetes.sh
        sh levantar_ws.sh
        sh config_fstab.sh

 * Configurar opciones del sistema ``system``, la red ``network``,
   la red inalámbrica ``wireless``, de seguridad ``firewall`` y del
   servicio de entrega de direcciones IPs ``dhcp``

        sh autoconfig.sh -ucr

   De esta manera se autoconfigura por defecto los siguientes valores:

        Use: autoconfig.sh [options]
        Example: autoconfig.sh -i 10.0.0.1 -u -c -r

        Options:

            -h show help
            -m set mac address, default C0:4A:00:3E:AC:A2
            -n set hostname, default current mac address C04A003EACA2
            -i set ip adress, default 10.0.0.1
            -s set ssid, default LetraViajera
            -u run uci set/delete, default no set/delete
            -c commit changes, default no commit
            -r reboot after changes if no errors

 * Enchufar el pendrive con el contenido generado, y reiniciar el router.

Una vez configurado, el router levanta un servidor dhcp en el wifi, y su
ip es 10.0.0.1, para entrar por la **wan** usar el nombre de dominio
*letraviajera*.


### Accediendo sin contraseña

Es posible simplificar la conexión al router definiendo un Alias en el
archivo ``~/.ssh/config``

           Host Letra
               User root
               Hostname LetraViajera
               UserKnownHostsFile /dev/null
               StrictHostKeyChecking no
               IdentityFile ~/.ssh/gcoop_rsa

La última opción ``IdentityFile`` corresponde a la llave que previamente
se copió en el router en ``/etc/dropbear/authorized_keys``

De esta manera se pueden ejecutar comandos en remoto, por ejemplo:

    ssh Letra 'sh /root/autoconfig.sh -ucr'


### Configurando varios routers

Existe un script que realiza todos los pasos luego del primer flash del
firmware OpenWRT:

    ssh Letra '/bin/sh /root/post_flash.sh'

La salida del log es similar a la siguiente:

    2014-07-18 18:17:30 Parámetros a Aplicar MAC=C0:4A:00:44:7C:C0
    HOST=C04A00447CC0 WAN_HOST=C04A00447CC0 IP=10.0.0.1 IP_BC=10.0.0.255
    SSID=LetraViajera
    uci commit
    reboot!...
    2014-07-18 18:17:30 Parámetros Aplicados MAC=C0:4A:00:44:7C:C0
    HOST=C04A00447CC0 WAN_HOST=C04A00447CC0 IP=10.0.0.1 IP_BC=10.0.0.255
    SSID=LetraViajera

Una vez realizado este paso, el router reinicia y en 1minuto vuelve a
estar operativo, pero su hostname pasa a ser su macaddress, es útil para
trabajar con varios equipos conectados en la misma red. En estos casos
es conveniente agregar un alias en el archivo ``~/.ssh/config``

    Host C04A00*
        User root
        UserKnownHostsFile /dev/null
        StrictHostKeyChecking no
        IdentityFile ~/.ssh/gcoop_rsa

Contando con esta configuración podemos acceder al equipo utilizando la
mac adress como hostname:

    sleep 1m && ssh C04A00447CC0 uptime

De esta manera deberíamos acceder al router sin contraseña y verificar
su uptime, nos confirma que pudo reiniciar sin problemas luego de los
cambios aplicados.


### Failsafe

En ocasiones, los cambios aplicados pueden corromper el sistema y el
router no inicia correctamente, para subsanar este inconveniente, se
puede iniciar en modo ``failsafe``, para esto es necesario presionar el
botón ``RESET`` varias veces, mientras está iniciando el router, en un
par de segundos el led WPS titilará muy rápido, eso indica que podemos
ingresar manualmente y eliminar las configuraciones aplicadas:

      sudo ifconfig eth0 192.168.1.1
      telnet 192.168.1.1
      mount_root
      rm -r /overlay/*
      reboot -f

Luego podemos ingresar por ssh a la ip: 192.168.1.1 y volver aplicar los
cambios necesarios, en modo failsafe se puede cambiar la contraseña de
root si la olvidaste.

