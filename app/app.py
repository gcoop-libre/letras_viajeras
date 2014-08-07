#! -*- coding: utf8 -*-
import csv
from flask import Flask, render_template, url_for
from flask.ext.bootstrap import Bootstrap

SECRET_KEY = 'alskdjalksdjalskdjaslkdjasldjaslkdjasdlkasd,mc,mxcnvm,xncv,sdkas'
BOOTSTRAP_JQUERY_VERSION = None

app = Flask(__name__)
app.config.from_object(__name__)

Bootstrap(app)

def obtener_filtros(categoria):
    filtros = {
        'cuentos' : [
            ( url_for('cuentos'), 'Todos'),
            ( url_for('cuentos_por_autor'), 'Por Autor'),
            ( url_for('cuentos_por_titulo'), 'Por Titulo'),
            ],
        'libros' : [
            ( url_for('libros'), 'Todos'),
            ( url_for('libros_por_autor'), 'Por Autor'),
            ( url_for('libros_por_titulo'), 'Por Titulo'),
            ],
        'revistas' : [
            ( url_for('revistas'), 'Todos'),
            ( url_for('revistas_por_nombre'), 'Por Nombre'),
            ],
        };
    return filtros.get(categoria, None)


def full_name(apellido, nombre):
    if nombre:
        return "%s, %s" % (apellido, nombre)
    else:
        return apellido

def filtrar_csv_por_categoria(categoria):
    """filtra el csv por la cuarta columna, categoria"""

    return filtrar_csv(lambda fila: fila[3] == categoria)

def filtrar_csv_por_categoria_y_autor(categoria, autor):
    """filtra el csv por la cuarta columna, categoria y la segunda"""

    return filtrar_csv(lambda fila: fila[3] == categoria and full_name(fila[0], fila[1]) == autor)

def filtrar_csv(funcion):
    """Filtra el csv usando una funcion"""

    with open('datos.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for fila in reader:
            fila = [a.decode('utf8') for a in fila]

            try:
              apellido, nombre, titulo, tipo, pdf, imagen = fila
            except ValueError:
              print fila

            if funcion(fila):
                yield (titulo, full_name(apellido, nombre), pdf, imagen)

def obtener_autores_categoria(categoria):
    datos = filtrar_csv_por_categoria(categoria)
    metodo = '%ss_de_autor' % categoria
    autores = set([(nombre, url_for(metodo, autor=nombre)) for _, nombre, _, _ in datos])
    return sorted(list(autores))

def obtener_titulos_categoria(categoria):
    datos = filtrar_csv_por_categoria(categoria)
    titulos = set([(u"%s - %s" % (titulo, nombre), url_for('static', filename=pdf)) for titulo, nombre, pdf, _ in datos])
    return sorted(list(titulos))

@app.route('/')
def index():
    return render_template('index.html', active_page='Inicio')

@app.route('/libros/')
def libros():
    datos = filtrar_csv_por_categoria('libro')
    return render_template(
            'catalogo.html',
            active_page='Libros',
            datos=datos,
            filtros=obtener_filtros('libros'),
            filtro_activo = 'Todos',
            )

@app.route('/libros/por_autor/')
def libros_por_autor():
    datos = obtener_autores_categoria('libro')
    return render_template(
            'lista.html',
            active_page='Libros',
            datos=datos,
            filtros=obtener_filtros('libros'),
            filtro_activo = 'Por Autor',
            )

@app.route('/libros/autor/<string:autor>/')
def libros_de_autor(autor):
    datos = filtrar_csv_por_categoria_y_autor('libro', autor)
    return render_template(
            'catalogo.html',
            active_page='Libros',
            datos=datos,
            filtros=obtener_filtros('libros'),
            filtro_activo = 'Por Autor',
            )

@app.route('/libros/por_titulo/')
def libros_por_titulo():
    datos = obtener_titulos_categoria('libro')
    return render_template(
            'lista.html',
            active_page='Libros',
            datos=datos,
            filtros=obtener_filtros('libros'),
            filtro_activo = 'Por Titulo',
            )

@app.route('/cuentos/')
def cuentos():
    datos = filtrar_csv_por_categoria('cuento')
    return render_template(
            'catalogo.html',
            active_page='Cuentos',
            datos=datos,
            filtros=obtener_filtros('cuentos'),
            filtro_activo = 'Todos',
            )

@app.route('/cuentos/por_autor/')
def cuentos_por_autor():
    datos = obtener_autores_categoria('cuento')
    return render_template(
            'lista.html',
            active_page='Cuentos',
            datos=datos,
            filtros=obtener_filtros('cuentos'),
            filtro_activo = 'Por Autor',
            )

@app.route('/cuentos/por_titulo/')
def cuentos_por_titulo():
    datos = obtener_titulos_categoria('cuento')
    return render_template(
            'lista.html',
            active_page='Cuentos',
            datos=datos,
            filtros=obtener_filtros('cuentos'),
            filtro_activo = 'Por Titulo',
            )

@app.route('/cuentos/autor/<string:autor>/')
def cuentos_de_autor(autor):
    datos = filtrar_csv_por_categoria_y_autor('cuento', autor)
    return render_template(
            'catalogo.html',
            active_page='Cuentos',
            datos=datos,
            filtros=obtener_filtros('cuentos'),
            filtro_activo = 'Por Autor',
            )



@app.route('/revistas/')
def revistas():
    datos = filtrar_csv_por_categoria('revista')
    return render_template(
            'catalogo.html',
            active_page='Revistas',
            datos=datos,
            filtros=obtener_filtros('revistas'),
            filtro_activo = 'Todos',
            )


@app.route('/revistas/por_nombre/')
def revistas_por_nombre():
    datos = obtener_titulos_categoria('revista')
    return render_template(
            'lista.html',
            active_page='Revistas',
            datos=datos,
            filtros=obtener_filtros('revistas'),
            filtro_activo = 'Por Nombre',
            )


@app.route('/acerca_de/')
def acerca_de():
    return render_template('acerca_de.html')


# fixes para que ande mac y el portal cautivo
# http://forums.appleinsider.com/t/153426/ios-6-and-captive-portals#post_2279865
@app.route('/library/test/success.html')
def fix_ios():
    return "<HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML>"

@app.route('/errors/err404.html')
def error_pages():
    return render_template(
            'err404.html',
            active_page='Error',
            )

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')

