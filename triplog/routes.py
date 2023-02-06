from flask import render_template, url_for
from triplog import app


@app.route("/")
def hello():
    return render_template('layout.html')
