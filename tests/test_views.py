# -*- coding: utf-8 -*-

from werkzeug.urls import url_quote

from flask import g, request

from fbone.models import User
from fbone.extensions import db, mail

from tests import TestCase


class TestFrontend(TestCase):

    def test_show(self):
        self._test_get_request('/', 'index.html')

    def test_signup(self):
        self._test_get_request('/signup', 'signup.html')

        data = {
            'name':'new_user',
            'email':'new_user@example.com',
            'password':'123456',
            'password_again':'123456'
        }
        response = self.client.post('/signup', data=data)
        new_user = User.query.filter_by(name=data['name']).first()
        assert new_user is not None
        self.assertRedirects(response, location='/user/')

    def test_login(self):
        self._test_get_request('/login', 'login.html')

    def test_logout(self):
        self._login()
        self._logout()

    def test_reset_password(self):
        response = self.client.get('/reset_password')
        self.assert_200(response)

        data = {
            'email':'demo@example.com',
        }
        user = User.query.filter_by(email=data.get('email')).first()
        assert user is not None
        assert user.activation_key is None

        response = self.client.post('/reset_password', data=data)
        self.assert_200(response)
        user = User.query.filter_by(email=data.get('email')).first()
        assert user.activation_key is not None

    def test_footers(self):
        for page in ['about', 'blog', 'help', 'privacy', 'terms']:
            self._test_get_request('/%s' % page, 'footers/%s.html' % page)


class TestSearch(TestCase):

    def setUp(self):
        super(TestSearch, self).setUp()
        for i in range(25):
            name = 'user%d' % i
            email = '%s@example.com' % name
            user = User(name=name, email=email, password='123456')
            db.session.add(user)
        db.session.commit()

    def _search(self, keywords, total):
        """
        Since get_context_variable is only inited in setUp(), we have to split
        them into different test_*().
        """

        response = self._test_get_request('/search?keywords=%s' % keywords, 'search.html')
        self.assertTemplateUsed(name='search.html')
        pagination = self.get_context_variable('pagination')
        assert pagination.total == total

    def test_search_name1(self):
        self._search('user', 25)

    def test_search_name2(self):
        self._search('user11', 1)

    def test_search_name3(self):
        self._search('abc', 0)

    def test_search_email(self):
        self._search('2@example.com', 3)

    def test_search_email(self):
        self._search('@abc.com', 0)


class TestUser(TestCase):

    def test_show(self):
        username = "demo"
        self._test_get_request('/user/%s' % username, 'user_pub.html')

        self._login()
        response = self.client.get('/user/%s' % username)
        self.assertRedirects(response, location='/user/')

    def test_home(self):
        response = self.client.get('/user/')
        self.assertRedirects(response, location='/login?next=%s' %
                             url_quote('/user/', safe=''))

        self._login()
        self._test_get_request('/user/', 'user_index.html')

    def test_settings_profile(self):
        response = self.client.get('/user/settings/profile')
        self.assertRedirects(response, location='/login?next=%s' %
                             url_quote('/user/settings/profile', safe=''))

        self._login()
        self._test_get_request('/user/settings/profile', 'settings/profile.html')

    def test_settings_account(self):
        response = self.client.get('/user/settings/account')
        self.assertRedirects(response, location='/login?next=%s' %
                             url_quote('/user/settings/account', safe=''))

        self._login()
        self._test_get_request('/user/settings/account', 'settings/account.html')

    def test_settings_avatar(self):
        response = self.client.get('/user/settings/avatar')
        self.assertRedirects(response, location='/login?next=%s' %
                             url_quote('/user/settings/avatar', safe=''))

        self._login()
        self._test_get_request('/user/settings/avatar', 'settings/avatar.html')

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
            mail.send_message(
                    subject='testing',
                    body='test',
                    recipients='tester@example.com'
                    )

            assert len(outbox) == 1
            assert outbox[0].subject == "testing"


class TestAdmin(TestCase):

    def test_show(self):
        self._test_get_request('/admin/')
        self._test_get_request('/admin/usermodel/')
        self._test_get_request('/admin/userdetailmodel/')
        self._test_get_request('/admin/rolemodel/')
        self._test_get_request('/admin/useravatar/')
