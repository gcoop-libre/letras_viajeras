#! -*- coding: utf8 -*-
from flask import Flask, url_for, render_template, Response, json, jsonify, redirect, request, flash
from flask.ext.bootstrap import Bootstrap

SECRET_KEY = 'alskdjalksdjalskdjaslkdjasldjaslkdjasdlkasd,mc,mxcnvm,xncv,sdkas'
BOOTSTRAP_JQUERY_VERSION = None

app = Flask(__name__)
app.config.from_object(__name__)

Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html', active_page='Inicio')

@app.route('/libros')
def libros():
    datos = [
        ('Historia de Cronopios y de Famas', 'Julio Cortazar', 'pdf/sample.pdf', 'libros/cronopios_famas.png'),
        ('Rayuela', 'Julio Cortazar', 'pdf/sample.pdf', 'libros/rayuela.png'),
        ('El Aleph', 'Jorge Luis Borges', 'pdf/sample.pdf', 'libros/elaleph.png'),
    ]

    datos = datos * 50

    return render_template('catalogo.html', active_page='Libros', datos=datos)

@app.route('/cuentos')
def cuentos():
    datos = [
        ('Historia de Cronopios y de Famas', 'Julio Cortazar', 'pdf/sample.pdf', 'libros/cronopios_famas.png'),
        ('Rayuela', 'Julio Cortazar', 'pdf/sample.pdf', 'libros/rayuela.png'),
        ('El Aleph', 'Jorge Luis Borges', 'pdf/sample.pdf', 'libros/elaleph.png'),
    ]

    datos = datos * 50

    return render_template('catalogo.html', active_page='Libros', datos=datos)




@app.route('/revistas')
def revistas():
    datos = [
        (u'El Pendulo N°1', u'Varios', u'pdf/sample.pdf', u'revistas/pendulo1.png'),
        (u'El Pendulo N°2', u'Varios', u'pdf/sample.pdf', u'revistas/pendulo2.png'),
        (u'El Pendulo N°5', u'Varios', u'pdf/sample.pdf', u'revistas/pendulo5.png'),
    ]

    datos = datos * 50

    return render_template('catalogo.html', active_page='Revistas', datos=datos)

@app.route('/acerca_de')
def acerca_de():
    return render_template('acerca_de.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
