# Taken from https://replit.com/@AllAwesome497's Replit template
import os 
from flask import Flask
from threading import Thread
import random

app = Flask('')

@app.route('/')
def home():
    repl_owner = os.environ.get('REPL_OWNER')
    return f'{repl_owner} is you !'


def run():
    app.run(host='0.0.0.0', port=random.randint(2000, 9000))


def keep_alive():
    t = Thread(target=run)
    t.start()
