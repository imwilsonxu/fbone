# INTRODUCTION

Fbone (Flask bone) is a [Flask](http://flask.pocoo.org) (Python microframework) template/bootstrap/boilerplate application, with best practices.

You can use it for

- learning Flask.
- kicking off your new project.

![Flask bone homepage screenshot](http://github.com/imwilsonxu/fbone/raw/master/screenshots/flask-bone-homepage-screenshot.png)

## FEATURES

### Frontend Framework

- [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate).
- [jQuery](http://jquery.com/). 
- [Twitter Bootstrap](https://github.com/twitter/bootstrap).

### Flask Extensions

- Handle **orm** with [SQLAlchemy](http://www.sqlalchemy.org).
- Handle **web forms** with [WTForms](http://wtforms.simplecodes.com/).
- Implement **user session management (signin/signout/rememberme)** with [Flask-Login](https://github.com/maxcountryman/flask-login).
- Implement **reset password via email** with [Flask-Mail](http://packages.python.org/Flask-Mail/).
- Implement **unit testing** with [Flask-Testing](http://packages.python.org/Flask-Testing/).
- Implement **external script (initdb/testing/etc)** with [Flask-Script](http://flask-script.readthedocs.org/en/latest/).
- Handle **i18n** with [Flask-Babel](http://packages.python.org/Flask-Babel/).

### Others

- Well designed structure for **large project**.
- Quickly Deploy via [mod\_wsgi](http://flask.pocoo.org/docs/deploying/mod_wsgi/) and [fabric](http://flask.pocoo.org/docs/patterns/fabric/).
- Admin interface.
- Home-bake logger.

## USAGE

Pre-required:

- Ubuntu (should be fine in other linux distro)
- git
- pip
- fabric
- sqlite
- virtualenv
- apache + mod\_wsgi

Clone.

    git clone https://github.com/imwilsonxu/fbone.git fbone

virtualenv.

    fab setup

Debug.

    fab d

Open `http://127.0.0.1:5000`, done!

## Deploy with WSGI

Clone.

    cd /var/www
    git clone https://github.com/imwilsonxu/fbone.git fbone
    sudo chown `whoami` -R fbone

vhost.

    WSGIDaemonProcess fbone user=wilson group=wilson threads=5
    WSGIScriptAlias /fbone /var/www/fbone/app.wsgi

    <Directory /var/www/fbone/>
        WSGIScriptReloading On
        WSGIProcessGroup fbone
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>

virtualenv.

    fab setup

**IMPORTANT**:

- Change `INSTANCE_FOLDER_PATH` in `fbone/utils.py` to suit yourself.
- Put `production.cfg` under `INSTANCE_FOLDER_PATH`.

## STRUCTURE

    ├── app.wsgi                (mod_wsgi wsgi config)
    ├── CHANGES
    ├── fabfile.py              (fabric file)
    ├── fbone                   (main app)
    │   ├── api                 (api module)
    │   ├── app.py              (create flask app)
    │   ├── config.py           (config module)
    │   ├── decorators.py
    │   ├── extensions.py       (init flask extensions)
    │   ├── frontend            (frontend module)
    │   ├── __init__.py
    │   ├── settings            (settings module)
    │   ├── static
    │   │   ├── css
    │   │   ├── favicon.png
    │   │   ├── humans.txt
    │   │   ├── img
    │   │   ├── js
    │   │   └── robots.txt
    │   ├── templates
    │   │   ├── errors
    │   │   ├── frontend
    │   │   ├── index.html
    │   │   ├── layouts 
    │   │   ├── macros
    │   │   ├── settings
    │   │   └── user
    │   ├── translations        (i18n)
    │   ├── user                (user module)
    │   │   ├── constants.py
    │   │   ├── forms.py        (wtforms)
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── views.py
    │   ├── utils.py
    ├── LICENSE
    ├── manage.py               (manage via flask-script)
    ├── MANIFEST.in
    ├── README.markdown
    ├── screenshots
    ├── setup.py
    └── tests                   (unit tests, run via `nosetest`)

## LICENSE

[MIT LICENSE](http://www.tldrlegal.com/license/mit-license)

## ACKNOWLEDGEMENTS

Thanks to Python, Flask, its [extensions](http://flask.pocoo.org/extensions/), and other goodies.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/imwilsonxu/fbone/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

