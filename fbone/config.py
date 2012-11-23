# -*- coding: utf-8 -*-

PROJECT = "fbone"

class BaseConfig(object):

    DEBUG = False
    TESTING = False

    # os.urandom(24)
    SECRET_KEY = 'secret key'


class DefaultConfig(BaseConfig):

    DEBUG = True

    SQLALCHEMY_ECHO = True
    # Sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/%s.sqlite' % PROJECT
    # Mysql:
    #SQLALCHEMY_DATABASE_URI = 'mysql://dbusername:dbpassword@dbhost/dbname'

    # To create log folder.
    # $ sudo mkdir -p /var/log/<PROJECT>
    # $ sudo chown $USER /var/log/<PROJECT>
    DEBUG_LOG = '/var/log/%s/debug.log' % PROJECT

    ACCEPT_LANGUAGES = ['zh']
    BABEL_DEFAULT_LOCALE = 'en'

    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Email (Flask-email)
    # https://bitbucket.org/danjac/flask-mail/issue/3/problem-with-gmails-smtp-server
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'imwilsonxu'
    MAIL_PASSWORD = 'Nicorobin'
    DEFAULT_MAIL_SENDER = '%s@gmail.com' % MAIL_USERNAME


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
