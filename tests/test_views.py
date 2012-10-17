# -*- coding: utf-8 -*-

from werkzeug.urls import url_quote

from flask import g, request

from fbone.models import User
from fbone.extensions import db

from tests import TestCase


class TestFrontend(TestCase):

    def setUp(self):
        super(TestFrontend, self).setUp()
        self._make_user()

    def test_show(self):
        self._test_get_request('/', 'index.html')

    def test_signup(self):
        self._test_get_request('/signup', 'signup.html')

        data = {
            'name':'new_user',
            'email':'new_user@bg.com',
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
        self._test_get_request('/reset_password', 'reset_password.html')

        data = {
            'email': self.user.email
        }

        response = self.client.post('/reset_password', data=data)
        self.assertRedirects(response, location='/')
        user = User.query.get(self.user.id)
        assert user.activation_key is not None
        #print g.outbox[0].subject

        old_password = self.user.password
        new_password = 'abcabc'
        data = {
            'activation_key': user.activation_key,
            'email': user.email,
            'password': new_password,
            'password_again': new_password
        }
        response = self.client.post('/change_password', data=data)
        self.assertRedirects(response, location='/login')
        user = User.query.get(self.user.id)
        assert user.password != old_password

        data = {
            'activation_key ': user.activation_key,
        }
        response = self.client.post('/reset_password', data=data)

        data = {
            'email': 'noexisted@test.com'
        }
        response = self.client.post('/reset_password', data=data)
        assert 'error' in response.data

    def test_change_password(self):
        self._login()
        self._test_get_request('/change_password', 'change_password.html')

        old_password = self.user.password
        new_password = 'abcabc'
        data = {
            'password': new_password,
            'password_again': new_password
        }
        response = self.client.post('/change_password', data=data)
        self.assertRedirects(response, location='/login')
        user = User.query.get(self.user.id)
        assert user.password != old_password


class TestSearch(TestCase):

    def setUp(self):
        super(TestSearch, self).setUp()
        for i in range(25):
            name = 'user%d' % i
            email = '%s@test.com' % name
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
        self._search('2@test.com', 3)

    def test_search_email(self):
        self._search('@abc.com', 0)


class TestUser(TestCase):

    def setUp(self):
        super(TestUser, self).setUp()
        self._make_user()

    def test_show(self):
        self._test_get_request('/user/%s' % self.user.name, 'user_pub.html')

        self._login()
        response = self.client.get('/user/%s' % self.user.name)
        self.assertRedirects(response, location='/user/')

    def test_home(self):
        response = self.client.get('/user/')
        self.assertRedirects(response, location='/login?next=%s' %
                             url_quote('/user/', safe=''))

        self._login()
        self._test_get_request('/user/', 'user_index.html')

    def test_follow_unfollow(self):
        user1 = User(name='tester1', email='tester1@test.com', password='123456')
        db.session.add(user1)
        user2 = User(name='tester2', email='tester2@test.com', password='223456')
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
