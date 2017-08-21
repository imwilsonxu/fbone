# INTRODUCTION

Fbone (Flask bone) is a [Flask](http://flask.pocoo.org) (Python microframework) template/bootstrap/boilerplate application, with best practices (I hope).

You can use it for

- learning Flask.
- kicking off your new project.

## COMPONENTS

### Frontend

- [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate)
- [jQuery](http://jquery.com/)
- [Twitter Bootstrap](https://github.com/twitter/bootstrap)
- [Jinja2](http://jinja.pocoo.org/docs/dev/)

### Flask Extensions

- [SQLAlchemy](http://www.sqlalchemy.org) and [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org)
- [WTForms](http://wtforms.readthedocs.io) and [Flask-WTF](https://flask-wtf.readthedocs.io).
- [Flask-Login](https://flask-login.readthedocs.io)
- [Flask-Testing](https://pythonhosted.org/Flask-Testing/)
- [Flask-RESTful](http://flask-restful-cn.readthedocs.io/)

### Others

- Modular Applications with Blueprints.
- Use [Sentry](https://getsentry.com) for real-time crash reporting.
- Automated managament via [fabric](http://flask.pocoo.org/docs/patterns/fabric/)

## USAGE

Pre-required Setup:

- MacOS/Ubuntu (should be fine in other linux distro)
- git
- Python / pip / Fabric
- sqlite / MySQL
- Apache + mod\_wsgi

    git clone https://github.com/imwilsonxu/fbone.git fbone

    fab setup_python_macos
    fab bootstrap
    fab test
    fab debug

## STRUCTURE

    ├── CHANGES                     Change logs
    ├── README.markdown
    ├── fabfile.py                  Fabric file to automated managament project
    ├── fbone.conf                  Apache config
    ├── requirements.txt            3rd libraries
    ├── tests.py                    Unittests
    ├── wsgi.py                     Wsgi app
    ├── fbone
       ├── __init__.py
       ├── app.py                   Main App
       ├── config.py                Develop / Testing configs
       ├── constants.py             Constants
       ├── decorators.py            Customized decorators
       ├── extensions.py            Flask extensions
       ├── filters.py               Flask filters
       ├── utils.py                 Python utils
       ├── frontend                 Frontend blueprint
       │   ├── __init__.py
       │   ├── forms.py             Forms used in frontend modular
       │   ├── views.py             Views used in frontend modular
       ├── user
       ├── api
       ├── static                   Static files
       │   ├── css
       │   ├── favicon.png
       │   ├── humans.txt
       │   ├── img
       │   ├── js
       │   └── robots.txt
       └── templates                Jinja2 templates
           ├── errors
           ├── frontend
           ├── index.html
           ├── layouts              Jinja2 layouts
           │   ├── base.html
           │   └── user.html
           ├── macros               Jinja2 macros
           ├── mails                Mail templates
           └── user

## TODO

- Upgrade to [Python3k](https://www.python.org/download/releases/3.0/).
- User [Celery](http://celeryprojet.org), distributed task queue.
- User [Elastic Search](https://github.com/elastic/elasticsearch), Open Source, Distributed, RESTful Search Engine.
- Use [PostgreSQL](https://www.postgresql.org).
- Use [GeeTest](http://www.geetest.com), a popular CAPTCHA service in China.

## LICENSE

[MIT LICENSE](http://www.tldrlegal.com/license/mit-license)

## ACKNOWLEDGEMENTS

Many thanks to Python, Flask and other good stacks.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/imwilsonxu/fbone/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
