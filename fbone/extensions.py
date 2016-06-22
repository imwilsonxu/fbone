# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
login_manager = LoginManager()

# https://docs.getsentry.com/hosted/clients/python/integrations/flask/
from raven.contrib.flask import Sentry
sentry = Sentry()
