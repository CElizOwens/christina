from flask import render_template, request, redirect, abort
from website.persistence import persistence
from website import app
from dateutil.parser import parse

from datetime import date


@app.route('/login', methods=["GET", "POST"])
def admin_login():
    return render_template('admin/login.html')


@app.route('/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')


@app.route('/repertoire', methods=['GET', 'POST'])
def repertoire():
    if request.method == 'POST':
        composer = request.form['composer']
        title = request.form['title']
        opus = request.form['opus']
        date_played = parse(request.form['date_played']).date()
        ensemble_id = request.form['ensemble_id']
        persistence.insert_piece(composer, title, opus, date_played, ensemble_id)
        redirect('/repertoire')
    all_pieces = persistence.get_all_pieces()
    all_ensembles = persistence.get_all_ensembles()
    return render_template('admin/repertoire.html', pieces=all_pieces, ensembles=all_ensembles)


rost = {
    'violins': ['Harmony TomSun', 'Lila McDonald', 'Niko Durr', 'Teresa Wang'],
    'violas': ['Sara Rusche', 'Thomas Chow (+)', 'Christina Owens (+)'],
    'cellos': ['Diana Louie', 'John Schroder', 'Daniel Chang', 'Nancy Bush'],
    'winds': ['Martha Stoddard (flute)'],
    'groups': ['Oakland Brass']
}


@app.route('/participants', methods=['GET', 'POST'])
def admin_participants():
    if request.method == 'POST':
        req = request.form
        rost[req['category']].append(req['name'])
    return render_template('admin/participants.html', violins=rost['violins'], violas=rost['violas'], cellos=rost['cellos'], winds=rost['winds'], groups=rost['groups'])
