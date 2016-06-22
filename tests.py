# -*- coding: utf-8 -*-

import unittest
from flask_testing import TestCase

from fbone import create_app
from fbone.user import User
from fbone.config import TestConfig
from fbone.extensions import db


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def init_data(self):
        demo = User(
                name=u'demo',
                email=u'demo@example.com',
                password=u'123456')
        db.session.add(demo)
        db.session.commit()

    def setUp(self):
        """Reset all tables before testing."""

        db.create_all()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""

        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        data = {
            'login': username,
            'password': password,
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        assert "Logged in" in response.data
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


class TestFrontend(BaseTestCase):

    def test_show(self):
        self._test_get_request('/', 'index.html')

    def test_signup(self):
        self._test_get_request('/signup', 'frontend/signup.html')

        data = {
            'email': 'new_user@example.com',
            'password': '123456',
            'name': 'new_user',
            'agree': True,
        }
        response = self.client.post('/signup', data=data, follow_redirects=True)
        assert "Signed up" in response.data
        new_user = User.query.filter_by(email=data['email']).first()
        assert new_user.name == "new_user"

    def test_login(self):
        self._test_get_request('/login', 'frontend/login.html')

        response = self.client.post('/login', data={
            'login': "demo@example.com",
            'password': "123456"}, follow_redirects=True)
        assert "Logged in" in response.data

    def test_logout(self):
        self.login("demo@example.com", "123456")
        self._logout()


if __name__ == '__main__':
    unittest.main()
