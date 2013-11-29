# local package imports
from flask import Flask, redirect, url_for, render_template, session, \
        request, g
import requests
# stdlib imports
import os
import urllib
import time
from base64 import b64encode
# my app imports
import config
import api_points as api

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html', auth_url = config.AUTH_URL)


if __name__ == '__main__':
    app.run()
