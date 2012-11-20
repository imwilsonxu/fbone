# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.mail import Mail
mail = Mail()

from flaskext.cache import Cache
cache = Cache()

from flask.ext.login import LoginManager
login_manager = LoginManager()
