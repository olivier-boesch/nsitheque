"""
NSIthèque
"""
__dev__ = True

from flask import Flask, render_template, request, redirect, url_for
from flask_compress import Compress

if __dev__:

else:
    from db_factory import DbInterface

app = Flask(__name__)

# compress output
Compress(app)


@app.route('/')
def index():
    """index"""
    pass


@app.route('/chronologie-ecrit')
def chronologie_ecrit():
    """sujets écrits par année - tableau général"""
    pass


@app.route('/chronologie-ecrit/<annee:int>')
def par_annee(annee):
    """sujets écrits par année"""
    pass



@app.route('/geo')
def regions():
    """par région géographique"""
    pass


@app.route('/geo/<region>')
def par_region(region):
    """sujet d'un certaine région"""
    pass


@app.route('/theme')
def themes():
    """index des themes"""
    pass


@app.route('/theme/<theme>')
def par_theme(theme):
    """sujets par theme"""
    pass


