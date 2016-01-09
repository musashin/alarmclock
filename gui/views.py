from gui import app
from flask import render_template, request, jsonify

@app.route('/')
@app.route('/index')
def index():
    return render_template("main.html")