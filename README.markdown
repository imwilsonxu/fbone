# INTRODUCTION

Fbone (Flask bone) is a [Flask](http://flask.pocoo.org) (Python microframework) template/bootstrap/boilerplate application.

You can use it for

- learning Flask.
- quicker developing your new project.

![Flask bone homepage screenshot](http://github.com/imwilsonxu/fbone/raw/master/screenshots/flask-bone-homepage-screenshot.png)

## FEATURES

- Well designed for **large project**.
- **Support HTML5** with [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate).
- Integrate with [jQuery](http://jquery.com/) and [bootstrap](https://github.com/twitter/bootstrap).
- Implement **user session management (signin/signout/rememberme)** with [Flask-Login](https://github.com/maxcountryman/flask-login).
- Implement **reset password via email** with [Flask-Mail](http://packages.python.org/Flask-Mail/).
- Implement **admin interface** with [Flask-Admin](https://flask-admin.readthedocs.org/en/latest/quickstart/).
- Implement **unit testing** with [Flask-Testing](http://packages.python.org/Flask-Testing/).
- Implement **external script (initdb/testing/etc)** with [Flask-Script](http://flask-script.readthedocs.org/en/latest/).
- Implement **Logger**.
- Handle **i18n** with [Flask-Babel](http://packages.python.org/Flask-Babel/).
- Handle **web forms** with [WTForms](http://wtforms.simplecodes.com/).
- Handle **orm** with [SQLAlchemy](http://www.sqlalchemy.org).
- Handle **deployment** with [mod\_wsgi](flask.pocoo.org/docs/deploying/mod_wsgi/) and [fabric](flask.pocoo.org/docs/patterns/fabric/).

## USAGE

Assume you are in Ubuntu and the project name is "myapp".

    sudo git clone https://github.com/imwilsonxu/fbone.git /srv/www/myapp
    sudo chmod -R o+w /srv/www/myapp
    cd /srv/www/myapp
    fab init:myapp

Open `http://127.0.0.1`, done!

Init/reset database (with sqlite, check out `fbone/config.py`).

    python manage.py initdb
    sudo chmod o+w /tmp/<project>.sqlite

Debug with local server.
    
    fab run

Compile babel.

    fab babel

## STRUCTURE

    sudo apt-get install -y tree
    cd fbone
    tree

## LICENSE

[MIT LICENSE](http://www.tldrlegal.com/license/mit-license)

## ACKNOWLEDGEMENTS

Thanks to Flask, its [extensions](http://flask.pocoo.org/extensions/), and other goodies.
