from flask import render_template, request, redirect, abort
# from persistence import persistence
from website import app


@app.route('/index_v1')
def index():
    return render_template('index_v1.html')

@app.route('/')
@app.route('/index')
def index_v2():
    return render_template('index_v2.html')

@app.route('/about')
def about():
    return render_template('about_v2.html')


@app.route('/scratch')
def scratch():
    return render_template('scratch.html')
