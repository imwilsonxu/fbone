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
    # Use a tmp database, change to anywhere to suit yourself.
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

    # Should be imported from env var.
    # https://bitbucket.org/danjac/flask-mail/issue/3/problem-with-gmails-smtp-server
    MAIL_DEBUG = DEBUG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'gmail_username'
    MAIL_PASSWORD = 'gmail_password'
    DEFAULT_MAIL_SENDER = '%s@gmail.com' % MAIL_USERNAME

    # Should be imported from env var.
    # export FBONE_APP_CONFIG=/home/wilson/.fbone.cfg
    USER_IMG_UPLOAD_PATH = "/path/to/fbone/static/img/users"


class TestConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
