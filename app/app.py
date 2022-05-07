# pip install flask
# pip install flask-sqlalchemy
# pip install flask_debugtoolbar
# pip install psycopg2-binary
# pip install flask-wtf
# pip install requests

from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def home_route():
    """"""
    return render_template('base.html')