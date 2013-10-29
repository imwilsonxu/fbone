# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~

    Define TestCase as base class for unit tests.
    Ref: http://packages.python.org/Flask-Testing/
"""

from flask.ext.testing import TestCase as Base, Twill

from fbone import create_app
from fbone.user import User, UserDetail, ADMIN, USER, ACTIVE
from fbone.config import TestConfig
from fbone.extensions import db
from fbone.utils import MALE


class TestCase(Base):
    """Base TestClass for your application."""

    def create_app(self):
        """Create and return a testing flask app."""

        app = create_app(TestConfig)
        self.twill = Twill(app, port=3000)
        return app

    def init_data(self):

        demo = User(
                name=u'demo',
                email=u'demo@example.com',
                password=u'123456',
                role_code=USER,
                status_code=ACTIVE,
                user_detail=UserDetail(
                    sex_code=MALE,
                    age=10,
                    url=u'http://demo.example.com',
                    deposit=100.00,
                    location=u'Hangzhou',
                    bio=u'admin Guy is ... hmm ... just a demo guy.'))
        admin = User(
                name=u'admin',
                email=u'admin@example.com',
                password=u'123456',
                role_code=ADMIN,
                status_code=ACTIVE,
                user_detail=UserDetail(
                    sex_code=MALE,
                    age=10,
                    url=u'http://admin.example.com',
                    deposit=100.00,
                    location=u'Hangzhou',
                    bio=u'admin Guy is ... hmm ... just a admin guy.'))
        db.session.add(demo)
        db.session.add(admin)
        db.session.commit()

    def setUp(self):
        """Reset all tables before testing."""

        db.create_all()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""

        db.drop_all()

    def login(self, username, password):
        data = {
            'login': username,
            'password': password,
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        assert "Hello" in response.data
        return response

    def _logout(self):
        response = self.client.get('/logout')
        self.assertRedirects(response, location='/')

    def _test_get_request(self, endpoint, template=None):
        response = self.client.get(endpoint)
        self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response
