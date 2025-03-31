"""
NSIthèque
"""
from functools import wraps

import pypdftk
from flask_wtf.file import FileAllowed
from pyotp import OTP

# are we in dev mode ?
__dev__ = True

from flask import Flask, render_template, request, abort, session, url_for, redirect, flash, make_response
from flask_compress import Compress
from db_factory import *
from app_secrets import *
import pyotp
from urllib.parse import unquote, quote
import segno
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField, RadioField, SelectMultipleField
from wtforms.fields.simple import PasswordField, SubmitField, StringField, HiddenField, FileField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

# compress output
Compress(app)

app._db = create_db_object(__dev__)
app._otp = pyotp.TOTP(LOGIN_KEY)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# -------------------------------- Helper functions

# pdf extraction
def extract_pdf_pages(filename:str, out_filename:str, pages:list[int], annexes:list[int] | None=None) -> None:
    """
    extracts pages from pdf file to another file
    :param filename: filename of original pdf file
    :param out_filename: output file name
    :param pages: pages ranges to extract - ex: [3,6]
    :param annexes:  pages ranges to extract for annexes - ex: [3,6] - defaults to None
    :return: temporary file with extracted pages or the out_file argument
    """
    ranges: list[list[int]] = [pages]
    if annexes is not None:
        ranges.append(annexes)
    pypdftk.get_pages(pdf_path=filename, ranges=ranges, out_file=out_filename)


# verify if pdf file exists and extract if needed
def ensure_file_exists(data:list[dict], filename_key:str, original_filename_key:str, number_key:str, pages_key:str, other_pages_key:str, filename_root:str='Ex') -> None:
    """
    Ensures that the file exists for exercises
        if don't, create the file by extracting pages from original page
    :param filename_root: root of the filename - defaults to 'Ex'
    :param data: list of database results (list of dicts)
    :param filename_key: key dict for destination filename
    :param original_filename_key: key dict for original filename
    :param number_key: key for exercise number
    :param pages_key: key for main page range
    :param other_pages_key: key for additionnal page range
    :return: None
    """
    for item in data:
        if item[filename_key] is None:
            # create filename
            item[filename_key] = f"{filename_root}{item[number_key]}-{item[original_filename_key]}"
            # pages
            pages = item[pages_key].split('-')
            # annexes
            if other_pages_key is not None and item[other_pages_key] is not None:
                others = item[other_pages_key].split('-')
            else:
                others = []
            # extract pages
            extract_pdf_pages(filename=item[original_filename_key],
                              out_filename=item[filename_key],
                              pages=pages,
                              annexes=others)


# guess data info from filename
def guess_data_from_filename(filename):
    """
    Try to guess data from filename
    at least: the two firsts digits as year
    at best: all data
    :param filename: filename to match
    :return: guessed data as dict like {'year':..., 'day':..., 'geo':..., 'number':...}
    """
    import re
    # try the whole
    # filename should be like reference -> 24-NSIJ1AN1.pdf or 24_NSIJ1AN1.pdf or 24NSIJ1AN1.pdf
    re_str = r'^(?P<year>[0-9]{2})[-_]?NSIJ(?P<day>[0-9])(?P<zone>\w{2})(?P<number>[0-9]).pdf$'
    match_found = re.match(re_str, filename)
    if match_found is not None:
        return match_found.groupdict()
    # try only the year
    # filename should start with two digits like 25$$$ty$rty$rt$y$rty$.titi
    re_str = r'^(?P<year>[0-9]{2})'
    match_found = re.match(re_str, filename)
    if match_found is not None:
        d = match_found.groupdict()
        # add non guessed data
        d.update({'day': None , 'geo': None , 'number': None})
        return d
    # nothing found
    return {'year': None, 'day': None , 'geo': None , 'number': None}


# db select queries
def db_get(sql, *args, no_list_auto=True):
    """get data with select statement"""
    data = app._db.make_sql_select(sql, *args)
    # app.logger.info(f"from Db {data!s}")
    if len(data) == 1 and no_list_auto:
        return data[0]
    return data


# db other queries
def db_update(sql, **kwargs):
    """update or delete data"""
    app._db.make_sql_update(sql, **kwargs)


# generate qr code inline image
@app.template_filter('qr')
def qr(path, **kwargs):
    """template filter to create qr code"""
    return segno.make_qr(path).svg_data_uri(**kwargs)


