import os
import secret_config


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)
    BASE_URL = 'http://localhost:5000'
    REDIRECT_URI = BASE_URL + '/auth'

class LocalConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost'

class ProdConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = secret_config.PROD_DB_URI
    BASE_URL = 'http://www.mpowr.ca'

exported = LocalConfig()
