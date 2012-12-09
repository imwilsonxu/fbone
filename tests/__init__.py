# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~

    Define TestCase as base class for unit tests.
    Ref: http://packages.python.org/Flask-Testing/
"""

import functools

from flask.ext.testing import TestCase as Base, Twill

from fbone import create_app
from fbone.models import User, UserDetail, Role, UserStatus
from fbone.config import TestConfig
from fbone.extensions import db


class TestCase(Base):
    """Base TestClass for your application."""

    def create_app(self):
        """Create and return a testing flask app."""

        app = create_app(TestConfig)
        self.twill = Twill(app, port=3000)
        return app

    def init_data(self):

        role_user = Role(name=u'user')
        role_admin = Role(name=u'admin')
        db.session.add(role_user)
        db.session.add(role_admin)
        db.session.commit()

        inactivated = UserStatus(name=u'inactivated')
        activated = UserStatus(name=u'activated')
        frozen = UserStatus(name=u'frozen')
        deleted = UserStatus(name=u'deleted')
        db.session.add(inactivated)
        db.session.add(activated)
        db.session.add(frozen)
        db.session.add(deleted)
        db.session.commit()
        
        demo = User(
                name = u'demo', 
                email = u'demo@example.com', 
                password = u'123456', 
                role = role_user,
                status = activated,
                user_detail = UserDetail(
                    real_name = u'Demo Guy',
                    age = 10,
                    url = u'http://demo.example.com', 
                    location = u'Hangzhou', 
                    bio = u'Demo Guy is ... hmm ... just a demo guy.',
                    ),
                )
        admin = User(
                name = u'admin', 
                email = u'admin@example.com', 
                password = u'123456', 
                role = role_admin,
                status = activated,
                user_detail = UserDetail(
                    real_name = u'admin Guy',
                    age = 10,
                    url = u'http://admin.example.com', 
                    location = u'Hangzhou', 
                    bio = u'admin Guy is ... hmm ... just a admin guy.',
                    ),
                )
        db.session.add(demo)
        db.session.add(admin)
        db.session.commit()

    def setUp(self):
        """Reset all tables before testing."""

        db.create_all()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""

        db.session.remove()
        db.drop_all()

    def _login(self, remember=False):
        name = 'demo'
        user = User.query.filter_by(name=name).first()

        data = {
            'login': name,
            'password': '123456',
            'remember': remember
        }
        response = self.client.post('/login', data=data)
        self.assertRedirects(response, location='/user/')
        return user

    def _logout(self):
        response = self.client.get('/logout')
        self.assertRedirects(response, location='/')

    def _test_get_request(self, endpoint, template=None):
        response = self.client.get(endpoint)
        self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response
