# -*- coding: utf-8 -*-

import os

from flask.ext.script import Manager

from fbone import create_app
from fbone.extensions import db
from fbone.user import User, UserDetail, ADMIN, USER, ACTIVE


app = create_app()
manager = Manager(app)
project_root_path = os.path.join(os.path.dirname(app.root_path))


@manager.command
def run():
    """Run local server."""

    app.run()


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()
    # Init/reset data.

    demo = User(
            name=u'demo', 
            email=u'demo@example.com', 
            password=u'123456', 
            role_id=USER,
            status_id=ACTIVE,
            user_detail=UserDetail(
                age=10,
                url=u'http://demo.example.com', 
                deposit=100.00,
                location=u'Hangzhou', 
                bio=u'Demo Guy is ... hmm ... just a demo guy.'),
            )
    admin = User(
            name=u'admin', 
            email=u'admin@example.com', 
            password=u'123456', 
            role_id=ADMIN,
            status_id=ACTIVE,
            user_detail=UserDetail(
                age=10,
                url=u'http://admin.example.com', 
                deposit=100.00,
                location=u'Hangzhou', 
                bio=u'admin Guy is ... hmm ... just a admin guy.'),
            )
    db.session.add(demo)
    db.session.add(admin)
    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
