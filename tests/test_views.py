# -*- coding: utf-8 -*-

from werkzeug.urls import url_quote

from fbone.user import User
from fbone.extensions import db, mail

from tests import TestCase


class TestFrontend(TestCase):

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
        assert "Hello" in response.data
        new_user = User.query.filter_by(name=data['name']).first()
        assert new_user is not None

    def test_login(self):
        self._test_get_request('/login', 'frontend/login.html')

    def test_logout(self):
        self.login('demo', '123456')
        self._logout()

    def test_reset_password(self):
        response = self.client.get('/reset_password')
        self.assert_200(response)

        data = {
            'email': 'demo@example.com',
        }
        user = User.query.filter_by(email=data.get('email')).first()
        assert user is not None
        assert user.activation_key is None
        # TODO: how to test sending email?

    def test_footers(self):
        self._test_get_request('/help', 'frontend/footers/help.html')


class TestUser(TestCase):

    def test_home(self):
        self.login('demo', '123456')
        self._test_get_request('/user/', 'user/index.html')

    def test_follow_unfollow(self):
        user1 = User(name='tester1', email='tester1@example.com', password='123456')
        db.session.add(user1)
        user2 = User(name='tester2', email='tester2@example.com', password='223456')
        db.session.add(user2)
        db.session.commit()

        user1.follow(user2)
        assert user1.num_following == 1
        assert user1.get_following_query().first().id == user2.id
        assert user2.num_followers == 1
        assert user2.get_followers_query().first().id == user1.id

        user1.unfollow(user2)
        assert user1.num_following == 0
        assert user2.num_followers == 0

    def test_send_email(self):
        with mail.record_messages() as outbox:
            mail.send_message(subject='testing',
                    body='test',
                    recipients=['tester@example.com'])

            assert len(outbox) == 1
            assert outbox[0].subject == "testing"


class TestSettings(TestCase):

    def test_profile(self):
        self.login('demo', '123456')
        response = self.client.get('/settings/profile')
        self.assert200(response)
        self.assertTemplateUsed("settings/profile.html")

    def test_password(self):
        self.login('demo', '123456')
        response = self.client.get('/settings/password')
        self.assert200(response)
        self.assertTemplateUsed("settings/password.html")

        data = {
            'password': '123456',
            'new_password': '654321',
            'password_again': '654321',
        }
        response = self.client.post('/settings/password', data=data)
        assert "help-block error" not in response.data
        self.assert200(response)
        self.assertTemplateUsed("settings/password.html")

        updated_user = User.query.filter_by(name='demo').first()
        assert updated_user is not None
        assert updated_user.check_password('654321')


class TestError(TestCase):

    def test_404(self):
        response = self.client.get('/404/')
        self.assert404(response)
        self.assertTemplateUsed('errors/page_not_found.html')


class TestAdmin(TestCase):

    def test_index(self):
        response = self.login('admin', '123456')
        self.assert200(response)

        response = self.client.get('/admin/')
        self.assertTemplateUsed('admin/index.html')
