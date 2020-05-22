from flask import render_template, request, redirect, abort
# from persistence import persistence
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/scratch')
def scratch():
    return render_template('scratch.html')