# disable caching for specific routes
def nocache(f):
    """decorator to disable caching"""
    @wraps(f)
    def no_cache(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return no_cache


def is_admin_user():
    """return if user is an admin"""
    return 'user' in session and session['user'] == 'admin'


# ----------------- Forms
class LoginForm(FlaskForm):
    key = StringField("Code d'authentification OTP",
                      render_kw={'inputmode': 'numeric', 'pattern': "[0-9]{6}", "autofocus": True,
                                 "placeholder": "OTP"}, validators=[DataRequired()])
    link_back = HiddenField(name='link_back', validators=[DataRequired()])


class ThemeForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    parent = RadioField('Parent',validators=[DataRequired()])


class SujetEcritForm(FlaskForm):
    reference = StringField('Reference', validators=[DataRequired()])
    fichier = FileField('Fichier du sujet (pdf)',
                        validators=[DataRequired(), FileAllowed(['pdf'])],
                        render_kw={"placeholder": "Fichier du sujet"})
    annee = StringField("Année",
                      render_kw={'inputmode': 'numeric', 'pattern': "[0-9]{4}","placeholder": "Année"},
                       validators=[DataRequired()])
    zone_geographique = SelectField("Zone Géographique", validators=[DataRequired()])
    # -- Exercices
    exercice1_numero = StringField("Exercice 1",
                                   validators=[DataRequired()],
                                   render_kw={'inputmode': 'numeric', 'placeholder': '1,2,3,4,5', 'pattern': '[1-5]{1}'})
    exercice1_pages = StringField("Pages du sujet",
                                  validators=[DataRequired()],
                                  render_kw={'placeholder': '2-5'})
    exercice1_annexes = StringField("Pages de l'annexe",
                                    render_kw={'placeholder': '1,2,3,4,5'})
    exercice1_themes = SelectMultipleField("Themes de l'exercice",
                                           validators=[DataRequired()])
    # --
    exercice2_numero = StringField("Exercice 1",
                                   validators=[DataRequired()],
                                   render_kw={'inputmode': 'numeric', 'placeholder': '1,2,3,4,5',
                                              'pattern': '[1-5]{1}'})
    exercice2_pages = StringField("Pages du sujet",
                                  validators=[DataRequired()],
                                  render_kw={'placeholder': '2-5'})
    exercice2_annexes = StringField("Pages de l'annexe",
                                    render_kw={'placeholder': '1,2,3,4,5'})
    exercice2_themes = SelectMultipleField("Themes de l'exercice",
                                           validators=[DataRequired()])
    # --
    exercice3_numero = StringField("Exercice 1",
                                   validators=[DataRequired()],
                                   render_kw={'inputmode': 'numeric', 'placeholder': '1,2,3,4,5',
                                              'pattern': '[1-5]{1}'})
    exercice3_pages = StringField("Pages du sujet",
                                  validators=[DataRequired()],
                                  render_kw={'placeholder': '2-5'})
    exercice3_annexes = StringField("Pages de l'annexe",
                                    render_kw={'placeholder': '1,2,3,4,5'})
    exercice3_themes = SelectMultipleField("Themes de l'exercice",
                                           validators=[DataRequired()])
    # --
    exercice4_numero = StringField("Exercice 1",
                                   render_kw={'inputmode': 'numeric', 'placeholder': '1,2,3,4,5',
                                              'pattern': '[1-5]{1}'})
    exercice4_pages = StringField("Pages du sujet",
                                  render_kw={'placeholder': '2-5'})
    exercice4_annexes = StringField("Pages de l'annexe",
                                    render_kw={'placeholder': '1,2,3,4,5'})
    exercice4_themes = SelectMultipleField("Themes de l'exercice")
    # --
    exercice5_numero = StringField("Exercice 1",
                                   render_kw={'inputmode': 'numeric', 'placeholder': '1,2,3,4,5',
                                              'pattern': '[1-5]{1}'})
    exercice5_pages = StringField("Pages du sujet",
                                  render_kw={'placeholder': '2-5'})
    exercice5_annexes = StringField("Pages de l'annexe",
                                    render_kw={'placeholder': '1,2,3,4,5'})
    exercice5_themes = SelectMultipleField("Themes de l'exercice")


# ------------ Frontend
@app.route('/')
def index():
    """index"""
    return render_template('index.html')


@app.route('/chronologie-ecrit')
def chronologie_ecrit():
    """sujets écrits par année - tableau général"""
    pass


@app.route('/chronologie-ecrit/<annee>')
def par_annee(annee):
    """sujets écrits par année"""
    pass


@app.route('/geo')
def regions():
    liste_regions = db_get(SELECT_ZONE_GEO)
    return str(liste_regions), 200


@app.route('/geo/<region>')
def par_region(region):
    """sujet d'un certaine région"""
    pass


@app.route('/theme')
def themes():
    """index des themes"""
    themes = db_get(SELECT_LIST_THEMES)
    return str(themes), 200


@app.route('/theme/<theme>')
def par_theme(theme):
    """sujets par theme"""
    pass


# ------------ Backend (secure part)

def admin_required(f):
    """decorator where admin access is required"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin_user():
            return redirect("/login?link_back={}".format(quote(request.url)))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    """login"""
    form = LoginForm()
    if request.method == 'POST':
        key = form.key.data
        if not app._otp.verify(key):
            flash('Invalid OTP Code')
            return redirect(url_for('login'))
        else:
            flash('Admin logged in')
            session['user'] = 'admin'
            url = form.link_back.data
            if url is not None and url != 'None' and url != '':
                return redirect(url)
            return redirect(url_for("gestion"))
    if request.method == 'GET':
        form.link_back.data = unquote(request.args.get("link_back", ''))
        render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """logout"""
    if 'user' in session:
        session.pop('user')
        flash('You have been logged out')
    url = request.args.get("link_back", None)
    if url is not None and url != 'None':
        return redirect(unquote(url))
    return redirect(url_for('index'))


@app.route('/gestion')
@admin_required
def gestion():
    """index gestion"""
    pass


@app.route('/gestion/themes', methods=['GET', 'POST'])
@admin_required
def gestion_themes():
    """gestion des themes"""
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    abort(405)


@app.route('/gestion/ajout-sujet-ecrit', methods=['GET', 'POST'])
@admin_required
def gestion_ajout_sujet_ecrit():
    """ajout des sujets de l'écrit"""
    form = SujetEcritForm()
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        themes = db_get()
    abort(405)


@app.route('/gestion/sujet-oral', methods=['GET', 'POST'])
@admin_required
def gestion_sujet_oral():
    """gestion des sujets de l'oral"""
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    abort(405)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)