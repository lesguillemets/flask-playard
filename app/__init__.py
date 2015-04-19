#!/usr/bin/env python2
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
