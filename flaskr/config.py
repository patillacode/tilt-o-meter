import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DOMAIN = 'http://localhost:5000'


class ProductionConfig(Config):
    DEBUG = False
    DOMAIN = 'https://tiltometer.patilla.es'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True
