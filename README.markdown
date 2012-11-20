# INTRODUCTION

Fbone (Flask bone) is a [Flask](http://flask.pocoo.org) (Python microframework) template/bootstrap/boilerplate application.

![Flask bone homepage screenshot](http://github.com/imwilsonxu/fbone/raw/master/screenshots/flask-bone-homepage-screenshot.png)

# FEATURES

- Register, login, logout, remember me and reset password.
- Use [twitter/bootstrap](https://github.com/twitter/bootstrap) and [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate).
- Handle forms with [WTForms](http://wtforms.simplecodes.com/).
- Handle database with [SQLAlchemy](http://www.sqlalchemy.org).
- Deploy on Apache + mod\_wsgi with [fabric](http://flask.pocoo.org/docs/deploying/mod_wsgi/).
- i18n support with [Flask-Babel](http://packages.python.org/Flask-Babel/).
- Unit testing with [Flask-Testing](http://packages.python.org/Flask-Testing/).

# USAGE

## Ubuntu

Download codes.

    git clone https://github.com/imwilsonxu/fbone.git <your-project-name>
    cd <your-project-name>
    # Clean git history.
    rm -rf .git

Setup packages.

    python setup.py install

Reset database (with sqlite, check out `fbone/config.py`).

    python manage.py reset

Run local server.
    
    python manage.py run

Compile babel.

    python setup.py compile_catalog --directory fbone/translations --locale zh -f

Deploy with fabric

    fab deploy

# STRUCTURE

    sudo apt-get install -y tree
    cd fbone
    tree

# ACKNOWLEDGEMENTS

Thanks to Flask and its [extensions](http://flask.pocoo.org/extensions/).
