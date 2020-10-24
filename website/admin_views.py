from flask import render_template, request, redirect, url_for, abort
from website.persistence import persistence
from website import app
from dateutil.parser import parse

# from datetime import date


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
        notes = request.form['notes']
        # opus = request.form['opus']
        # date_played = parse(request.form['date_played']).date()
        # ensemble_id = request.form['ensemble_id']
        # persistence.insert_piece(composer, title, opus, ensemble_id)
        persistence.insert_piece(composer, title)
        redirect('/repertoire')
    # all_pieces = persistence.get_all_pieces()
    # # all_ensembles = persistence.get_all_ensembles()
    # return render_template('admin/repertoire.html', pieces=all_pieces)  #    , ensembles=all_ensembles)
    all_performances = persistence.get_all_performances()
    return render_template('admin/repertoire.html', performances=all_performances)


@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        location = request.form['location']
        day_time = parse(request.form['day_time'])
        persistence.insert_event(location, day_time)
        redirect('/events')
    events = persistence.get_all_events()  # just venues and datetimes
    programs = []  # list of event and program namedtuples
    for event in events:
        program = persistence.get_program(event)
        programs.append(program)
    return render_template('admin/events.html', programs=programs)


@app.route('/edit_event/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        notes = request.form['notes']
        persistence.insert_performance(event_id, name, title, notes)
        redirect(url_for('edit_event', event_id=event_id))
    event = persistence.get_event(event_id)
    program = persistence.get_program(event)
    return render_template('admin/edit_event.html', event_id=event_id, program=program)


rost = {
    'violins': ['Harmony TomSun', 'Lila McDonald', 'Niko Durr', 'Teresa Wang'],
    'violas': ['Sara Rusche', 'Thomas Chow (+)', 'Christina Owens (+)'],
    'cellos': ['Diana Louie', 'John Schroder', 'Daniel Chang', 'Nancy Bush'],
    'winds': ['Martha Stoddard (flute)'],
    'groups': ['Oakland Brass']
}


@app.route('/roster', methods=['GET', 'POST'])
def admin_participants():
    if request.method == 'POST':
        req = request.form
        rost[req['category']].append(req['name'])
    return render_template('admin/roster.html', violins=rost['violins'], violas=rost['violas'], cellos=rost['cellos'], winds=rost['winds'], groups=rost['groups'])
