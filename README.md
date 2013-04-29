# Letras Viajeras

**Letras Viajeras** es una iniciativa de la [Dirección de Bibliotecas y 
Promoción de la Lectura del Gobierno de la Provincia de Buenos Aires](http://www.ic.gba.gov.ar/), 
que permitirá a los pasajeros de larga y media distancia tener acceso 
gratuito a libros digitales, con sus dispositivos móviles a través de 
una conexión Wi-fi que permitirá descargar libros y contenidos literarios 
seleccionados por la Dirección.

Los documentos, (libros, cuentos y revistas) son materiales del dominio 
público y/o con licencias libres.

![alt text](https://github.com/gcoop-libre/letras_viajeras/blob/master/data/muestra.png Ejemplo)

Letras Viajeras fue desarrollado íntegramente con Software Libre por la 
[Cooperativa de trabajo gcoop](http://gcoop.coop). La solución consiste en un Router Inalámbrico al que se le instala [OpenWRT](http://openwrt.org), un Firmware libre basado en el kernel Linux.


## Componentes

La solucíon comprende un generador de un sitio estatico HTML y la configuración de *OpenWRT* para que funcione en modo portal cautivo.

Para generar el sitio estático se utiliza el microframework 
[Flask](http://flask.pocoo.org), y la extensión [Frozen Flask](http://pythonhosted.org/Frozen-Flask/)

Para servir esos contenidos, se utiliza un Router **TP-Link mr3020** y el firmware [Open-WRT](http://openwrt.org).

La [guia de instalación](https://github.com/gcoop-libre/letras_viajeras/blob/master/GUIA_INSTALACION.md) está enfocada a usuarios con experiencia en sistemas **POSIX**, y conocimientos de networking.


