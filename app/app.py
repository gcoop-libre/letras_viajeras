#! -*- coding: utf8 -*-
import csv
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap

SECRET_KEY = 'alskdjalksdjalskdjaslkdjasldjaslkdjasdlkasd,mc,mxcnvm,xncv,sdkas'
BOOTSTRAP_JQUERY_VERSION = None

app = Flask(__name__)
app.config.from_object(__name__)

Bootstrap(app)

def filtrar_csv_por_categoria(categoria):
    with open('datos.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for fila in reader:
            fila = [a.decode('utf8') for a in fila]
            apellido, nombre, titulo, tipo, pdf, imagen = fila
            if tipo == categoria:
                yield (titulo, "%s %s" % (nombre, apellido), pdf, imagen)


@app.route('/')
def index():
    return render_template('index.html', active_page='Inicio')

@app.route('/libros/')
def libros():
    datos = filtrar_csv_por_categoria('libro')
    return render_template('catalogo.html', active_page='Libros', datos=datos)

@app.route('/cuentos/')
def cuentos():
    datos = filtrar_csv_por_categoria('cuento')
    return render_template('catalogo.html', active_page='Cuentos', datos=datos)




@app.route('/revistas/')
def revistas():
    datos = filtrar_csv_por_categoria('revista')
    return render_template('catalogo.html', active_page='Revistas', datos=datos)

@app.route('/acerca_de/')
def acerca_de():
    return render_template('acerca_de.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
