#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
http://python.org.ar/pyar/Recetario/NormalizarCaracteresUnicode
http://stackoverflow.com/questions/120656/directory-listing-in-python
'''

import os
import shutil

from unicodedata import normalize

ANTES = {}

src_dir = './libros_orig/'
dst_dir = './libros/'

def normalizar_string(unicode_string):
    u"""Retorna unicode_string normalizado para efectuar una búsqueda.

    >>> normalizar_string(u'Mónica Viñao')
    'monica_vinao'

    """
    return normalize('NFKD', unicode_string).encode('ASCII', 'ignore').lower().replace(' ','_')

def normalizar_archivos():
    # Primero creamos todos los directorios
    for dirname, dirnames, filenames in os.walk(src_dir):
        ndirname = normalizar_string(dirname.decode('utf8'))
        for subdirname in dirnames:
            nsubdirname = normalizar_string(subdirname.decode('utf8'))
            new_dir = os.path.join(ndirname.replace(src_dir, dst_dir), nsubdirname)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

    for dirname, dirnames, filenames in os.walk(src_dir):
        ndirname = normalizar_string(dirname.decode('utf8'))
        for filename in filenames:
            nfilename = normalizar_string(filename.decode('utf8'))
            if filename != nfilename:
                ANTES[nfilename] = filename
            shutil.copy(os.path.join(dirname, filename),
                        os.path.join(ndirname.replace(src_dir, dst_dir), nfilename))

if __name__ == "__main__":

    normalizar_archivos()

    for dirname, dirnames, filenames in os.walk(dst_dir):
        for filename in filenames:
            print os.path.join(dirname, filename),
            if filename in ANTES:
                print " || ", ANTES[filename],
            print

