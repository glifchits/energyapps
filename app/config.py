import os

class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(24)


class LocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost'
