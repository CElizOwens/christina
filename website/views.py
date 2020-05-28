from flask import render_template, request, redirect, abort
# from persistence import persistence
from website import app


@app.route('/index_v1')
def index():
    return render_template('public/index_v1.html')

@app.route('/')
@app.route('/index')
def index_v2():
    return render_template('public/index_v2.html')

@app.route('/about')
def about():
    return render_template('public/about_v2.html')
