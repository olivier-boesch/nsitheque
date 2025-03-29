"""
NSIthèque
"""

# are we in dev mode ?
try:
    from dev import __dev__
except ImportError:
    __dev__ = False

from flask import Flask, render_template, request, redirect, url_for
from flask_compress import Compress
from db_factory import create_db_object
from app_secrets import *


app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

# compress output
Compress(app)

app._db = create_db_object(__dev__)


# ------------ Frontend
@app.route('/')
def index():
    """index"""
    return render_template('index.html')


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


# ------------ Backend
@app.route('/gestion')
def gestion():
    """index gestion"""
    pass


@app.route('/gestion/themes')
def gestion_themes():
    """gestion des themes"""
    pass


@app.route('/gestion/sujet')
def gestion_sujet():
    """gestion des sujets"""
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)