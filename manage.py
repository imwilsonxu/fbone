# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from fbone import create_app
from fbone.extensions import db
from fbone.user import User, UserDetail, Role, ACTIVE
from fbone.utils import MALE


app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run(host="0.0.0.0")


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    db.session.add(Role(
        name=u'admin',
        description='Administrator role'
    ))

    db.session.add(Role(
        name=u'staff',
        description='Staff role'
    ))

    db.session.add(Role(
        name=u'user',
        description='User role'
    ))
    db.session.commit()


    ds = app.security.datastore
    admin = ds.create_user(
	    email='admin',
	    name='Administrator',
	    password=u'123456',
	    roles=['admin', 'user'],
	    status_code=ACTIVE,
	    user_detail=UserDetail(
                sex_code=MALE,
                age=10,
                url=u'http://admin.example.com',
                deposit=100.00,
                location=u'Hangzhou',
                bio=u'admin Guy is ... hmm ... just a admin guy.')
    )

    db.session.add(admin)
    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
