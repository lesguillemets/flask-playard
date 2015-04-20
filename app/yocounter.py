#!/usr/bin/env python2

import requests
from google.appengine.ext import ndb
from flask import request
from consts import yoback_token
from app import app
from consts import yocounter_token

class CountedYoer(ndb.Model):
    username = ndb.StringProperty()
    count = ndb.IntegerProperty(default=1)
    last_yoed = ndb.DateTimeProperty(auto_now=True, auto_now_add=True)
    
    @classmethod
    def query_book(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.last_yoed)

@app.route("/yocounter/callback")
def countup():
    user = request.args.get('username')
    user_records = CountedYoer.query(
        CountedYoer.username == user).fetch(1)
    if not user_records:
        create_user(user)
        notify_user(user)
        return (
            "Hello, Nice to meet you!" +
            "This is the first time you've yoed me!"
        )
    else:
        user_record = user_records[0]
        n = user_record.count
        last_yo = user_record.last_yoed
        user_record.count += 1
        if (n+1) % 10 == 0:
            notify_user(user)
        user_record.put()
        return ("This is the " + str(n) + " th yo, " + user + ".\n"
                "You Last Yoed me " + str(last_yo) + "UTC."
                )

def notify_user(username):
    p = requests.post(
        'http://api.justyo.co/yo/',
        data = {
            'api_token': yocounter_token, 'username': username,
            'link' : ('http://playard-lesguillemets.appspot.com/yocounter/user/' + username)
        }
    )
    if p.ok:
        return "OK"
    else:
        return p.status_code

@app.route("/yocounter/user/<username>")
def show_yo_count(username):
    user_records = CountedYoer.query(
        CountedYoer.username == username).fetch(1)
    if not user_records:
        return "You haven't yoed me yet."
    else:
        user_record = user_records[0]
        return ("You've yoed me " + str(user_record.count) + " times.")

def create_user(username):
    user = CountedYoer(
        parent=ndb.Key("YoCountBook", "first"),
        username = username
    )
    return user.put()
