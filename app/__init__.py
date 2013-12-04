from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

import os
import schema

app = Flask(__name__)

lm = LoginManager()
lm.init_app(app)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost'
db = SQLAlchemy(app)

db.create_all()

app.secret_key = os.urandom(24)
