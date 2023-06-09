# Taken from https://replit.com/@AllAwesome497's Replit template

from flask import Flask
from threading import Thread
import random

app = Flask('')


@app.route('/')
def home():
    return 'Pong!'


def run():
    app.run(host='0.0.0.0', port=random.randint(2000, 9000))


def keep_alive():
    t = Thread(target=run)
    t.start()
