from flask import render_template, g
from flask.ext.login import current_user

from app import app
from app import config

from app.api import api
app.register_blueprint(api)
from app.auth import auth
app.register_blueprint(auth)


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
