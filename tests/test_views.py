# -*- coding: utf-8 -*-

from werkzeug.urls import url_quote

from flask import g, request

from fbone.user import User, ADMIN, USER_ROLE, NEW, USER_STATUS
from fbone.extensions import db, mail

from tests import TestCase


class TestFrontend(TestCase):

    def test_show(self):
        self._test_get_request('/', 'index.html')

    def test_signup(self):
        self._test_get_request('/signup', 'frontend/signup.html')

        data = {
            'name':'new_user',
            'email':'new_user@example.com',
            'password':'123456',
            'password_again':'123456'
        }
        response = self.client.post('/signup', data=data)
        assert "help-block error" not in response.data
        new_user = User.query.filter_by(name=data['name']).first()
        assert new_user is not None
        self.assertRedirects(response, location='/user/')

    def test_login(self):
        self._test_get_request('/login', 'frontend/login.html')

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
        assert "help-block error" not in response.data
        self.assert_200(response)
        user = User.query.filter_by(email=data.get('email')).first()
        assert user.activation_key is not None

    def test_footers(self):
        for page in ['about', 'blog', 'help', 'privacy', 'terms']:
            self._test_get_request('/%s' % page, 'frontend/footers/%s.html' % page)


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

        response = self._test_get_request('/search?keywords=%s' % keywords, 'frontend/search.html')
        self.assertTemplateUsed(name='frontend/search.html')
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
        self._test_get_request('/user/%s' % username, 'user/show.html')

        self._login()
        response = self.client.get('/user/%s' % username)
        self.assertRedirects(response, location='/user/')

    def test_home(self):
        response = self.client.get('/user/')
        self.assertRedirects(response, location='/login?next=%s' %
                             url_quote('/user/', safe=''))

        self._login()
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
            mail.send_message(
                    subject='testing',
                    body='test',
                    recipients='tester@example.com'
                    )

            assert len(outbox) == 1
            assert outbox[0].subject == "testing"


class TestSettings(TestCase):

    def test_profile(self):
        endpoint = '/settings/profile'

        response = self.client.get(endpoint)
        self.assertRedirects(response, location='/login?next=%s' % url_quote(endpoint, safe=''))

        user = self._login()
        response = self.client.get('/settings/profile')
        self.assert200(response)
        self.assertTemplateUsed("settings/profile.html")

        data = {
            'name': 'demo1',
            'email': 'demo1@example.com',
            'role_id': ADMIN,
            'status_id': NEW,
            'real_name': user.user_detail.real_name,
            'age': user.user_detail.age,
            'url': user.user_detail.url,
            'location': user.user_detail.location,
            'bio': user.user_detail.bio,
        }
        response = self.client.post(endpoint, data=data)
        print response.data
        assert "help-block error" not in response.data
        self.assert200(response)
        self.assertTemplateUsed("settings/profile.html")
        
        new_user = User.query.filter_by(name=data.get('name')).first()
        assert new_user is not None
        assert new_user.email == data.get('email')
        assert new_user.getRole() == USER_ROLE.get(ADMIN)
        assert new_user.getStatus() == USER_STATUS.get(NEW)

    def test_account(self):
        endpoint = '/settings/account'

        response = self.client.get(endpoint)
        self.assertRedirects(response, location='/login?next=%s' % url_quote(endpoint, safe=''))

        user = self._login()
        response = self.client.get('/settings/account')
        self.assert200(response)
        self.assertTemplateUsed("settings/account.html")

        data = {
            'password':'123456',
            'new_password':'654321',
            'password_again':'654321',
        }
        response = self.client.post(endpoint, data=data)
        assert "help-block error" not in response.data
        self.assert200(response)
        self.assertTemplateUsed("settings/account.html")
        
        updated_user = User.query.filter_by(name=user.name).first()
        assert updated_user is not None
        assert updated_user.check_password('654321')

    def test_avatar(self):
        response = self.client.get('/settings/avatar')
        self.assertRedirects(response, location='/login?next=%s' %
                             url_quote('/settings/avatar', safe=''))

        self._login()
        self._test_get_request('/settings/avatar', 'settings/avatar.html')


class TestAdmin(TestCase):

    def test_show(self):
        self._test_get_request('/admin/')
        self._test_get_request('/admin/usermodel/')
        self._test_get_request('/admin/userdetailmodel/')
        self._test_get_request('/admin/rolemodel/')
        self._test_get_request('/admin/useravatar/')
