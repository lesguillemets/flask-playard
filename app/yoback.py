#!/usr/bin/env python2
import requests
from flask import request
from consts import yoback_token
from app import app

@app.route("/yoback", methods=["GET"])
def yoback():
    user = request.args.get('username')
    p = requests.post(
        'http://api.justyo.co/yo/',
        data = {'api_token': yoback_token, 'username': user}
    )
    if p.ok:
        return("OK")
    else:
        return p.status_code
