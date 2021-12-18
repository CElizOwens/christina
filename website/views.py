from flask import render_template, request, redirect, abort
# from persistence import persistence
from website import app
from website.config import cross_origin

@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code)

@app.route('/index_v1')
@cross_origin()
def index():
    return render_template('public/index_v1.html')

@app.route('/')
@app.route('/index')
@cross_origin()
def index_v2():
    return render_template('public/index_v2.html')

@app.route('/about')
@cross_origin()
def about():
    return render_template('public/about_v2.html')
