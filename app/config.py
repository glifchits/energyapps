import os
import secret_config


class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    BASE_URL = 'http://localhost:5000'
    REDIRECT_URI = BASE_URL + '/auth'

class LocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost'

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = secret_config.PROD_DB_URI
    BASE_URL = 'http://www.mpowr.ca'
