from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

import os
import schema
import constants


app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost'
db = SQLAlchemy(app)

db.create_all()

app.secret_key = os.urandom(24)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'
lm.login_message = (constants.CSS_ERR, "You need to be logged in to do that!")

