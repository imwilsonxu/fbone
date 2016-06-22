# -*- coding: utf-8 -*-

from flask import Flask, render_template

from config import DefaultConfig
from user import User

from extensions import db, login_manager
from filters import format_date, pretty_date, nl2br
from utils import INSTANCE_FOLDER_PATH


# For import *
__all__ = ['create_app']


def create_app(config=None, app_name=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT

    app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH, instance_relative_config=True)
    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app)
    configure_extensions(app)
    configure_logging(app)
    configure_template_filters(app)
    configure_error_handlers(app)
    configure_cli(app)

    return app


def configure_app(app, config=None):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(DefaultConfig)

    # http://flask.pocoo.org/docs/config/#instance-folders
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)

    # Use instance folder instead of env variables to make deployment easier.
    #app.config.from_envvar('%s_APP_CONFIG' % DefaultConfig.PROJECT.upper(), silent=True)


def configure_extensions(app):
    # flask-sqlalchemy
    db.init_app(app)

    # Sentry
    if app.config['SENTRY_DSN']:
        sentry.init(app, dsn=app.config['SENTRY_DSN'])

    # flask-login
    login_manager.login_view = 'frontend.login'
    login_manager.refresh_view = 'frontend.reauth'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    login_manager.setup_app(app)


def configure_blueprints(app):
    """Configure blueprints in views."""

    from user import user
    from frontend import frontend
    from api import api

    for bp in [user, frontend, api]:
        app.register_blueprint(bp)


def configure_template_filters(app):
    """Configure filters."""

    app.jinja_env.filters["pretty_date"] = pretty_date
    app.jinja_env.filters["format_date"] = format_date
    app.jinja_env.filters["nl2br"] = nl2br


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    import os
    from logging.handlers import SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)

    # Testing
    #app.logger.info("testing info.")
    #app.logger.warn("testing warn.")
    #app.logger.error("testing error.")

    mail_handler = SMTPHandler(app.config['MAIL_SERVER'],
                               app.config['MAIL_USERNAME'],
                               app.config['ADMINS'],
                               'Your Application Failed!',
                               (app.config['MAIL_USERNAME'],
                                app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(mail_handler)


def configure_hook(app):

    @app.before_request
    def before_request():
        pass


# http://flask.pocoo.org/docs/latest/errorhandling/
def configure_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404


def configure_cli(app):

    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()
