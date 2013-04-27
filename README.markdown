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
- Implement **unit testing** with [Flask-Testing](http://packages.python.org/Flask-Testing/).
- Implement **external script (initdb/testing/etc)** with [Flask-Script](http://flask-script.readthedocs.org/en/latest/).
- Implement **admin interface**.
- Implement **Logger**.
- Handle **i18n** with [Flask-Babel](http://packages.python.org/Flask-Babel/).
- Handle **web forms** with [WTForms](http://wtforms.simplecodes.com/).
- Handle **orm** with [SQLAlchemy](http://www.sqlalchemy.org).
- Handle **deployment** with [mod\_wsgi](flask.pocoo.org/docs/deploying/mod_wsgi/) and [fabric](flask.pocoo.org/docs/patterns/fabric/).

## USAGE

Pre-required:

- Ubuntu (or other linux distro)
- git
- pip
- fabric
- sqlite
- virtualenv
- apache + mod\_wsgi

Clone.

    git clone https://github.com/imwilsonxu/fbone.git fbone

Debug.

    fab d

Open `http://127.0.0.1:5000`, done!

## Deploy with WSGI

virtualenv.

    virtualenv env
    . env/bin/activate
    python setup.py install

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

## STRUCTURE

Use `tree` to display project structure:
    
    sudo apt-get install -y tree
    cd fbone
    tree

Explain:

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

Thanks to Flask, its [extensions](http://flask.pocoo.org/extensions/), and other goodies.
