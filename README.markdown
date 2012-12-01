# INTRODUCTION

Fbone (Flask bone) is a [Flask](http://flask.pocoo.org) (Python microframework) template/bootstrap/boilerplate application.

![Flask bone homepage screenshot](http://github.com/imwilsonxu/fbone/raw/master/screenshots/flask-bone-homepage-screenshot.png)

## FEATURES

- A well designed structure for big project.
- Use [jQuery](http://jquery.com/), [bootstrap](https://github.com/twitter/bootstrap) and [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate).
- Implement tricky "Remember me" with [Flask-Login](https://github.com/maxcountryman/flask-login).
- Handle forms with [WTForms](http://wtforms.simplecodes.com/).
- Handle database with [SQLAlchemy](http://www.sqlalchemy.org).
- Deploy on Apache + mod\_wsgi with [fabric](http://flask.pocoo.org/docs/deploying/mod_wsgi/).
- i18n support with [Flask-Babel](http://packages.python.org/Flask-Babel/).
- Unit testing with [Flask-Testing](http://packages.python.org/Flask-Testing/).

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
