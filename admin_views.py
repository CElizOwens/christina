from flask import render_template, request, redirect, abort
# from persistence import persistence
from website import app


@app.route('/admin/dashboard')
def admin_dashboard():
    return "Admin Dashboard"

@app.route('/admin/profile')
def admin_profile():
    return "Admin Profile"
