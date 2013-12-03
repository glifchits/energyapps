from flask import render_template

from app import app
from app import config

from app.api import api
app.register_blueprint(api)
from app.auth import auth
app.register_blueprint(auth)


@app.route('/')
def home():
    return render_template('index.html', auth_url = config.AUTH_URL)


if __name__ == '__main__':
    app.run()
