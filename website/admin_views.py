from flask import render_template, request, redirect, abort
# from persistence import persistence
from website import app



@app.route('/login', methods=["GET", "POST"])
def admin_login():
    return render_template('admin/login.html')

@app.route('/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/repertoire')
def repertoire():
    return render_template('admin/repertoire.html')


@app.route('/personnel')
def admin_profile():
    return render_template('admin/personnel.html')
