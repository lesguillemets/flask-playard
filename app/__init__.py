#!/usr/bin/env python2
from __future__ import unicode_literals
from flask import Flask
from flask import request
from flask import json
import requests

from consts import yoback_token

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/yoback", methods=["GET","POST"])
def yoback():
    user = request.form['username']
    requests.post(
        'http://api.justyo.co/yo/',
        data = {'api_token': yoback_token, 'username': user}
    )
    return("OK")
