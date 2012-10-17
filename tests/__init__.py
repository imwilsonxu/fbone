# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~

    Define TestCase as base class for unit tests.
    Ref: http://packages.python.org/Flask-Testing/
"""

import functools

from flaskext.testing import TestCase as Base, Twill

from fbone import create_app
from fbone.models import User
from fbone.config import TestConfig
from fbone.extensions import db


class TestCase(Base):
    """Base TestClass for your application."""

    def create_app(self):
        """Create and return a testing flask app."""

        app = create_app(TestConfig)
        self.twill = Twill(app, port=3000)
        return app

    def setUp(self):
        """Reset all tables before testing."""

        db.create_all()

    def tearDown(self):
        """Clean db session and drop all tables."""

        db.session.remove()
        db.drop_all()

    def _make_user(self):
        user = User(name='tester', email='tester@test.com', password='123456')
        db.session.add(user)
        db.session.commit()
        assert user.id is not None
        self.user = user

    def _login(self, remember=False):
        name = 'tester'
        user = User.query.filter_by(name=name).first()
        if user is None:
            user = self._make_user()

        data = {
            'login': name,
            'password': '123456',
            'remember': remember
        }
        response = self.client.post('/login', data=data)
        self.assertRedirects(response, location='/user/')

    def _logout(self):
        response = self.client.get('/logout')
        self.assertRedirects(response, location='/')

    def _test_get_request(self, endpoint, template):
        response = self.client.get(endpoint)
        self.assert_200(response)
        self.assertTemplateUsed(name=template)
        return response
