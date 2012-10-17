# Fbone

Fbone is a template/boostrap/boilerplate flask application.

## Features

- Register, login, logout, remember me and reset password.
- Use [twitter/bootstrap](https://github.com/twitter/bootstrap) and [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate).
- Handle forms with [WTForms](http://wtforms.simplecodes.com/).
- Handle database with [SQLAlchemy](http://www.sqlalchemy.org).
- Deploy on Apache + mod\_wsgi with [fabric](http://flask.pocoo.org/docs/deploying/mod_wsgi/).
- i18n support with [Flask-Babel](http://packages.python.org/Flask-Babel/).
- Unit testing with [Flask-Testing](http://packages.python.org/Flask-Testing/).

## Usage

    # install packages.
    $ python setup.py install

    # run local server
    $ python shell.py run

    # reset database
    $ python shell.py reset

    # compile with babel
    $ python setup.py compile_catalog --directory fbone/translations --locale zh -f
