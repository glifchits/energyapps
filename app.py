from flask import render_template

from app import app
from app import config
from app.api import api
app.register_blueprint(api)
'''
from app.data import data
app.register_blueprint(data)
'''

@app.route('/')
def index():
    return render_template('index.html', auth_url = config.AUTH_URL)


if __name__ == '__main__':
    app.run()
