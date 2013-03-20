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
    return render_template('index.html')

@app.route('/libros')
def libros():
    return render_template('catalogo.html', active_page='Libros')

@app.route('/cuentos')
def cuentos():
    return render_template('cuentos.html')

@app.route('/revistas')
def revistas():
    return render_template('revistas.html')

@app.route('/acerca_de')
def acerca_de():
    return render_template('acerca_de.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
