from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

import os
import schema
import constants
from config import exported as exportedConfig

app = Flask(__name__)
app.config.from_object(exportedConfig)

db = SQLAlchemy(app)
db.create_all()

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'
lm.login_message = (constants.CSS_ERR, "You need to be logged in to do that!")

