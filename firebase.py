from news import News
import os
import pyrebase
import requests
from requests import HTTPError

API_KEY = os.environ['SNAKE_API_KEY']


def exists(child):
    return child.get().val() is not None


def fcm(item: News, is_debug: bool):
    if API_KEY is None or API_KEY is "":
        print("Define a valid SNAKE_API_KEY environment variable")
        return

    headers = {
        "content-type": "application/json",
        "Authorization": "key=" + API_KEY
    }

    data = {
        is_debug and "d_title" or "title": "\"{}\"".format(item.title),
        is_debug and "d_message" or "message": "\"{}\"".format(item.message),
        "url": "\"{}\"".format(item.url),
        "isPrivate": item.is_private and "\"true\"" or "\"false\""
    }

    message = {
        "to": "/topics/global",
        "priority": "high",
        "data": data,
    }

    print("Pushing an item to " + (is_debug and "debug" or "production") + " builds ({})".format(item.number))

    r = requests.post("https://fcm.googleapis.com/fcm/send", json=message, headers=headers)
    code = r.status_code
    if code < 100 or code > 300:
        print("Error {}".format(code))
        print(r.reason)
        print(r.text)
        print(r.content)


def database_auth(username, hash_password: str):
    if API_KEY is None or API_KEY is "":
        print("Define a valid SNAKE_API_KEY environment variable")
        return "1"

    config = {
        "apiKey": API_KEY,
        "authDomain": "liceobold.firebaseapp.com",
        "databaseURL": "https://liceobold.firebaseio.com/",
        "storageBucket": "liceobold.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    if not exists(db.child("users").child(username).shallow()):
        return "2"

    values = str(db.child("users").child(username).get().val())
    print(values)
    print(hash_password)
    print(values == hash_password)
    if values == hash_password:
        return "0"
    else:
        return "3"


def login(email: str, password: str):
    if API_KEY is None or API_KEY is "":
        print("Define a valid SNAKE_API_KEY environment variable")
        return 2

    config = {
       "apiKey": API_KEY,
       "authDomain": "liceobold.firebaseapp.com",
       "databaseURL": "https://liceobold.firebaseio.com/",
       "storageBucket": "liceobold.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()

    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except HTTPError:
        return 1
    else:
        token = user["idToken"]
        registered = user["registered"]
        if registered is False or token is None or token is "":
            return 3
        else:
            return 0
