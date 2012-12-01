# -*- coding: utf-8 -*-

import os

from flask.ext.script import Manager, prompt, prompt_pass, prompt_bool

from fbone import create_app
from fbone.extensions import db
from fbone.models import User, UserDetail, UserRole


manager = Manager(create_app())

from fbone import create_app
app = create_app()
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
            name = u'demo', 
            email = u'demo@example.com', 
            password = u'123456', 
            role_id = 1,
            user_detail = UserDetail(
                real_name = u'Demo Guy',
                age = 10,
                url = u'http://demo.example.com', 
                location = u'Hangzhou', 
                bio = u'Demo Guy is ... hmm ... just a demo guy.'
                ),
            )
    db.session.add(demo)
    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
