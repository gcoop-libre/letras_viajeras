# Puntos a tener en cuenta

 *  Testing automático de equipos:
    - Levanta red Wireless "PromocionLecturaBA"
    - La conexion es existosa, entrega IP, gateway y dns
    - Se puede obtener la URl "http://promocionlecturaba/" y se obtiene el index
    - Para cualquier url, se redirecciona a esa URl
    - Al bootear se monta correctamente /dev/sda1 en /www (se infiere de 3)

 * Generación de Contenido
    - A partir de un excel, que guardamos en un csv
 
 * Estilo
    - Como va a ser el diseño?
    - imagenes de portada, iconos ?
 
 * Deployment
    - ¿Quien se encarga de comprar los equipos?
    - Plazos de entrega?
    - Tenemos que instalar los 45 equipos nosotros?
 
 * Montaje 
    - Como se instalan in situ? Velcro autoadhesivo? cinta bifaz?
  
 * Alimentacion
    - Voltaje de entrada? ¿Como convertimos las tensiones LM7805? 
    - Mandamos a hacer una plaquita con LM2596 para el step down?
    - ¿Cables µUSB-???? ? ¿quien los arma?


 * Armar sitio con acerca de (mostrar open wrt y refe de implementacion)
