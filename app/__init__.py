from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os
import schema

app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost'
db = SQLAlchemy(app)

db.create_all()

app.secret_key = os.urandom(24)
